#!/usr/bin/env python
# coding: utf8

import os
import sys


def filesystem():
    """ Check if model and csv dir exists, if not create it. """

    base_path = os.path.abspath(os.path.dirname(sys.modules['__main__'].__file__))
    userdata_models = "/data/models"
    userdata_csvs = "/data/csv"

    if not os.path.exists(base_path+userdata_models):
        os.makedirs(base_path+userdata_models)

    if not os.path.exists(base_path+userdata_csvs):
        os.makedirs(base_path+userdata_csvs)
