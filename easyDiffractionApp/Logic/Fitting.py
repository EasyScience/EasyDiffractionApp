# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import copy
import lmfit

import numpy as np

from PySide6.QtCore import QObject, Signal, Slot, Property, QThreadPool

from EasyApp.Logic.Logging import console
from Logic.Helpers import IO
from Logic.Data import Data

try:
    from cryspy.procedure_rhochi.rhochi_by_dictionary import \
        rhochi_calc_chi_sq_by_dictionary
    console.debug('CrysPy module imported')
except ImportError:
    console.error('No CrysPy module found')


SCALE = 1

class Worker(QObject):
    finished = Signal()

    def __init__(self, proxy):
        super().__init__()
        self._proxy = proxy
        self._needCancel = False

        self._cryspyDictInitial = copy.deepcopy(self._proxy.data._cryspyDict)
        self._cryspyUsePrecalculatedData = False
        self._cryspyCalcAnalyticalDerivatives = False

        #self._paramsInit = lmfit.Parameters()
        self._paramsFinal = lmfit.Parameters()

        self._gofPrevIter = None
        self._gofLastIter = None

        #QThread.setTerminationEnabled()

    def run(self):

        def callbackFunc(params, iter, resid, *args, **kws):
            chiSq = np.sum(np.square(resid))
            #pointsCount = resid.size
            #freeParamsCount = len(params.valuesdict())
            self._proxy.fitting.chiSq = chiSq / (self._proxy.fitting._pointsCount - self._proxy.fitting._freeParamsCount)
            console.info(IO.formatMsg('main', f'Iteration: {iter:5d}', f'Reduced Chi2: {self._proxy.fitting.chiSq:16g}'))

            # Check if fitting termination is requested
            if self._needCancel:
                self._needCancel = False
                #self._proxy.data._cryspyDict = copy.deepcopy(self._cryspyDictInitial)
                console.error('Terminating the execution of the optimization thread')
                #QThread.terminate()  # Not needed for Lmfit
                return True  # Cancel minimization and return back to after lmfit.minimize

            # Update iteration number in the status bar
            self._proxy.status.fitIteration = f'{iter}'

            # Calc goodness-of-fit (GOF) value shift between iterations
            gofStart = self._proxy.fitting.chiSqStart
            if iter == 1:
                self._gofPrevIter = self._proxy.fitting.chiSqStart
            self._gofLastIter = self._proxy.fitting.chiSq
            gofShift = abs(self._gofLastIter - self._gofPrevIter)
            self._gofPrevIter = self._gofLastIter
            # Update goodness-of-fit (GOF) value updated in the status bar
            if iter == 1 or gofShift > 0.01:
                self._proxy.status.goodnessOfFit = f'{gofStart:0.2f} → {self._gofLastIter:0.2f}'  # NEED move to connection
                self._proxy.fitting.chiSqSignificantlyChanged.emit()

            return False  # Continue minimization

        def residFunc(params):

            # Update CrysPy dict from Lmfit params
            for param in params:
                block, group, idx = Data.strToCryspyDictParamPath(param)
                self._proxy.data._cryspyDict[block][group][idx] = params[param].value

            # Calculate diffraction pattern
            rhochi_calc_chi_sq_by_dictionary(
                self._proxy.data._cryspyDict,
                dict_in_out=self._proxy.data._cryspyInOutDict,
                flag_use_precalculated_data=self._cryspyUsePrecalculatedData,
                flag_calc_analytical_derivatives=self._cryspyCalcAnalyticalDerivatives)

            # Total residual
            totalResid = np.empty(0)
            for dataBlock in self._proxy.experiment.dataBlocksNoMeas:
                ed_name = dataBlock['name']['value']
                cryspy_name = f'pd_{ed_name}'
                cryspyInOutDict = self._proxy.data._cryspyInOutDict

                y_meas_array = cryspyInOutDict[cryspy_name]['signal_exp'][0]
                sy_meas_array = cryspyInOutDict[cryspy_name]['signal_exp'][1]
                y_bkg_array = cryspyInOutDict[cryspy_name]['signal_background']
                y_calc_all_phases_array = cryspyInOutDict[cryspy_name]['signal_plus'] + \
                                          cryspyInOutDict[cryspy_name]['signal_minus']
                y_calc_all_phases_array_with_bkg = y_calc_all_phases_array + y_bkg_array

                resid = (y_calc_all_phases_array_with_bkg - y_meas_array) / sy_meas_array
                totalResid = np.append(totalResid, resid)

            return totalResid

        self._proxy.fitting._freezeChiSqStart = True

        # Save initial state of cryspyDict if cancel fit is requested
        self._cryspyDictInitial = copy.deepcopy(self._proxy.data._cryspyDict)

        # Preliminary calculations
        self._cryspyUsePrecalculatedData = False
        self._cryspyCalcAnalyticalDerivatives = False
        #self._proxy.fitting.chiSq, self._proxy.fitting._pointsCount, _, _, freeParamNames = rhochi_calc_chi_sq_by_dictionary(
        chiSq, pointsCount, _, _, freeParamNames = rhochi_calc_chi_sq_by_dictionary(
            self._proxy.data._cryspyDict,
            dict_in_out=self._proxy.data._cryspyInOutDict,
            flag_use_precalculated_data=self._cryspyUsePrecalculatedData,
            flag_calc_analytical_derivatives=self._cryspyCalcAnalyticalDerivatives)

        # Number of measured data points
        self._proxy.fitting._pointsCount = pointsCount

        # Number of free parameters
        self._proxy.fitting._freeParamsCount = len(freeParamNames)
        if self._proxy.fitting._freeParamsCount != self._proxy.fittables._freeParamsCount:
            console.error(f'Number of free parameters differs. Expected {self._proxy.fittables._freeParamsCount}, got {self._proxy.fitting._freeParamsCount}')

        # Reduced chi-squared goodness-of-fit (GOF)
        self._proxy.fitting.chiSq = chiSq / (self._proxy.fitting._pointsCount - self._proxy.fitting._freeParamsCount)

        # Create lmfit parameters to be varied
        freeParamValuesStart = [self._proxy.data._cryspyDict[way[0]][way[1]][way[2]] for way in freeParamNames]
        paramsLmfit = lmfit.Parameters()
        for cryspyParamPath, val in zip(freeParamNames, freeParamValuesStart):
            lmfitParamName = Data.cryspyDictParamPathToStr(cryspyParamPath)  # Only ascii letters and numbers allowed for lmfit.Parameters()???
            left = self._proxy.model.paramValueByFieldAndCrypyParamPath('min', cryspyParamPath)
            if left is None:
                left = self._proxy.experiment.paramValueByFieldAndCrypyParamPath('min', cryspyParamPath)
            if left is None:
                left = -np.inf
            right = self._proxy.model.paramValueByFieldAndCrypyParamPath('max', cryspyParamPath)
            if right is None:
                right = self._proxy.experiment.paramValueByFieldAndCrypyParamPath('max', cryspyParamPath)
            if right is None:
                right = np.inf
            paramsLmfit.add(lmfitParamName, value=val, min=left, max=right)

        # Minimization: lmfit.minimize
        self._proxy.fitting.chiSqStart = self._proxy.fitting.chiSq
        self._cryspyUsePrecalculatedData = True
        method = 'BFGS'
        tol = 1e+3
        method = 'L-BFGS-B'
        tol = 1e-2
        method = self._proxy.fitting.minimizerMethod
        tol = self._proxy.fitting.minimizerTol
        reduce_fcn = None  # None : sum-of-squares of residual (default) = (r*r).sum()
        result = lmfit.minimize(residFunc,
                                paramsLmfit,
                                args=(),
                                method=method,
                                reduce_fcn=reduce_fcn,
                                iter_cb=callbackFunc,
                                tol=tol)

        #lmfit.report_fit(result)

        # Optimization status
        if result.success:  # NEED FIX: Move to connections. Pass names via signal.emit(names)
            console.info('Optimization successfully finished')
            self._proxy.status.fitStatus = 'Success'
        else:
            if result.aborted:
                console.info('Optimization aborted')
                self._proxy.status.fitStatus = 'Aborted'
                #self.cancelled.emit()
            else:
                console.info('Optimization failed')
                self._proxy.status.fitStatus = 'Failure'
                ## Restore cryspyDict from the state before minimization started
                #self._proxy.data._cryspyDict = copy.deepcopy(self._cryspyDictInitial)

        # Update CrysPy dict with the best params after minimization finished/aborted/failed
        for param in result.params:
            block, group, idx = Data.strToCryspyDictParamPath(param)
            self._proxy.data._cryspyDict[block][group][idx] = result.params[param].value

        # Calculate optimal chi2
        self._cryspyUsePrecalculatedData = False
        self._cryspyCalcAnalyticalDerivatives = False
        chiSq, _, _, _, _ = rhochi_calc_chi_sq_by_dictionary(
            self._proxy.data._cryspyDict,
            dict_in_out=self._proxy.data._cryspyInOutDict,
            flag_use_precalculated_data=self._cryspyUsePrecalculatedData,
            flag_calc_analytical_derivatives=self._cryspyCalcAnalyticalDerivatives)
        self._proxy.fitting.chiSq = chiSq / (self._proxy.fitting._pointsCount - self._proxy.fitting._freeParamsCount)
        console.info(f"Optimal reduced chi2 per {self._proxy.fitting._pointsCount} points and {self._proxy.fitting._freeParamsCount} free params: {self._proxy.fitting.chiSq:.2f}")
        self._proxy.status.goodnessOfFit = f'{self._proxy.fitting.chiSqStart:0.2f} → {self._proxy.fitting.chiSq:0.2f}'  # NEED move to connection
        self._proxy.fitting.chiSqSignificantlyChanged.emit()

        # Update internal dicts with the best params
        #names = [Data.cryspyDictParamPathToStr(name) for name in parameter_names_free]
        #self._proxy.experiment.editDataBlockByCryspyDictParams(names)
        #self._proxy.model.editDataBlockByCryspyDictParams(names)
        self._proxy.experiment.editDataBlockByLmfitParams(result.params)
        self._proxy.model.editDataBlockByLmfitParams(result.params)

        # Finishing
        self._proxy.fitting._freezeChiSqStart = False
        self.finished.emit()
        console.info('Optimization process has been finished')


class Fitting(QObject):
    isFittingNowChanged = Signal()
    fitFinished = Signal()
    chiSqStartChanged = Signal()
    chiSqChanged = Signal()
    chiSqSignificantlyChanged = Signal()
    minimizerMethodChanged = Signal()
    minimizerTolChanged = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self._proxy = parent
        self._threadpool = QThreadPool.globalInstance()
        self._worker = Worker(self._proxy)
        self._isFittingNow = False

        self._chiSq = None
        self._chiSqStart = None
        self._freezeChiSqStart = False

        self._pointsCount = None
        self._freeParamsCount = 0

        self._minimizerMethod = 'BFGS'
        self._minimizerTol = 1e+3

        self._worker.finished.connect(self.setIsFittingNowToFalse)
        self._worker.finished.connect(self.fitFinished)

    @Property(str, notify=minimizerMethodChanged)
    def minimizerMethod(self):
        return self._minimizerMethod

    @minimizerMethod.setter
    def minimizerMethod(self, newValue):
        if self._minimizerMethod == newValue:
            return
        self._minimizerMethod = newValue
        self.minimizerMethodChanged.emit()

    @Property(float, notify=minimizerTolChanged)
    def minimizerTol(self):
        return self._minimizerTol

    @minimizerTol.setter
    def minimizerTol(self, newValue):
        if self._minimizerTol == newValue:
            return
        self._minimizerTol = newValue
        self.minimizerTolChanged.emit()

    @Property(bool, notify=isFittingNowChanged)
    def isFittingNow(self):
        return self._isFittingNow

    @isFittingNow.setter
    def isFittingNow(self, newValue):
        if self._isFittingNow == newValue:
            return
        self._isFittingNow = newValue
        self.isFittingNowChanged.emit()

    @Property(float, notify=chiSqStartChanged)
    def chiSqStart(self):
        return self._chiSqStart

    @chiSqStart.setter
    def chiSqStart(self, newValue):
        if self._chiSqStart == newValue:
            return
        self._chiSqStart = newValue
        self.chiSqStartChanged.emit()

    @Property(float, notify=chiSqChanged)
    def chiSq(self):
        return self._chiSq

    @chiSq.setter
    def chiSq(self, newValue):
        if self._chiSq == newValue:
            return
        self._chiSq = newValue
        self.chiSqChanged.emit()

    @Slot()
    def startStop(self):
        self._proxy.status.fitStatus = ''

        if self._worker._needCancel:
            console.debug('Minimization process has been already requested to cancel')
            return

        if self.isFittingNow:
            self._worker._needCancel = True
            console.debug('Minimization process has been requested to cancel')
        else:
            if self._proxy.fittables._freeParamsCount > 0:
                self.isFittingNow = True
                #self._worker.run()
                self._threadpool.start(self._worker.run)
                console.debug('Minimization process has been started in a separate thread')
            else:
                self._proxy.status.fitStatus = 'No free params'
                console.debug('Minimization process has not been started. No free parameters found.')

    def setIsFittingNowToFalse(self):
        self.isFittingNow = False


#https://stackoverflow.com/questions/30843876/using-qthreadpool-with-qrunnable-in-pyqt4
#https://stackoverflow.com/questions/70868493/what-is-the-best-way-to-stop-interrupt-qrunnable-in-qthreadpool
#https://stackoverflow.com/questions/24825441/stop-scipy-minimize-after-set-time
#https://stackoverflow.com/questions/22390479/qrunnable-trying-to-abort-a-task
