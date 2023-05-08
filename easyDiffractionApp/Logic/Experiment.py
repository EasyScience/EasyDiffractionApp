# SPDX-FileCopyrightText: 2023 easyDiffraction contributors <support@easydiffraction.org>
# SPDX-License-Identifier: BSD-3-Clause
# © 2021-2023 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

# noqa: E501

from gemmi import cif
import numpy as np
import pathlib
import json

from PySide2.QtCore import Signal, QObject

from easyCore import np
from easyCore.Utils.io.xml import XMLSerializer
from easyApp.Logic.Utils.Utils import generalizePath
from easyDiffractionLib.Jobs import get_job_from_file


class ExperimentLogic(QObject):
    """
    """
    # signals controlled by LC
    experimentLoadedChanged = Signal()
    experimentSkippedChanged = Signal()
    clearFrontendState = Signal()

    # signals controlled by our proxy
    patternParametersAsObjChanged = Signal()
    structureParametersChanged = Signal()
    experimentDataAsXmlChanged = Signal()

    def __init__(self, parent=None, interface=None):
        super().__init__(parent)
        self.parent = parent
        self._interface = interface
        self._experiment_parameters = None
        self._experiment_data_as_xml = ""
        self._experiment_data_as_cif = ""
        self.experiment_data = None
        self._experiment_data = None
        self._experiment_loaded = False
        self._experiment_skipped = False
        self.experiments = self._defaultExperiments()
        self.clearFrontendState.connect(self.onClearFrontendState)
        self.spin_polarized = False
        self._current_spin_component = 'Sum'
        self._refine_sum = True
        self._refine_diff = True
        self._refine_up = False
        self._refine_down = False
        self.fn_aggregate = self.pol_sum

    def _defaultExperiment(self):
        return {
            "label": "D1A@ILL",
            "color": "#00a3e3"
        }

    def _loadExperimentCif(self, file_url):
        print("+ _loadExperimentCif")
        file_path = generalizePath(file_url)
        block = cif.read(file_path).sole_block()
        data = self.experimentFromCifBlock(block)

        # load content of the cif file as string
        # This will assume that generated CIF is the same as the one loaded
        with open(file_path, 'r') as f:
            cif_string = f.read()
        self._experiment_data_as_cif = cif_string

        # job name from file nameF_onExperimentDataAdded
        job_name = pathlib.Path(file_path).stem
        if not hasattr(self, 'job') or self.job is None:
            _, self.job = get_job_from_file(file_path, job_name, phases=self.parent.phases(), interface=self._interface)
        else:
            self.job.from_cif_file(file_path, experiment_name=job_name)

        self._interface.interface_obj.set_exp_cif(self._experiment_data_as_cif)
        # self._interface._InterfaceFactoryTemplate__interface_obj.set_exp_cif(self._experiment_data_as_cif)
        # Update job on sample
        self.parent.l_sample._sample = self.job

        return data

    def _loadExperimentCifString(self, cif_string):
        print("+ _loadExperimentCifString")
        block = cif.read_string(cif_string).sole_block()
        # this now contains no data, since we don't want to flood the text viewer
        data = self.experimentFromCifBlock(block)
        # Update job's instrument data
        self.job.from_cif_string(cif_string)
        self.parent.l_sample._sample = self.job
        return data

    def experimentFromCifBlock(self, block):
        """
        Loads experimental parameters from cif string
        """
        data = self.parent.experiments()[0]
        if type(block) is str:
            block = cif.read_string(block).sole_block()
        # at this point self.job is not yet defined, so query block
        if block.find_loop("_tof_meas_time").tag is not None or block.find_loop("_tof_meas_time_of_flight").tag is not None:
            #header = "_pd_meas_time_of_flight" # ?? which format is correct?
            header = "_tof_meas_time"
            prefix = "_tof_"
        else:
            header = "_pd_meas_2theta"
            prefix = "_pd_"
        # Polarized case
        data.x = np.fromiter(block.find_loop(header), float)
        data.y = np.fromiter(block.find_loop(prefix+"meas_intensity_up"), float)
        data.e = np.fromiter(block.find_loop(prefix+"meas_intensity_up_sigma"), float)
        data.yb = np.fromiter(block.find_loop(prefix+"meas_intensity_down"), float)
        data.eb = np.fromiter(block.find_loop(prefix+"meas_intensity_down_sigma"), float)
        spin_polarized = True
        # Unpolarized case
        if not np.any(data.y):
            data.x = np.fromiter(block.find_loop(header), float)
            data.y = np.fromiter(block.find_loop(prefix+"meas_intensity"), float)
            data.e = np.fromiter(block.find_loop(prefix+"meas_intensity_sigma"), float)
            data.yb = np.zeros(len(data.y))
            data.eb = np.zeros(len(data.e))
            spin_polarized = False
        # setting spin polarization needs to be done first, before experiment is loaded
        self.setPolarized(spin_polarized)

        # Get phase parameters
        sample_phase_labels = self.parent.getPhaseNames()
        experiment_phase_labels = list(block.find_loop("_phase_label"))
        experiment_phase_scales = np.fromiter(block.find_loop("_phase_scale"), float)
        for (phase_label, phase_scale) in zip(experiment_phase_labels, experiment_phase_scales):
            if phase_label in sample_phase_labels:
                self.parent.setPhaseScale(phase_label, phase_scale)

        return data

    def _loadExperimentData(self, file_url):
        print("+ _loadExperimentData")
        file_path = generalizePath(file_url)
        job_name = pathlib.Path(file_path).stem

        data = self.parent.experiments()[0]
        # TODO: figure out how to tell ToF from CW
        try:
            data.x, data.y, data.e, data.yb, data.eb = np.loadtxt(file_path, unpack=True)
            self.setPolarized(True)
            self.job = self.parent.l_sample._defaultCWPolJob(name=job_name)
        except Exception as e:
            data.x, data.y, data.e = np.loadtxt(file_path, unpack=True)
            data.yb = np.zeros(len(data.y))
            data.eb = np.zeros(len(data.e))
            self.setPolarized(False)
            # check if set to ToF
            current_type = self.parent.experimentType()
            if 'TOF' in current_type:
                self.job = self.parent.l_sample._defaultTOFJob(name=job_name)
            else:
                self.job = self.parent.l_sample._defaultCWJob(name=job_name)

        # Update job on sample
        self.parent.l_sample._sample = self.job
        return data

    def _experimentDataParameters(self, data):
        x_min = data.x[0]
        x_max = data.x[-1]
        x_step = (x_max - x_min) / (len(data.x) - 1)
        parameters = {
            "x_min":  x_min,
            "x_max":  x_max,
            "x_step": x_step
        }
        return parameters

    def _defaultExperiments(self):
        return []

    def refinement(self):
        return {"sum": self._refine_sum, "diff": self._refine_diff, "up": self._refine_up, "down": self._refine_down}

    def refinement_methods(self):
        return {self.pol_sum: self._refine_sum, self.pol_diff: self._refine_diff, self.pol_up: self._refine_up, self.pol_down: self._refine_down}

    def setPolarized(self, polarized: bool):
        if self.spin_polarized == polarized:
            return False
        current_type = self.parent.experimentType()
        if 'TOF' in current_type:
            return False # no polarized for TOF

        self.spin_polarized = polarized
        if polarized:
            if 'unp' in current_type:
                current_type = current_type.replace('unp', 'pol')
            elif 'pol' in current_type:
                return False # no change
            else:
                # old style unpolarized
                current_type = current_type + "pol"
        else:
            if 'pol' in current_type:
                current_type = current_type.replace('pol', 'unp')

        self.parent.setExperimentType(current_type)
        # need to recalculate the profile
        self.parent.updateCalculatedData()
        return True

    def updateExperimentData(self, name=None):
        self._experiment_data = self.parent.experiments()[0]
        self.experiments = [{'name': name}]
        self.setCurrentExperimentDatasetName(name)
        self.setPolarized(self.spin_polarized)
        self._onExperimentDataAdded()

    def experimentLoaded(self, loaded: bool):
        if self._experiment_loaded == loaded:
            return
        self._experiment_loaded = loaded
        self.experimentLoadedChanged.emit()

    def experimentSkipped(self, skipped: bool):
        if self._experiment_skipped == skipped:
            return
        self._experiment_skipped = skipped
        self.experimentSkippedChanged.emit()

    def experimentDataAsObj(self):
        return [{'name': experiment.name} for experiment in self.parent.experiments()]

    def _setExperimentDataAsXml(self):
        self._experiment_data_as_xml = XMLSerializer().encode({"item":self.experiments}, skip=['interface'])
        self._experiment_data_as_cif = self.as_cif()

    def addExperimentDataFromCif(self, file_url):
        self.parent.shouldProfileBeCalculated = False # don't run update until we're done with setting parameters
        self._experiment_data = self._loadExperimentCif(file_url)
        self.newExperimentUpdate(file_url)

    def addExperimentDataFromXye(self, file_url):
        self._experiment_data = self._loadExperimentData(file_url)
        self.newExperimentUpdate(file_url)

    def newExperimentUpdate(self, file_url):
        self.parent.setExperimentName(pathlib.Path(file_url).stem)
        self.experiments = [{'name': experiment.name} for experiment in self.parent.experiments()]
        self.experimentLoaded(True)
        self.experimentSkipped(False)
        # slot in Exp proxy -> notify parameter proxy
        self.structureParametersChanged.emit()

    def addBackgroundDataFromCif(self, file_url):
        file_path = generalizePath(file_url)
        block = cif.read(file_path).sole_block()
        # Get background
        if (self.is_tof()):
            x_label = "_tof_background_time"
            y_label = "_tof_background_intensity"
        else:
            x_label = "_pd_background_2theta"
            y_label = "_pd_background_intensity"
        background_2thetas = np.fromiter(block.find_loop(x_label), float)
        background_intensities = np.fromiter(block.find_loop(y_label), float)
        self.parent.setBackgroundPoints(background_2thetas, background_intensities)

    def removeExperiment(self):
        self.parent.removeBackgroundPoints()
        self.parent.l_sample.reset()
        self.parent.removeAllConstraints()
        self._current_spin_component = 'Sum'
        self.experiments.clear()
        self._experiment_data = None
        self.experimentLoaded(False)
        self.experimentSkipped(False)
        self.setPolarized(False)
        self.parent.clearFrontendState()

    def _onExperimentSkippedChanged(self):
        self.parent.updateCalculatedData()

    def _onExperimentLoadedChanged(self):
        self.parent.onPatternParametersChanged()

    def setCurrentExperimentDatasetName(self, name):
        self.parent.setCurrentExperimentDatasetName(name)

    def initializeBackground(self):
        self.parent.setMeasuredData(
                                    self._experiment_data.x,
                                    self._experiment_data.y + self._experiment_data.yb,
                                    self._experiment_data.e + self._experiment_data.eb)

        self.parent.setSimulationParameters(json.dumps(self._experiment_parameters))
        self.parent.initializeContainer()

    def _onExperimentDataAdded(self):
        print("***** _onExperimentDataAdded")
        # default settings are up+down
        self.parent.setMeasuredData(
                                    self._experiment_data.x,
                                    self._experiment_data.y + self._experiment_data.yb,
                                    self._experiment_data.e + self._experiment_data.eb)
        self._experiment_parameters = \
            self._experimentDataParameters(self._experiment_data)

        # notify parameter proxy
        params_json = json.dumps(self._experiment_parameters)
        self.parent.shouldProfileBeCalculated = True # now we can run update

        self._experiment_data_as_cif = self.as_cif() # need to redo this here
        self._interface.interface_obj.set_exp_cif(self._experiment_data_as_cif)

        self.parent.setSimulationParameters(params_json)
        if len(self.parent.sampleBackgrounds()) == 0:
            self.parent.initializeContainer()

        self.parent.setExperimentNameFromParameters()
        self.parent.notifyProjectChanged()

        # another go after setting the background
        # self._interface._InterfaceFactoryTemplate__interface_obj.set_exp_cif(self._experiment_data_as_cif)
        # self._interface.interface_obj.set_exp_cif(self._experiment_data_as_cif)

    def _onPatternParametersChanged(self):
        self.parent.setPatternParametersAsObj()
        # slot in Exp proxy -> notify Param proxy
        self.patternParametersAsObjChanged.emit()
        # Now, update the CIF representation
        self._setExperimentDataAsXml()
        # and notify the proxy that CIF changed
        self.experimentDataAsXmlChanged.emit()

    def onClearFrontendState(self):
        self.parent.clearFrontendState()

    def spinComponent(self):
        return self._current_spin_component

    @staticmethod
    def pol_sum(a, b):
        return a + b

    @staticmethod
    def pol_diff(a, b):
        return a - b

    @staticmethod
    def pol_up(a, b):
        return a

    @staticmethod
    def pol_down(a, b):
        return b

    def setSpinComponent(self, component=None):
        if self._current_spin_component == component:
            return False
        if component is not None:
            self._current_spin_component = component

        phase_label = self.parent.getPhaseNames()[0]
        components = self._interface.get_phase_components(phase_label)
        calc_y = components['components']['up']
        calc_yb = components['components']['down']
        bg = self._interface.get_component('f_background') * 2.0

        self.fn_aggregate = self.pol_sum
        has_experiment = self._experiment_data is not None
        if self._current_spin_component == 'Sum':
            if has_experiment:
                y = self._experiment_data.y + self._experiment_data.yb
                e = self._experiment_data.e + self._experiment_data.eb
            sim_y = calc_y + calc_yb + bg
            self.fn_aggregate = self.pol_sum
        elif self._current_spin_component == 'Difference':
            if has_experiment:
                y = self._experiment_data.y - self._experiment_data.yb
                e = self._experiment_data.e + self._experiment_data.eb
            bg = np.zeros_like(bg)
            sim_y = calc_y - calc_yb
            self.fn_aggregate = self.pol_diff
        elif self._current_spin_component == 'Up':
            if has_experiment:
                y = self._experiment_data.y
                e = self._experiment_data.e
            bg = bg / 2
            sim_y = calc_y + bg
            self.fn_aggregate = self.pol_up
        elif self._current_spin_component == 'Down':
            if has_experiment:
                y = self._experiment_data.yb
                e = self._experiment_data.eb
            bg = bg / 2
            sim_y = calc_yb + bg
            self.fn_aggregate = self.pol_down
        else:
            return False

        if has_experiment:
            sim_x = self._experiment_data.x
        else:
            sim_x = self.parent.sim_x()
        self.parent.setBackgroundData(sim_x, bg)
        if has_experiment:
            self.parent.setMeasuredData(self._experiment_data.x, y, e)

        self.parent.setCalculatedData(sim_x, sim_y)

        return has_experiment

    def refineSum(self):
        return self._refine_sum

    def setRefineSum(self, value):
        self._refine_sum = value

    def refineDiff(self):
        return self._refine_diff

    def setRefineDiff(self, value):
        self._refine_diff = value

    def refineUp(self):
        return self._refine_up

    def setRefineUp(self, value):
        self._refine_up = value

    def refineDown(self):
        return self._refine_down

    def setRefineDown(self, value):
        self._refine_down = value

    def is_tof(self):
        return "tof" in str(self.job).replace(" `"+self.job.name+"`", "").lower()
    
    def is_pol(self):
        return "pol" in str(self.job).replace(" `"+self.job.name+"`", "").lower()

    def as_cif(self):
        '''
        Returns a CIF representation of the experiment.
        (pattern, background, instrument, data points etc.)
        '''
        # header
        self.job = self.parent.l_sample._sample
        cif = "data_" + self.job.name + "\n\n"
        if self.is_tof():
            cif += self.tof_param_as_cif() + "\n\n"
            is_tof = True
        else:
            cif += self.cw_param_as_cif()+  "\n\n"

        if self.is_pol():
            cif += self.polar_param_as_cif() + "\n\n"

        cif += self.phases_as_cif() + "\n\n"
        cif += self.background_as_cif() + "\n\n"
        cif += self.exp_data_as_cif() + "\n\n"
        return cif

    def phases_as_cif(self):
        '''
        Returns a CIF representation of the phases names and scales.
        '''
        cif_phase = "loop_\n"
        cif_phase += "_phase_label\n"
        cif_phase += "_phase_scale\n"
        cif_phase += "_phase_igsize\n"
        for phase in self.parent.l_sample._sample.phases:
            cif_phase += phase.name + " " + str(phase.scale.raw_value) + " 0.0\n"
        return cif_phase

    def exp_data_as_cif(self):
        '''
        Returns a CIF representation of the experimental datapoints x,y,e.
        '''
        if not hasattr(self, '_experiment_data'):
            return ""
        if self._experiment_data is None:
            return ""

        cif_exp_data = "_range_2theta_min " + str(self._experiment_data.x[0]) + "\n"
        cif_exp_data += "_range_2theta_max " + str(self._experiment_data.x[-1]) + "\n"
        cif_exp_data += "_setup_radiation neutrons\n"

        cif_exp_data += "\nloop_"

        if self.is_tof():
            cif_exp_data += "\n_tof_meas_time"
            cif_prefix = "_tof_"
        else:
            cif_exp_data += "\n_pd_meas_2theta"
            cif_prefix = "_pd_"

        if self.is_pol():
            cif_exp_data += "\n" + \
                            cif_prefix + "meas_intensity_up\n" + \
                            cif_prefix + "meas_intensity_up_sigma\n" + \
                            cif_prefix + "meas_intensity_down\n" + \
                            cif_prefix + "meas_intensity_down_sigma"
        else:
            cif_exp_data += "\n" + \
                            cif_prefix + "meas_intensity\n" + \
                            cif_prefix + "meas_intensity_sigma"

        for i in range(len(self._experiment_data.x)):
            cif_exp_data += "\n" + str(self._experiment_data.x[i]) + " "
            if self.is_pol():
                cif_exp_data += str(self._experiment_data.y[i]) + " " + \
                    str(self._experiment_data.e[i]) + " " + \
                    str(self._experiment_data.yb[i]) + " " + \
                    str(self._experiment_data.eb[i])
            else:
                cif_exp_data += str(self._experiment_data.y[i]) + " " + \
                    str(self._experiment_data.e[i])

        return cif_exp_data

    def background_as_cif(self):
        '''
        Returns a CIF representation of the background.
        '''
        cif_background = ""
        if self.parent.l_background._background_as_obj is None:
            return cif_background

        if self.is_tof():
            cif_background += "\nloop_\n_tof_background_time\n_tof_background_intensity"
        else:
            cif_background += "\nloop_ \n_pd_background_2theta\n_pd_background_intensity"
        background = self.parent.l_background._background_as_obj
        for i in range(len(background.data)):
            cif_background += "\n" + str(background.data[i].x.raw_value) + " " + str(background.data[i].y.raw_value)
        return cif_background

    def cw_param_as_cif(self):
        '''
        Returns a CIF representation of the CW instrument parameters
        '''
        cif_ipar_data = ""
        cif_ipar_data += "\n_setup_wavelength " + str(self.job.parameters.wavelength.raw_value)
        cif_ipar_data += "\n_setup_offset_2theta  " + str(self.job.pattern.zero_shift.raw_value)
        cif_ipar_data += "\n"
        cif_ipar_data += "\n_pd_instr_resolution_u " + str(self.job.parameters.resolution_u.raw_value)
        cif_ipar_data += "\n_pd_instr_resolution_v " + str(self.job.parameters.resolution_v.raw_value)
        cif_ipar_data += "\n_pd_instr_resolution_w " + str(self.job.parameters.resolution_w.raw_value)
        cif_ipar_data += "\n_pd_instr_resolution_x " + str(self.job.parameters.resolution_x.raw_value)
        cif_ipar_data += "\n_pd_instr_resolution_y " + str(self.job.parameters.resolution_y.raw_value)
        cif_ipar_data += "\n"
        cif_ipar_data += "\n_pd_instr_reflex_asymmetry_p1 " + str(self.job.parameters.reflex_asymmetry_p1.raw_value)
        cif_ipar_data += "\n_pd_instr_reflex_asymmetry_p2 " + str(self.job.parameters.reflex_asymmetry_p2.raw_value)
        cif_ipar_data += "\n_pd_instr_reflex_asymmetry_p3 " + str(self.job.parameters.reflex_asymmetry_p3.raw_value)
        cif_ipar_data += "\n_pd_instr_reflex_asymmetry_p4 " + str(self.job.parameters.reflex_asymmetry_p4.raw_value)
        return cif_ipar_data

    def polar_param_as_cif(self):
        cif_pat_data = ""
        cif_pat_data += "\n_diffrn_radiation_polarization " + str(self.job.pattern.beam.polarization.raw_value)
        cif_pat_data += "\n_diffrn_radiation_efficiency " + str(self.job.pattern.efficiency.raw_value)
        cif_pat_data += "\n_setup_field " + str(self.job.pattern.field.raw_value)
        cif_pat_data += "\n_chi2_sum " + str(self._refine_sum)
        cif_pat_data += "\n_chi2_diff " + str(self._refine_diff)
        cif_pat_data += "\n_chi2_up " + str(self._refine_up)
        cif_pat_data += "\n_chi2_down " + str(self._refine_down)
        return cif_pat_data

    def tof_param_as_cif(self):
        '''
        Returns a CIF representation of the TOF instrument parameters
        '''
        cif_tof_data = ""
        cif_tof_data += "\n_tof_parameters_zero " + str(self.job.pattern.zero_shift.raw_value)
        cif_tof_data += "\n_tof_parameters_dtt1 " + str(self.job.parameters.dtt1.raw_value)
        cif_tof_data += "\n_tof_parameters_dtt2 " + str(self.job.parameters.dtt2.raw_value)
        cif_tof_data += "\n_tof_parameters_2theta_bank " + str(self.job.parameters.ttheta_bank.raw_value)
        cif_tof_data += "\n_tof_profile_sigma0 " + str(self.job.parameters.sigma0.raw_value)
        cif_tof_data += "\n_tof_profile_sigma1 " + str(self.job.parameters.sigma1.raw_value)
        cif_tof_data += "\n_tof_profile_sigma2 " + str(self.job.parameters.sigma2.raw_value)
        cif_tof_data += "\n_tof_profile_gamma0 " + str(self.job.parameters.gamma0.raw_value)
        cif_tof_data += "\n_tof_profile_gamma1 " + str(self.job.parameters.gamma1.raw_value)
        cif_tof_data += "\n_tof_profile_gamma2 " + str(self.job.parameters.gamma2.raw_value)
        cif_tof_data += "\n_tof_profile_alpha0 " + str(self.job.parameters.alpha0.raw_value)
        cif_tof_data += "\n_tof_profile_alpha1 " + str(self.job.parameters.alpha1.raw_value)
        cif_tof_data += "\n_tof_profile_beta0 " + str(self.job.parameters.beta0.raw_value)
        cif_tof_data += "\n_tof_profile_beta1 " + str(self.job.parameters.beta1.raw_value)
        return cif_tof_data
