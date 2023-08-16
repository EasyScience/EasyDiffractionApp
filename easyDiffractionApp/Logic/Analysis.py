# SPDX-FileCopyrightText: 2023 EasyDiffraction contributors
# SPDX-License-Identifier: BSD-3-Clause
# © © 2023 Contributors to the EasyDiffraction project <https://github.com/easyscience/EasyDiffractionApp>

from PySide6.QtCore import QObject, Signal, Slot, Property

from EasyApp.Logic.Logging import console
from Logic.Helpers import IO


class Analysis(QObject):
    definedChanged = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self._proxy = parent
        self._defined = False

    # QML accessible properties

    @Property(bool, notify=definedChanged)
    def defined(self):
        return self._defined

    @defined.setter
    def defined(self, newValue):
        if self._defined == newValue:
            return
        self._defined = newValue
        console.debug(IO.formatMsg('main', f'Analysis defined: {newValue}'))
        self.definedChanged.emit()

    @Slot()
    def resetAll(self):
        self.defined = False
        console.debug("All analysis removed")
