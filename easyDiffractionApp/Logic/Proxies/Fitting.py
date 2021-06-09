from PySide2.QtCore import QObject, Signal, Slot, Property
from easyCore.Utils.UndoRedo import property_stack_deco


class FittingProxy(QObject):
    """
    A proxy class to interact between the QML plot and Python datasets.
    """
    fitFinishedNotify = Signal()
    fitResultsChanged = Signal()
    dummySignal = Signal()
    currentMinimizerChanged = Signal()
    currentMinimizerMethodChanged = Signal()
    currentCalculatorChanged = Signal()

    def __init__(self, parent=None, logic=None):
        super().__init__(parent)

        self.logic = logic.l_fitting
        self.logic.fitStarted.connect(self.fitFinishedNotify)
        self.logic.fitFinished.connect(self.fitFinishedNotify)
        self.logic.fitFinished.connect(self.fitResultsChanged)
        self.logic.currentMinimizerChanged.connect(self.currentMinimizerChanged)
        self.logic.currentMinimizerMethodChanged.connect(self.currentMinimizerMethodChanged)
        self.logic.currentCalculatorChanged.connect(self.currentCalculatorChanged)

    @Slot()
    def fit(self):
        # Currently using python threads from the `threading` module,
        # since QThreads don't seem to properly work under macos
        # self.logic.fit(self._data)
        self.logic.fit()

    @Property('QVariant', notify=fitResultsChanged)
    def fitResults(self):
        return self.logic._fit_results

    @Property(bool, notify=fitFinishedNotify)
    def isFitFinished(self):
        return self.logic._fit_finished

    ####################################################################################################################
    # Minimizer
    ####################################################################################################################

    @Property('QVariant', notify=dummySignal)
    def minimizerNames(self):
        return self.logic.fitter.available_engines

    @Property(int, notify=currentMinimizerChanged)
    def currentMinimizerIndex(self):
        return self.logic.currentMinimizerIndex()

    @currentMinimizerIndex.setter
    @property_stack_deco('Minimizer change')
    def currentMinimizerIndex(self, new_index: int):
        self.logic.setCurrentMinimizerIndex(new_index)

    # def _onCurrentMinimizerChanged(self):
    #     print("***** _onCurrentMinimizerChanged")
    #     self.logic.onCurrentMinimizerChanged()

    # Minimizer method
    @Property('QVariant', notify=currentMinimizerChanged)
    def minimizerMethodNames(self):
        return self.logic.minimizerMethodNames()

    @Property(int, notify=currentMinimizerMethodChanged)
    def currentMinimizerMethodIndex(self):
        return self.logic._current_minimizer_method_index

    @currentMinimizerMethodIndex.setter
    @property_stack_deco('Minimizer method change')
    def currentMinimizerMethodIndex(self, new_index: int):
        self.logic.currentMinimizerMethodIndex(new_index)

    def _onCurrentMinimizerMethodChanged(self):
        print("***** _onCurrentMinimizerMethodChanged")

    ####################################################################################################################
    # Calculator
    ####################################################################################################################

    @Property('QVariant', notify=dummySignal)
    def calculatorNames(self):
        return self.logic.calculatorNames()

    @Property(int, notify=currentCalculatorChanged)
    def currentCalculatorIndex(self):
        return self.logic.currentCalculatorIndex()

    @currentCalculatorIndex.setter
    @property_stack_deco('Calculation engine change')
    def currentCalculatorIndex(self, new_index: int):
        self.logic.setCurrentCalculatorIndex(new_index)
