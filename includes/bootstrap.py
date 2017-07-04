#!/usr/bin/env python
# coding: utf8

import sys

from includes.helpers.filesystem import filesystem as filesystem_mls
from includes.types.bestdoc import init_bestdoc
from includes.types.clear import init_clear
from includes.types.distances import init_distances
from includes.types.extract import init_extract
from includes.types.prepare import init_prepare
from includes.types.scrape import init_scrape
from includes.types.toptopics import init_toptopic
from includes.types.train import init_train


def main():
    """ Entry point for "ml-seotool" """

    try:
        sys.argv[1]
    except IndexError:
        print("Tool needs an argument - first argument (module/type) non existent.")
        sys.exit()

    filesystem_mls()

    tool_type = sys.argv[1]

    if tool_type == 'scrape':
        init_scrape()
    elif tool_type == 'extract':
        init_extract()
    elif tool_type == 'prepare':
        init_prepare()
    elif tool_type == 'train':
        init_train()
    elif tool_type == 'top-topics':
        init_toptopic()
    elif tool_type == 'best-doc':
        init_bestdoc()
    elif tool_type == 'distances':
        init_distances()
    elif tool_type == 'clear':
        init_clear()
