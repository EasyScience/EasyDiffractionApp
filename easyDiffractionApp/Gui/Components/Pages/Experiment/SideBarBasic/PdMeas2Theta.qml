// SPDX-FileCopyrightText: 2022 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021-2022 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements

import Gui.Globals as Globals


EaElements.GroupRow {

    EaElements.ParamTextField {
        enabled: false
        parameter: Globals.Proxies.experimentMainParam('_pd_meas_2theta_range_min')
    }

    EaElements.ParamTextField {
        enabled: false
        parameter: Globals.Proxies.experimentMainParam('_pd_meas_2theta_range_max')
    }

    EaElements.ParamTextField {
        enabled: false
        parameter: Globals.Proxies.experimentMainParam('_pd_meas_2theta_range_inc')
    }

    EaElements.ParamTextField {
        parameter: Globals.Proxies.experimentMainParam('_pd_meas_2theta_offset')
        onEditingFinished: Globals.Proxies.setExperimentMainParam(parameter, 'value', Number(text))
        fitCheckBox.onToggled: Globals.Proxies.setExperimentMainParam(parameter, 'fit', fitCheckBox.checked)
    }

}
