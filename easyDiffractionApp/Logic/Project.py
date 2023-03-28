# SPDX-FileCopyrightText: 2023 easyDiffraction contributors <support@easydiffraction.org>
# SPDX-License-Identifier: BSD-3-Clause
# © 2021-2023 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

# noqa: E501
import os
import datetime
from timeit import default_timer as timer
import json

from PySide2.QtCore import Signal, QObject

from easyCore.Datasets.xarray import np
from easyCore.Utils.io.xml import XMLSerializer
from easyDiffractionLib.sample import Sample
from easyApp.Logic.Utils.Utils import generalizePath


class ProjectLogic(QObject):
    """
    """
    projectCreatedChanged = Signal()
    projectInfoChanged = Signal()
    reset = Signal()
    phasesAsObjChanged = Signal()
    structureParametersChanged = Signal()
    experimentDataAdded = Signal()
    experimentLoadedChanged = Signal()

    def __init__(self, parent=None , interface=None):
        super().__init__(parent)
        self.parent = parent
        self._interface = interface
        self._interface_name = interface.current_interface_name
        self.project_save_filepath = ""
        self.project_load_filepath = ""
        self._project_info = self._defaultProjectInfo()
        self._project_created = False
        self._state_changed = False
        self._read_only = False

        self._report = ""
        self._currentProjectPath = os.path.join(os.path.expanduser("~"), 'TestProject')

    ####################################################################################################################
    ####################################################################################################################
    # Reporting
    ####################################################################################################################
    ####################################################################################################################

    def setReport(self, report):
        """
        Keep the QML generated HTML report for saving
        """
        self._report = report

    def saveReport(self, filepath):
        """
        Save the generated report to the specified file
        Currently only html
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(self._report)
            success = True
        except IOError:
            success = False
        return success

    def setProjectCreated(self, created: bool):
        if self._project_created == created:
            return
        self._project_created = created
        self.projectCreatedChanged.emit()

    ####################################################################################################################
    ####################################################################################################################
    # project
    ####################################################################################################################
    ####################################################################################################################

    def _defaultProjectInfo(self):
        return dict(
            name="Example Project",
            short_description="diffraction, powder, 1D",
            samples="Not loaded",
            experiments="Not loaded",
            modified=datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
        )

    def projectExamplesAsXml(self):
        model = { "item": [
            {"name": "PbSO4", "description": "neutrons, powder, constant wavelength, D1A@ILL",
             "path": "../Resources/Examples/PbSO4/project.json"},
            {"name": "Co2SiO4", "description": "neutrons, powder, constant wavelength, D20@ILL",
             "path": "../Resources/Examples/Co2SiO4/project.json"},
            {"name": "Dy3Al5O12", "description": "neutrons, powder, constant wavelength, G41@LLB",
             "path": "../Resources/Examples/Dy3Al5O12/project.json"},
            {"name": "CeCuAl3", "description": "neutrons, powder, time-of-flight, Polaris@ISIS",
             "path": "../Resources/Examples/CeCuAl3/project.json"},
            {"name": "Na2Ca3Al2F14", "description": "neutrons, powder, time-of-flight, Osiris@ISIS",
             "path": "../Resources/Examples/Na2Ca3Al2F14/project.json"},
            {"name": "Si3N4", "description": "neutrons, powder, constant wavelength, multi-phase, 3T2@LLB",
             "path": "../Resources/Examples/Si3N4/project.json"},
            {"name": "Fe3O4", "description": "neutrons, powder, constant wavelength, polarised, 6T2@LLB",
             "path": "../Resources/Examples/Fe3O4/project.json"},
            {"name": "Ho2Ti2O7", "description": "neutrons, powder, constant wavelength, polarised, VIP@LLB",
             "path": "../Resources/Examples/Ho2Ti2O7/project.json"},
            # disbaled until the new Cryspy is available.
            # {"name": "La0.5Ba0.5CoO3", "description": "neutrons, powder, constant wavelength, HRPT@PSI",
            #  "path": "../Resources/Examples/La0.5Ba0.5CoO3/project.json"}
        ]}
        # XMLSerializer doesn't currently handle lists.
        xml = XMLSerializer().encode(model, data_only=True)
        return xml

    def projectInfoAsCif(self):
        cif_list = []
        for key, value in self._project_info.items():
            if ' ' in value:
                value = f"'{value}'"
            cif_list.append(f'_{key} {value}')
        cif_str = '\n'.join(cif_list)
        return cif_str

    def projectInfoAsJson(self, json_str):
        self._project_info = json.loads(json_str)

    def editProjectInfo(self, key, value):
        if key == 'location':
            self._currentProjectPath = value
            return
        else:
            if self._project_info[key] == value:
                return
            self._project_info[key] = value

    def currentProjectPath(self, new_path):
        if self._currentProjectPath == new_path:
            return
        self._currentProjectPath = new_path

    def createProject(self):
        projectPath = self._currentProjectPath
        mainCif = os.path.join(projectPath, 'project.cif')
        samplesPath = os.path.join(projectPath, 'samples')
        experimentsPath = os.path.join(projectPath, 'experiments')
        calculationsPath = os.path.join(projectPath, 'calculations')
        if not os.path.exists(projectPath):
            os.makedirs(projectPath)
            os.makedirs(samplesPath)
            os.makedirs(experimentsPath)
            os.makedirs(calculationsPath)
            with open(mainCif, 'w') as file:
                file.write(self.projectInfoAsCif())
        else:
            print(f"ERROR: Directory {projectPath} already exists")

    def stateHasChanged(self, changed: bool):
        if self._state_changed == changed:
            return
        self._state_changed = changed

    def _loadProjectAs(self, filepath):
        """
        """
        self.project_load_filepath = filepath
        print("LoadProjectAs " + filepath)
        self._loadProject()

    def _loadProject(self):
        """
        """
        start_time = timer()
        path = generalizePath(self.project_load_filepath)
        if not os.path.isfile(path):
            print("Failed to find project: '{0}'".format(path))
            return
        with open(path, 'r') as xml_file:
            descr: dict = json.load(xml_file)

        interface_name = descr.get('interface', None)
        if interface_name is not None:
            old_interface_name = self._interface.current_interface_name
            if old_interface_name != interface_name:
                self._interface.switch(interface_name)

        descr['sample']['interface'] = self._interface
        sample_descr = Sample.from_dict(descr['sample'])

        self.parent.assignToSample(sample_descr)

        # project info
        self._project_info = descr['project_info']

        # read only flag
        self._read_only = descr['read_only']

        # experiment
        if 'experiments' in descr:
            data = descr['experiments']
            exp_name = descr['project_info']['experiments']

            self.parent.sendToExperiment(data, exp_name)
        else:
            # delete existing experiment
            self.parent.removeExperiment(skipped=descr['experiment_skipped'])

        new_minimizer_settings = descr.get('minimizer', None)
        if new_minimizer_settings is not None:
            new_engine = new_minimizer_settings['engine']
            new_method = new_minimizer_settings['method']
            self.parent.setNewEngine(engine=new_engine, method=new_method)

        self.parent.setSampleOnFitter()

        # tell the LC that the stack needs resetting
        self.parent.resetStack()

        self.setProjectCreated(True)
        print("\nProject loading time: {0:.3f} s\n".format(timer() - start_time))

    def saveProject(self):
        """
        """
        projectPath = self._currentProjectPath
        project_save_filepath = os.path.join(projectPath, 'project.json')
        descr = {
            'sample': self.parent.getSampleAsDict()
        }
        if not self.parent.isExperimentSkipped():
            descr['experiments'] = self.parent.getExperiments()

        descr['experiment_skipped'] = self.parent.isExperimentSkipped()
        descr['read_only'] = self._read_only
        descr['project_info'] = self._project_info

        descr['interface'] = self._interface.current_interface_name

        descr['minimizer'] = self.parent.fittingNamesDict()

        content_json = json.dumps(descr, indent=4, default=self.default)

        path = generalizePath(project_save_filepath)
        createFile(path, content_json)
        self.stateHasChanged(False)

    def default(self, obj):
        if type(obj).__module__ == np.__name__:
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            else:
                return obj.item()
        raise TypeError('Unknown type:', type(obj))

    def resetState(self):
        self._project_info = self._defaultProjectInfo()
        self.setProjectCreated(False)
        self.projectInfoChanged.emit()
        self.project_save_filepath = ""
        self.parent.resetState()

    def updateProjectInfo(self, key_value):
        if len(key_value) == 2:
            self._project_info[key_value[0]] = key_value[1]
            self.projectInfoChanged.emit()

    def statusModelAsObj(self):
        return self.parent.statusModelAsObj()

    def statusModelAsXml(self):
        return self.parent.statusModelAsXml()

def createFile(path, content):
    if os.path.exists(path):
        print(f'File already exists {path}. Overwriting...')
        os.unlink(path)
    try:
        message = f'create file {path}'
        with open(path, "w") as file:
            file.write(content)
    except Exception as exception:
        print(message, exception)
