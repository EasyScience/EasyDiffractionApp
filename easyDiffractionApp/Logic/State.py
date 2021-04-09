# noqa: E501
import os
import sys
import numpy as np

from dicttoxml import dicttoxml
import xmltodict
from xml.dom.minidom import parseString
import json

from easyAppLogic.Utils.Utils import generalizePath
from easyDiffractionApp.Logic.DataStore import DataSet1D, DataStore


class State(object):
    """
    """
    def __init__(self, parent=None, interface_name=""):
        self.parent = parent
        self.interface_name = interface_name
        self.project_save_filepath = ""
        self.project_load_filepath = ""
        self.experiment_data = None
        self._experiment_data = None
        self.experiments = self._defaultExperiments()
        self._parameters = None
        self._instrument_parameters = None
        self._status_model = None

        self.phases = None
        self._data = self._defaultData()