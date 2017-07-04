#!/usr/bin/env python
# coding: utf8

import csv
import os
import sys

import gensim
from gensim import corpora

import annoy
from slugify import slugify


def init_distances():
    """ Initialize distance calculater """

    try:
        sys.argv[2]
    except IndexError:
        print("Tool needs an argument - second argument (search query) non existent.")
        sys.exit()

    query = sys.argv[2]
    slug = slugify(query)

    base_path = os.path.abspath(
        os.path.dirname(
            sys.modules['__main__'].__file__
        )
    )

    train_folder = base_path + "/data//models/" + slug + "/trained/"
    doc_path = base_path + "/data/csv/" + slug + "/content.csv"

    print("")
    print("Method: Spotify Annoy")

    # Load our matrix market representation of lsi vectors
    matrix_market = gensim.corpora.MmCorpus(
        gensim.utils.smart_open(
            train_folder + "lsi-vectors.mm"
        )
    )

    # set max features and docs, you may tune here
    num_features, num_docs = matrix_market.num_terms, matrix_market.num_docs

    # Create annoy index
    index_annoy = annoy.AnnoyIndex(
        num_features,
        metric='angular'
    )

    # Load trained annoy model
    index_annoy.load(train_folder + 'annoy.model')

    # get all docnames/idents
    articles = []

    with open(doc_path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            articles.append(row[0])

    # Compare between input docs - for evaluation
    # could be used to build a simple similarity database, /product database
    for i, doc in enumerate(articles):

        print("Distance between '" + articles[i] + "' and ...")
        print()

        for j, docj in enumerate(articles):
            if j == i:
                pass

            print(
                "   ... '" +
                articles[j] +
                "': " +
                str(index_annoy.get_distance(i, j))
            )

        print()

    print("\nNotice: the smaller the number, the similar are both urls")
