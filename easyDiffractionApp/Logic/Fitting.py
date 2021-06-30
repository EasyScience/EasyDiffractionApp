from PySide2.QtCore import Signal, QObject, QThread

from threading import Thread

from easyCore.Fitting.Fitting import Fitter as CoreFitter


def _defaultFitResults():
    return {
        "success": None,
        "nvarys":  None,
        "GOF":     None,
        "redchi2": None
    }


class FittingLogic(QObject):
    """
    Logic related to the fitter setup
    """
    fitFinished = Signal()
    fitStarted = Signal()
    currentMinimizerChanged = Signal()
    currentMinimizerMethodChanged = Signal()
    currentCalculatorChanged = Signal()
    finished = Signal(dict)

    def __init__(self, parent=None, interface=None):
        super().__init__(parent)

        self.parent = parent
        self.interface = interface
        self.fitter = CoreFitter(self.parent.l_phase._sample, self.interface.fit_func)

        # Multithreading
        # self._fitter_thread = None
        self._fit_finished = True
        self._fit_results = _defaultFitResults()
        self.data = None
        self.is_fitting_now = False
        self._current_minimizer_method_index = 0
        self._current_minimizer_method_name = self.fitter.available_methods()[0]  # noqa: E501
        self.currentMinimizerChanged.connect(self.onCurrentMinimizerChanged)

        self.fit_thread = Thread(target=self.fit_threading)
        self.finished.connect(self._setFitResults)
        self.fitFinished.emit()

    def fit_threading(self):
        data = self.data
        method = self._current_minimizer_method_name

        self._fit_finished = False
        self.fitStarted.emit()
        exp_data = data.experiments[0]

        x = exp_data.x
        y = exp_data.y
        weights = 1 / exp_data.e

        res = self.fitter.fit(x, y, weights=weights, method=method)
        self.finished.emit(res)

    def _setFitResults(self, res):
        if self.fit_thread.is_alive():
            self.fit_thread.join()
        self._fit_results = {
            "success": res.success,
            "nvarys":  res.n_pars,
            "GOF":     float(res.goodness_of_fit),
            "redchi2": float(res.reduced_chi)
        }
        self._fit_finished = True
        self.fitFinished.emit()
        # must reinstantiate the thread object
        self.fit_thread = Thread(target=self.fit_threading)

    # def fit(self, data):
    def fit(self):
        self.data = self.parent.l_parameters._data
        if not self.fit_thread.is_alive():
            self.is_fitting_now = True
            self.fit_thread.start()

    def currentMinimizerIndex(self):
        current_name = self.fitter.current_engine.name
        index = self.fitter.available_engines.index(current_name)
        return index

    def setCurrentMinimizerIndex(self, new_index: int):
        if self.currentMinimizerIndex() == new_index:
            return
        new_name = self.fitter.available_engines[new_index]
        self.fitter.switch_engine(new_name)
        self.currentMinimizerChanged.emit()

    def onCurrentMinimizerChanged(self):
        idx = 0
        minimizer_name = self.fitter.current_engine.name
        if minimizer_name == 'lmfit':
            idx = self.minimizerMethodNames().index('leastsq')
        elif minimizer_name == 'bumps':
            idx = self.minimizerMethodNames().index('lm')
        if -1 < idx != self._current_minimizer_method_index:
            # Bypass the property as it would be added to the stack.
            self._current_minimizer_method_index = idx
            self._current_minimizer_method_name = self.minimizerMethodNames()[idx]  # noqa: E501
            self.currentMinimizerMethodChanged.emit()
        return

    def minimizerMethodNames(self):
        current_minimizer = self.fitter.available_engines[self.currentMinimizerIndex()]  # noqa: E501
        tested_methods = {
            'lmfit': ['leastsq', 'powell', 'cobyla'],
            'bumps': ['newton', 'lm'],
            'DFO_LS': ['leastsq']
        }
        return tested_methods[current_minimizer]

    def currentMinimizerMethodIndex(self, new_index: int):
        if self._current_minimizer_method_index == new_index:
            return

        self._current_minimizer_method_index = new_index
        self._current_minimizer_method_name = self.minimizerMethodNames()[new_index]  # noqa: E501
        self.currentMinimizerMethodChanged.emit()

    ####################################################################################################################
    # Calculator
    ####################################################################################################################

    def calculatorNames(self):
        return self.interface.available_interfaces

    def currentCalculatorIndex(self):
        return self.interface.available_interfaces.index(self.interface.current_interface_name)

    def setCurrentCalculatorIndex(self, new_index: int):
        if self.currentCalculatorIndex == new_index:
            return
        new_name = self.interface.available_interfaces[new_index]
        self.interface.switch(new_name)
        self.currentCalculatorChanged.emit()
        print("***** _onCurrentCalculatorChanged")
        self._onCurrentCalculatorChanged()
        self.parameters._updateCalculatedData()

    def _onCurrentCalculatorChanged(self):
        data = self.parameters._data.simulations
        data = data[0]
        data.name = f'{self.interface.current_interface_name} engine'


class Fitter(QThread):
    """
    Simple wrapper for calling a function in separate thread
    """
    failed = Signal(str)
    finished = Signal(dict)

    def __init__(self, parent, obj, method_name, *args, **kwargs):
        QThread.__init__(self, parent)
        self._obj = obj
        self.method_name = method_name
        self.args = args
        self.kwargs = kwargs

    def run(self):
        res = {}
        if hasattr(self._obj, self.method_name):
            func = getattr(self._obj, self.method_name)
            try:
                res = func(*self.args, **self.kwargs)
            except Exception as ex:
                self.failed.emit(str(ex))
                return str(ex)
            self.finished.emit(res)
        return res

    def stop(self):
        self.terminate()
        self.wait()  # to assure proper termination
