# SPDX-FileCopyrightText: 2023 easyDiffraction contributors <support@easydiffraction.org>
# SPDX-License-Identifier: BSD-3-Clause
# © 2021-2023 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>


import re

from PySide2.QtCore import Signal, QObject

from easyCore import np, borg
from easyCore.Utils.io.xml import XMLSerializer

from easyDiffractionLib import Phases, Phase, Lattice, Site, SpaceGroup
from easyCrystallography.Components.AtomicDisplacement import AtomicDisplacement
from easyCrystallography.Components.Susceptibility import MagneticSusceptibility
from easyCrystallography.Symmetry.tools import SpacegroupInfo
from easyApp.Logic.Utils.Utils import generalizePath


# noinspection PyUnresolvedReferences
class PhaseLogic(QObject):
    """
    """
    phaseAdded = Signal()
    updateProjectInfo = Signal(tuple)
    structureParametersChanged = Signal()
    phasesEnabled = Signal()
    phasesAsObjChanged = Signal()
    phasesReplaced = Signal()

    def __init__(self, parent=None, interface=None):
        super().__init__(parent)
        self.parent = parent
        self._interface = interface
        self.phases = Phases()
        self._phases_as_obj = []
        self._phases_as_xml = ""
        self._phases_as_cif = ""
        self._current_phase_index = 0
        self.has_msp = False
        # self.addDefaultPhase()

    ####################################################################################################################
    ####################################################################################################################
    # phases
    ####################################################################################################################
    ####################################################################################################################

    def currentPhaseIndex(self, new_index: int):
        if self._current_phase_index == new_index or new_index == -1:
            return False
        if len(self.phases) <= new_index:
            return False # no phase at this index
        self._current_phase_index = new_index
        return True

    def removeAllPhases(self):
        for name in self.phases.phase_names:
            del self.phases[name]
        self.structureParametersChanged.emit()
        self.phasesEnabled.emit()

    def removePhase(self, phase_name: str):
        if phase_name in self.phases.phase_names:
            del self.phases[phase_name]
            return True
        return False

    def addDefaultPhase(self):
        borg.stack.enabled = False
        default_phase = self._defaultPhase()
        r = re.compile('(.+[^0-9])\d*$')
        known_phases = [r.findall(s)[0] for s in self.phases.phase_names]  # Strip out any 1, 2, 3 etc we may have added
        if default_phase.name in known_phases:
            idx = known_phases.count(default_phase.name)
            default_phase.name = default_phase.name + str(idx)
        # print('Disabling scale')
        default_phase.scale.fixed = True
        self.phases.append(default_phase)
        borg.stack.enabled = True

    # @staticmethod
    def _defaultPhase(self):
        space_group = SpaceGroup('F d -3:2')
        cell = Lattice(5.0, 3.0, 4.0, 90, 90, 90)
        adp = AtomicDisplacement("Uiso")
        atom = Site(label='O', specie='O', fract_x=0.0, fract_y=0.0, fract_z=0.0, adp=adp, interface=self._interface)
        phase = Phase('Test', spacegroup=space_group, cell=cell, interface=self._interface)
        phase.add_atom(atom)
        return phase

    def _onPhaseAdded(self):
        self.phases.name = 'Phases'
        name = self.phases[self._current_phase_index].name
        self.updateProjectInfo.emit(('samples', name))
        self.parent.sample().interface = self._interface

    def currentCrystalSystem(self):
        phases = self.phases
        if not phases:
            return ''

        current_system = phases[self._current_phase_index].spacegroup.crystal_system  # noqa: E501
        current_system = current_system.capitalize()
        return current_system

    def setCurrentCrystalSystem(self, new_system: str):
        new_system = new_system.lower()
        space_group_numbers = SpacegroupInfo.get_ints_from_system(new_system)
        top_space_group_number = space_group_numbers[0]
        top_space_group_name = SpacegroupInfo.get_symbol_from_int_number(top_space_group_number)  # noqa: E501
        self._setCurrentSpaceGroup(top_space_group_name)

    def currentPhaseAsExtendedCif(self):
        if len(self.phases) == 0:
            return
        symm_ops = self.phases[self._current_phase_index].spacegroup.symmetry_ops
        symm_ops_cif_loop = "loop_\n _symmetry_equiv_pos_as_xyz\n"
        for symm_op in symm_ops:
            symm_ops_cif_loop += f' {symm_op.as_xyz_string()}\n'
        extended_cif = str(self.phases[self._current_phase_index].cif) + symm_ops_cif_loop
        return extended_cif

    def phasesAsCif(self, phases_as_cif):
        if self._phases_as_cif == phases_as_cif:
            return
        phases = Phases()
        for phase in Phases.from_cif_string(phases_as_cif):
            phases.append(phase)
        self.phases = phases

        self.parent.setPhasesOnSample(self.phases)
        self.updateParameters()

    def _setPhasesAsObj(self):
        self._phases_as_obj = self.phases.as_dict(skip=['interface', 'msp_values', 'Uiso_ani'])['data']
        self.parent.setCalculatedDataForPhase()
        # phase set - update xml so parameter table is also updated
        self.parent.emitParametersChanged()

    def _setPhasesAsXml(self):
        self._phases_as_xml = XMLSerializer().encode({"item":self._phases_as_obj}, skip=['interface'])

    def _setPhasesAsCif(self):
        self._phases_as_cif = str(self.phases.cif)

    def _setCurrentSpaceGroup(self, new_name: str):
        phases = self.phases
        if phases[self._current_phase_index].spacegroup.space_group_HM_name == new_name:  # noqa: E501
            return
        phases[self._current_phase_index].spacegroup.space_group_HM_name = new_name  # noqa: E501
        self._updateCalculatedData()

    def updateParameters(self):
        self.parent.parametersChanged.emit()
        self.parent.emitParametersChanged()

    def _spaceGroupSettingList(self):
        phases = self.phases
        if not phases:
            return []

        current_number = self._currentSpaceGroupNumber()
        settings = SpacegroupInfo.get_compatible_HM_from_int(current_number)
        return settings

    def _spaceGroupNumbers(self):
        current_system = self.currentCrystalSystem().lower()
        numbers = SpacegroupInfo.get_ints_from_system(current_system)
        return numbers

    def _currentSpaceGroupNumber(self):
        phases = self.phases
        current_number = phases[self._current_phase_index].spacegroup.int_number  # noqa: E501
        return current_number

    def getCurrentSpaceGroup(self):
        def space_group_index(number, numbers):
            if number in numbers:
                return numbers.index(number)
            return 0

        phases = self.phases
        if not phases:
            return -1

        space_group_numbers = self._spaceGroupNumbers()
        current_number = self._currentSpaceGroupNumber()
        current_idx = space_group_index(current_number, space_group_numbers)
        return current_idx

    def currentSpaceGroup(self, new_idx: int):
        space_group_numbers = self._spaceGroupNumbers()
        space_group_number = space_group_numbers[new_idx]
        space_group_name = SpacegroupInfo.get_symbol_from_int_number(space_group_number)  # noqa: E501
        self._setCurrentSpaceGroup(space_group_name)

    def formattedSpaceGroupList(self):
        def format_display(num):
            name = SpacegroupInfo.get_symbol_from_int_number(num)
            return f"<font color='#999'>{num}</font> {name}"

        space_group_numbers = self._spaceGroupNumbers()
        display_list = [format_display(num) for num in space_group_numbers]
        return display_list

    def crystalSystemList(self):
        systems = [system.capitalize() for system in SpacegroupInfo.get_all_systems()]  # noqa: E501
        return systems

    def formattedSpaceGroupSettingList(self):
        def format_display(num, name):
            return f"<font color='#999'>{num}</font> {name}"

        raw_list = self._spaceGroupSettingList()
        formatted_list = [format_display(i + 1, name) for i, name in enumerate(raw_list)]  # noqa: E501
        return formatted_list

    def currentSpaceGroupSetting(self):
        phases = self.phases
        if not phases:
            return 0

        settings = self._spaceGroupSettingList()
        current_setting = phases[self._current_phase_index].spacegroup.space_group_HM_name.raw_value  # noqa: E501
        for setting in settings:
            if current_setting in setting:
                return settings.index(setting)
        return 0

    def setCurrentSpaceGroupSetting(self, new_number: int):
        settings = self._spaceGroupSettingList()
        name = settings[new_number]
        self._setCurrentSpaceGroup(name)

    ####################################################################################################################
    # Phase: Atoms
    ####################################################################################################################
    def addDefaultAtom(self):
        index = len(self.phases[0].atoms.atom_labels) + 1
        label = f'Label{index}'
        adp = AtomicDisplacement("Uiso")
        atom = Site(label=label,
                    specie='Cl',
                    fract_x=0.5,
                    fract_y=0.5,
                    fract_z=0.5,
                    adp=adp)

        self.phases[self._current_phase_index].add_atom(atom)
        self.updateParameters()

    def removeAtom(self, atom_label: str):
        self.phases[self._current_phase_index].remove_atom(atom_label)
        self.updateParameters()

    def setCurrentExperimentDatasetName(self, name):
        if self.parent.experiments()[0].name == name:
            return
        self.parent.setExperimentName(name)
        self.updateProjectInfo.emit(('experiments', name))

    def addSampleFromCif(self, cif_url):
        file_list = cif_url.split(',')
        for cif_file in file_list:
            cif_path = generalizePath(cif_file)
            borg.stack.enabled = False
            phases = Phases.from_cif_file(cif_path)
            self.phases.interface = self._interface
            for phase in phases:
                phase.scale.fixed = True
                self.phases.append(phase)
                # see if MSP is present (or just default)
                msps = [hasattr(atom, 'msp') for atom in phase.atoms]  # noqa: E501
                self.has_msp = any(msps)
            self.phasesReplaced.emit()
            borg.stack.enabled = True

    def getCurrentPhaseName(self):
        return self.phases[self._current_phase_index].name

    def hasMsp(self):
        return self.has_msp

    def getAtom(self, index):
        return self.phases[self._current_phase_index].atoms[index]

    def setCurrentPhaseName(self, name):
        if self.phases[self._current_phase_index].name == name:
            return
        self.phases[self._current_phase_index].name = name
        # self._project_info['samples'] = name
        self.updateProjectInfo.emit(('samples', name))

    def samplesPresent(self):
        result = len(self.phases) > 0
        return result

    def _updateCalculatedData(self):
        self.parent.updateCalculatedData()
