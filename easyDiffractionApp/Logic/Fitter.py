from PySide6.QtCore import Signal, QObject, QThread

from threading import Thread

from easyCore.Fitting.Fitting import Fitter as CoreFitter
from easyCore import borg


class FitterLogic(QObject):
    """
    Logic related to the fitter setup
    """
    fitFinished = Signal()
    fitStarted = Signal()
    currentMinimizerChanged = Signal()
    finished = Signal(dict)

    def __init__(self, parent=None, sample=None, fit_func=""):
        super().__init__(parent)
        self.fitter = CoreFitter(sample, fit_func)

        self.parent = parent

        # Multithreading
        # self._fitter_thread = None
        self._fit_finished = True
        self._fit_results = self._defaultFitResults()

        self._current_minimizer_method_index = 0
        self._current_minimizer_method_name = self.fitter.available_methods()[0]  # noqa: E501

        self.fit_thread = Thread(target=self.fit_threading)
        self.finished.connect(self._setFitResults)

    def fit_threading(self):
        data = self.data
        method = self.minimizer_name

        self._fit_finished = False
        self.fitStarted.emit()
        exp_data = data.experiments[0]

        x = exp_data.x
        y = exp_data.y
        weights = 1 / exp_data.e

        res = self.fitter.fit(x, y, weights=weights, method=method)
        self.finished.emit(res)

    def _defaultFitResults(self):
        return {
            "success": None,
            "nvarys":  None,
            "GOF":     None,
            "redchi2": None
        }

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

    def fit(self, data):
        self.data = data
        self.minimizer_name = self._current_minimizer_method_name
        if not self.fit_thread.is_alive():
            self.is_fitting_now = True
            self.fit_thread.start()

    ########### QTHREADS #################
    # def fit_qthreads(self, data, minimizer_name):
    #     # if running, stop the thread
    #     if not self._fit_finished:
    #         self.onStopFit()
    #         borg.stack.endMacro()  # need this to close the undo stack properly
    #         return

    #     self._fit_finished = False
    #     self.fitStarted.emit()
    #     exp_data = data.experiments[0]

    #     x = exp_data.x
    #     y = exp_data.y
    #     weights = 1 / exp_data.e
    #     method = minimizer_name

    #     args = (x, y)
    #     kwargs = {"weights": weights, "method": method}
    #     self._fitter_thread = Fitter(self.parent, self.fitter, 'fit', *args, **kwargs)  # noqa: E501
    #     self._fitter_thread.finished.connect(self._setFitResults)
    #     self._fitter_thread.setTerminationEnabled(True)
    #     self._fitter_thread.failed.connect(self._setFitResultsFailed)
    #     self._fitter_thread.start()
    # def _setFitResultsFailed(self, res):
    #     self.finishFitting()

    # def finishFitting(self):
    #     self._fit_finished = True
    #     self.fitFinished.emit()

    # def onStopFit(self):
    #     """
    #     Slot for thread cancelling and reloading parameters
    #     """
    #     self._fitter_thread.terminate()
    #     self._fitter_thread.wait()
    #     self._fitter_thread = None

    #     self._fit_results['success'] = 'cancelled'
    #     self._fit_results['nvarys'] = None
    #     self._fit_results['GOF'] = None
    #     self._fit_results['redchi2'] = None
    #     self._setFitResultsFailed("Fitting stopped")
    # def setFitFinished(self, fit_finished: bool):
    #     if self._fit_finished == fit_finished:
    #         return
    #     self._fit_finished = fit_finished

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
            self.currentMinimizerChanged.emit()
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
