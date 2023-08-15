// SPDX-FileCopyrightText: 2022 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021-2022 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements

import Gui.Globals as Globals


EaElements.GroupRow {

    EaElements.ParamComboBox {
        parameter: Globals.Proxies.experimentMainParam('_diffrn_radiation_probe')
        onActivated: Globals.Proxies.setExperimentMainParamWithFullUpdate(parameter, 'value', currentText)
    }

    EaElements.ParamTextField {
        parameter: Globals.Proxies.experimentMainParam('_diffrn_radiation_wavelength')
        onEditingFinished: Globals.Proxies.setExperimentMainParam(parameter, 'value', Number(text))
        fitCheckBox.onToggled: Globals.Proxies.setExperimentMainParam(parameter, 'fit', fitCheckBox.checked)
    }

}
