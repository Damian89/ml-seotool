#!/usr/bin/env python
# coding: utf8

import os
import sys


def init_clear():


    ignorelist = [
        '.gitkeep',
        '.gitignore'
    ]

    base_path = os.path.abspath(os.path.dirname(sys.modules['__main__'].__file__))
    save_path_models = base_path + "/data/models/"
    train_folder = base_path + "/data/csv/"
    stopword_folder = base_path + "/data/slug-stopwords/"

    for root, dirs, files in os.walk(save_path_models, topdown=False):
        for name in files:
            if name not in ignorelist:
                os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))

    for root, dirs, files in os.walk(train_folder, topdown=False):
        for name in files:
            if name not in ignorelist:
                os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))

    for root, dirs, files in os.walk(stopword_folder, topdown=False):
        for name in files:
            if name not in ignorelist:
                os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))