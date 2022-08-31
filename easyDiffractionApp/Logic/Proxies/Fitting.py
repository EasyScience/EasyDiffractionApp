# SPDX-FileCopyrightText: 2022 easyDiffraction contributors <support@easydiffraction.org>
# SPDX-License-Identifier: BSD-3-Clause
# © 2021-2022 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

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
    calculatorListChanged = Signal()
    currentCalculatorChanged = Signal()
    constraintsChanged = Signal()
    constraintsModified = Signal()


    def __init__(self, parent=None, logic=None):
        super().__init__(parent)

        self.logic = logic.l_fitting
        self.parent = parent
        self.logic.fitStarted.connect(self.fitFinishedNotify)
        self.logic.fitFinished.connect(self.fitFinishedNotify)
        self.logic.fitFinished.connect(self.fitResultsChanged)
        self.logic.constraintsRemoved.connect(self.constraintsChanged)
        self.logic.currentMinimizerChanged.connect(self.currentMinimizerChanged)
        self.logic.currentMinimizerMethodChanged.connect(self.currentMinimizerMethodChanged)
        self.logic.currentCalculatorChanged.connect(self.currentCalculatorChanged)

    @Slot()
    def fit(self):
        # Currently using python threads from the `threading` module,
        # since QThreads don't seem to properly work under macos
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
        self.currentMinimizerChanged.emit()
        self.parent.project.statusInfoChanged.emit()

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
        self.currentMinimizerMethodChanged.emit()
        self.parent.project.statusInfoChanged.emit()

    def _onCurrentMinimizerMethodChanged(self):
        print("***** _onCurrentMinimizerMethodChanged")

    ####################################################################################################################
    # Calculator
    ####################################################################################################################

    @Property('QVariant', notify=calculatorListChanged)
    def calculatorNames(self):
        return self.logic.calculatorNames()

    @Property(int, notify=currentCalculatorChanged)
    def currentCalculatorIndex(self):
        return self.logic.currentCalculatorIndex()

    @currentCalculatorIndex.setter
    @property_stack_deco('Calculation engine change')
    def currentCalculatorIndex(self, new_index: int):
        self.logic.setCurrentCalculatorIndex(new_index)
        self.currentCalculatorChanged.emit()
        self.parent.project.statusInfoChanged.emit()


    ####################################################################################################################
    # Constraints
    ####################################################################################################################

    @Slot(int, str, str, str, int)
    def addConstraint(self, dependent_par_idx, relational_operator,
                      value, arithmetic_operator, independent_par_idx):
        self.logic.addConstraint(dependent_par_idx, relational_operator,
                                 value, arithmetic_operator, independent_par_idx)
        self.constraintsModified()
        self.constraintsChanged.emit()

    @Property(str, notify=constraintsChanged)
    def constraintsAsXml(self):
        return self.logic.constraintsAsXml()

    @Slot(int)
    def removeConstraintByIndex(self, index: int):
        self.logic.removeConstraintByIndex(index)
        self.constraintsModified()
        self.constraintsChanged.emit()

    @Slot(int, str)
    def toggleConstraintByIndex(self, index, enabled):
        self.logic.toggleConstraintByIndex(index, enabled)
        self.constraintsModified()
        self.constraintsChanged.emit()

    def constraintsModified(self):
        self.parent.parameters._setParametersAsObj()
        self.parent.parameters._setParametersAsXml()
        self.parent.parameters._onSimulationParametersChanged()
