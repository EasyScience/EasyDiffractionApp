# SPDX-FileCopyrightText: 2022 easyDiffraction contributors <support@easydiffraction.org>
# SPDX-License-Identifier: BSD-3-Clause
# © 2021-2022 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

from PySide2.QtCore import Signal, QObject, QThread

import numpy as np

from threading import Thread

from easyDiffractionLib.interface import InterfaceFactory as Calculator
from easyCore.Fitting.Fitting import Fitter as CoreFitter
from easyCore.Fitting.Constraints import ObjConstraint, NumericConstraint

from dicttoxml import dicttoxml
from distutils.util import strtobool


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
    failed = Signal(str)
    constraintsRemoved = Signal()

    def __init__(self, parent=None, interface=None):
        super().__init__(parent)

        self.parent = parent
        self.interface = interface
        self.fitter = CoreFitter(self.parent.sample(), self.interface.fit_func)

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
        self.finished.connect(self.onSuccess)
        self.failed.connect(self.onFailed)

    def fit_nonpolar(self):
        data = self.data
        method = self._current_minimizer_method_name

        self._fit_finished = False
        self.fitStarted.emit()
        exp_data = data.experiments[0]

        x = exp_data.x
        y = exp_data.y
        weights = 1 / exp_data.e

        kwargs = {
            'weights': weights,
            'method': method
        }

        local_kwargs = {}
        if method == 'least_squares':
            kwargs['minimizer_kwargs'] = {'diff_step': 1e-5}

        # save some kwargs on the interface object for use in the calculator
        self.interface._InterfaceFactoryTemplate__interface_obj.saved_kwargs = local_kwargs
        try:
            res = self.fitter.fit(x, y, **kwargs)

        except Exception as ex:
            self.failed.emit(str(ex))
            return
        self.finished.emit(res)

    def fit_polar(self):
        data = self.data
        method = self._current_minimizer_method_name
        self._fit_finished = False
        self.fitStarted.emit()
        exp_data = data.experiments[0]
        x = exp_data.x

        refinement = self.parent.refinementMethods()
        targets = [component for component in refinement if refinement[component]]
        try:
            x_, y_, fit_func = self.interface().generate_pol_fit_func(x, exp_data.y, exp_data.yb, targets)
        except Exception as ex:
            raise NotImplementedError('This is not implemented for this calculator yet')
        weights = 1/exp_data.e
        weights = np.tile(weights, len(targets))

        kwargs = {
            'weights': weights,
            'method': method
        }

        local_kwargs = {}
        if method == 'least_squares':
            kwargs['minimizer_kwargs'] = {'diff_step': 1e-5}

        # save some kwargs on the interface object for use in the calculator
        # TODO FIX THIS THIS IS NOT THE WAY TO DO IT :-/
        self.interface._InterfaceFactoryTemplate__interface_obj.saved_kwargs = local_kwargs
        try:
            obj = self.fitter.fit_object
            fitter = CoreFitter(obj, fit_func)
            res = fitter.fit(x_, y_, **kwargs)
        except Exception as ex:
            self.failed.emit(str(ex))
            return
        self.finished.emit(res)

    def fit_threading(self):
        if self.parent.isSpinPolarized():
            self.fit_polar()
        else:
            self.fit_nonpolar()

    def setFailedFitResults(self):
        self._fit_results = _defaultFitResults()
        self._fit_results['success'] = 'Failure'  # not None but a string

    def setSuccessFitResults(self, res):
        self._fit_results = {
            "success": res.success,
            "nvarys":  res.n_pars,
            "GOF":     float(res.goodness_of_fit),
            "redchi2": float(res.reduced_chi)
        }

    def resetErrors(self):
        # Reset all errors to zero
        all_pars = set(self.parent.sample().get_parameters())
        fit_pars = {par for par in all_pars if par.enabled and not par.fixed}
        to_zero = all_pars.difference(fit_pars)
        borg = self.parent.sample()._borg
        borg.stack.beginMacro('reset errors')
        for par in to_zero:
            par.error = 0.
        borg.stack.endMacro()
        macro = borg.stack.history.popleft()
        for command in macro._commands:
            borg.stack.history[0]._commands.appendleft(command)

    def joinFitThread(self):
        if self.fit_thread.is_alive():
            self.fit_thread.join()

    def finishFit(self):
        self._fit_finished = True
        self.fitFinished.emit()
        # TODO: remove once background is correctly implemented in polarized
        if self.parent.isSpinPolarized():
            self.parent.setSpinComponent()
        # must re-instantiate the thread object
        self.fit_thread = Thread(target=self.fit_threading)

    def onSuccess(self, res):
        self.joinFitThread()
        self.resetErrors()
        self.setSuccessFitResults(res)
        self.finishFit()

    def onFailed(self, ex):
        print("**** onFailed: fit FAILED with:\n {}".format(str(ex)))
        self.joinFitThread()
        self.setFailedFitResults()
        self.finishFit()

    # def fit(self, data):
    def fit(self):
        self.data = self.parent.pdata()
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
            idx = self.minimizerMethodNames().index('least_squares')
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
            'lmfit': ['least_squares', 'leastsq'], # 'least_squares', 'powell', 'cobyla', 'leastsq'
            'bumps': ['lm'], # 'newton', 'lm'
            'DFO_LS': ['leastsq']
        }
        return tested_methods[current_minimizer]

    def currentMinimizerMethodIndex(self, new_index: int):
        if self._current_minimizer_method_index == new_index:
            return

        self._current_minimizer_method_index = new_index
        self._current_minimizer_method_name = self.minimizerMethodNames()[new_index]  # noqa: E501
        self.currentMinimizerMethodChanged.emit()

    def setNewEngine(self, engine=None, method=None):
        new_engine_index = self.fitter.available_engines.index(engine)
        self.setCurrentMinimizerIndex(new_engine_index)
        new_method_index = self.minimizerMethodNames().index(method)
        self.currentMinimizerMethodIndex(new_method_index)

    def fittingNamesDict(self):
        return {
            'engine': self.fitter.current_engine.name,
            'method': self._current_minimizer_method_name
            }

    ####################################################################################################################
    # Calculator
    ####################################################################################################################

    def calculatorNames(self):
        interfaces = self.interface.interface_compatability(self.parent.sample().exp_type_str)
        return interfaces

    def currentCalculatorIndex(self):
        interfaces = self.interface.interface_compatability(self.parent.sample().exp_type_str)
        return interfaces.index(self.interface.current_interface_name)

    def setCurrentCalculatorIndex(self, new_index: int):
        if self.currentCalculatorIndex == new_index:
            return
        interfaces = self.interface.interface_compatability(self.parent.sample().exp_type_str)
        new_name = interfaces[new_index]
        self.interface.switch(new_name)
        # recreate the fitter object with the new interface
        self.fitter = CoreFitter(self.parent.sample(), self.interface.fit_func)

        self.parent.sample().update_bindings()
        self.currentCalculatorChanged.emit()
        print("***** _onCurrentCalculatorChanged")
        data = self.parent.pdata().simulations[0]
        data.name = f'{self.interface.current_interface_name} engine'
        self.parent.updateCalculatedData()

    # Constraints
    def addConstraint(self, dependent_par_idx, relational_operator,
                      value, arithmetic_operator, independent_par_idx):
        if dependent_par_idx == -1 or value == "":
            print("Failed to add constraint: Unsupported type")
            return
        # if independent_par_idx == -1:
        #    print(f"Add constraint: {self.fitablesList()[dependent_par_idx]['label']}{relational_operator}{value}")
        # else:
        #    print(f"Add constraint: {self.fitablesList()[dependent_par_idx]['label']}{relational_operator}{value}{arithmetic_operator}{self.fitablesList()[independent_par_idx]['label']}")
        pars = [par for par in self.fitter.fit_object.get_parameters() if par.enabled]
        if arithmetic_operator != "" and independent_par_idx > -1:
            c = ObjConstraint(pars[dependent_par_idx],
                              str(float(value)) + arithmetic_operator,
                              pars[independent_par_idx])
        elif arithmetic_operator == "" and independent_par_idx == -1:
            c = NumericConstraint(pars[dependent_par_idx],
                                  relational_operator.replace("=", "=="),
                                  float(value))
        else:
            print("Failed to add constraint: Unsupported type")
            return
        # print(c)
        c()
        self.fitter.add_fit_constraint(c)

    def constraintsList(self):
        constraint_list = []
        for index, constraint in enumerate(self.fitter.fit_constraints()):
            if type(constraint) is ObjConstraint:
                independent_name = constraint.get_obj(constraint.independent_obj_ids).name
                relational_operator = "="
                value = float(constraint.operator[:-1])
                arithmetic_operator = constraint.operator[-1]
            elif type(constraint) is NumericConstraint:
                independent_name = ""
                relational_operator = constraint.operator.replace("==", "=")
                value = constraint.value
                arithmetic_operator = ""
            else:
                print(f"Failed to get constraint: Unsupported type {type(constraint)}")
                return
            number = index + 1
            dependent_name = constraint.get_obj(constraint.dependent_obj_ids).name
            enabled = int(constraint.enabled)
            constraint_list.append(
                {"number": number,
                 "dependentName": dependent_name,
                 "relationalOperator": relational_operator,
                 "value": value,
                 "arithmeticOperator": arithmetic_operator,
                 "independentName": independent_name,
                 "enabled": enabled}
            )
        return constraint_list

    def constraintsAsXml(self):
        xml = dicttoxml(self.constraintsList(), attr_type=False)
        xml = xml.decode()
        return xml

    def removeConstraintByIndex(self, index: int):
        self.fitter.remove_fit_constraint(index)

    def toggleConstraintByIndex(self, index, enabled):
        constraint = self.fitter.fit_constraints()[index]
        constraint.enabled = bool(strtobool(enabled))

    def removeAllConstraints(self):
        for _ in range(len(self.fitter.fit_constraints())):
            self.removeConstraintByIndex(0)
        self.constraintsRemoved.emit()


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
