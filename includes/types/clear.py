#!/usr/bin/env python
# coding: utf8

import os
import sys


def init_clear():

    base_path = os.path.abspath(os.path.dirname(sys.modules['__main__'].__file__))
    save_path_models = base_path + "/data/models/"
    train_folder = base_path + "/data/csv/"

    for root, dirs, files in os.walk(save_path_models, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))

    for root, dirs, files in os.walk(train_folder, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
