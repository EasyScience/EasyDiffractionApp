// SPDX-FileCopyrightText: 2022 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2022 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents


Rectangle {
    visible: true
    width: 300
    height: 200

    EaElements.ParamTextField {
        anchors.centerIn: parent
        width: 100

        parameter: {'value': 10.378,
                    'error': 0.002,
                    'enabled': true,
                    'fittable': true,
                    'fit': true,
                    'name': '_cell_length_a',
                    'prettyName': 'length a',
                    'units': 'Å',
                    'url': 'https://google.com'}
    }
}
