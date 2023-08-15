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
        parameter: Globals.Proxies.modelMainParam('_cell_length_a')
        onEditingFinished: Globals.Proxies.setModelMainParam(parameter, 'value', Number(text))
        fitCheckBox.onToggled: Globals.Proxies.setModelMainParam(parameter, 'fit', fitCheckBox.checked)
    }

    EaElements.ParamTextField {
        parameter: Globals.Proxies.modelMainParam('_cell_length_b')
        onEditingFinished: Globals.Proxies.setModelMainParam(parameter, 'value', Number(text))
        fitCheckBox.onToggled: Globals.Proxies.setModelMainParam(parameter, 'fit', fitCheckBox.checked)
    }

    EaElements.ParamTextField {
        parameter: Globals.Proxies.modelMainParam('_cell_length_c')
        onEditingFinished: Globals.Proxies.setModelMainParam(parameter, 'value', Number(text))
        fitCheckBox.onToggled: Globals.Proxies.setModelMainParam(parameter, 'fit', fitCheckBox.checked)
    }

    EaElements.ParamTextField {
        parameter: Globals.Proxies.modelMainParam('_cell_angle_alpha')
        onEditingFinished: Globals.Proxies.setModelMainParam(parameter, 'value', Number(text))
        fitCheckBox.onToggled: Globals.Proxies.setModelMainParam(parameter, 'fit', fitCheckBox.checked)
    }

    EaElements.ParamTextField {
        parameter: Globals.Proxies.modelMainParam('_cell_angle_beta')
        onEditingFinished: Globals.Proxies.setModelMainParam(parameter, 'value', Number(text))
        fitCheckBox.onToggled: Globals.Proxies.setModelMainParam(parameter, 'fit', fitCheckBox.checked)
    }

    EaElements.ParamTextField {
        parameter: Globals.Proxies.modelMainParam('_cell_angle_gamma')
        onEditingFinished: Globals.Proxies.setModelMainParam(parameter, 'value', Number(text))
        fitCheckBox.onToggled: Globals.Proxies.setModelMainParam(parameter, 'fit', fitCheckBox.checked)
    }

}
