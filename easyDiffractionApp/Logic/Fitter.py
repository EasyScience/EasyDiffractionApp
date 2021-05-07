from PySide2.QtCore import Signal, QThread

from easyCore.Fitting.Fitting import Fitter as CoreFitter
from easyCore import borg


class FitterLogic():
    """
    Logic related to the fitter setup
    """
    def __init__(self, parent=None, sample=None, fit_func=""):
        self.fitter = CoreFitter(sample, fit_func)

        self.parent = parent

        # Multithreading
        self._fitter_thread = None
        self._fit_finished = True
        self._fit_results = self._defaultFitResults()

    def fit(self, data, minimizer_name):
        # if running, stop the thread
        if not self.parent.isFitFinished:
            self.onStopFit()
            borg.stack.endMacro()  # need this to close the undo stack properly
            return

        self.parent.isFitFinished = False
        exp_data = data.experiments[0]

        x = exp_data.x
        y = exp_data.y
        weights = 1 / exp_data.e
        method = minimizer_name

        args = (x, y)
        kwargs = {"weights": weights, "method": method}
        self._fitter_thread = Fitter(self.fitter, 'fit', *args, **kwargs)
        self._fitter_thread.finished.connect(self._setFitResults)
        self._fitter_thread.setTerminationEnabled(True)
        self._fitter_thread.failed.connect(self._setFitResultsFailed)
        self._fitter_thread.start()

    def _defaultFitResults(self):
        return {
            "success": None,
            "nvarys":  None,
            "GOF":     None,
            "redchi2": None
        }

    def _setFitResults(self, res):
        self._fit_results = {
            "success": res.success,
            "nvarys":  res.n_pars,
            "GOF":     float(res.goodness_of_fit),
            "redchi2": float(res.reduced_chi)
        }
        self.parent.fitResultsChanged.emit()
        self.parent.isFitFinished = True
        self.parent.fitFinished.emit()

    def _setFitResultsFailed(self, res):
        self.parent.isFitFinished = True

    def onStopFit(self):
        """
        Slot for thread cancelling and reloading parameters
        """
        self._fitter_thread.terminate()
        self._fitter_thread.wait()
        self._fitter_thread = None

        self._fit_results['success'] = 'cancelled'
        self._fit_results['nvarys'] = None
        self._fit_results['GOF'] = None
        self._fit_results['redchi2'] = None
        self._setFitResultsFailed("Fitting stopped")

    def _onFitFinished(self):
        self.parent.fitFinishedNotify.emit()
        self.parent.parametersChanged.emit()

    def setFitFinished(self, fit_finished: bool):
        if self._fit_finished == fit_finished:
            return
        self._fit_finished = fit_finished


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
