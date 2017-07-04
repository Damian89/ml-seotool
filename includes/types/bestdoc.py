#!/usr/bin/env python
# coding: utf8

import csv
import os
import re
import sys

import gensim
from gensim import corpora, models, similarities

import annoy
from slugify import slugify


def make_best_doc(search, model, corpus, dictionary, docfile, docrating):
    """ 
    Since the path to the best docs within corpus is always the same
    for gensim models, we can write this down and use multiple times
    """

    # make search lower
    search = search.lower()

    # remove everything except [a-z0-9]
    # TODO: didnt test umlaute, ...
    search = re.sub(r'[^a-z0-9 ]+', '', search)

    # make sim index on corpus with model
    index = similarities.MatrixSimilarity(model[corpus])

    # vectorize search
    vec_bow = dictionary.doc2bow(search.split())

    # convert the query to model space
    vec_lsi = model[vec_bow]

    # perform a similarity query against the corpus
    sims = index[vec_lsi]

    # sort
    sims = sorted(enumerate(sims), key=lambda item: -item[1])

    # get all docnames/idents
    articles = []

    with open(docfile, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            articles.append(row[0])

    # show similarities
    for i, (doc, cs) in enumerate(sims):
        articlename = articles[doc].rstrip()
        rating = str(cs) + " " + articlename
        print(rating)

        if articlename in docrating:
            docrating[articlename] += cs
        else:
            docrating[articlename] = cs

    return docrating


def init_bestdoc():
    """ Initialize best doc search """

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

    save_path_models = base_path + "/data//models/" + slug + "/dict/"
    train_folder = base_path + "/data//models/" + slug + "/trained/"
    doc_path = base_path + "/data/csv/" + slug + "/content.csv"

    # basic file checks
    if os.path.exists(save_path_models + "dictionary.dict") is False:
        print("dictionary.dict not found - run prepare_dict_corpus.py first")
        sys.exit()

    if os.path.exists(save_path_models + "corpus.mm") is False:
        print("corpus.mm not found - run prepare_dict_corpus.py first")
        sys.exit()

    dictionary = corpora.Dictionary.load(save_path_models + "dictionary.dict")
    corpus = corpora.MmCorpus(save_path_models + "corpus.mm")

    # No commenting necessary - its always loading the model
    # and get the top docs based on query and model

    print("Extracted topics and topic complexes:")
    print("Method: Hierarchical Dirichlet Process")
    model = models.HdpModel.load(train_folder + "hdpmodel.model")

    sumrating = make_best_doc(
        query,
        model,
        corpus,
        dictionary,
        doc_path,
        {}
    )

    print("")
    print("Method: TFIDF + Latent Semantic Indexing")
    model = models.LsiModel.load(train_folder + "tfidf-lsi.model")

    sumrating = make_best_doc(
        query,
        model,
        corpus,
        dictionary,
        doc_path,
        sumrating
    )

    print("")
    print("Method: Latent Dirichlet Allocation")
    model = models.LdaModel.load(train_folder + "lda.model")

    sumrating = make_best_doc(
        query,
        model,
        corpus,
        dictionary,
        doc_path,
        sumrating
    )

    # Spotify Annoy is a litte more complex

    # Get number of lines based on document count
    num_lines = sum(1 for line in open(doc_path))

    print("")
    print("Method: Spotify Annoy")

    # Load lsi model
    lsi = gensim.models.LsiModel.load(train_folder + "lsi.model")

    # Load matric market
    matrix_market = gensim.corpora.MmCorpus(
        gensim.utils.smart_open(
            train_folder + "lsi-vectors.mm"
        )
    )

    # get featues and max docs
    # we dont need num_docs currently, but you may tune the output here
    num_features, num_docs = matrix_market.num_terms, matrix_market.num_docs

    # Load gensim similarity
    index_gensim = gensim.similarities.Similarity.load(
        train_folder + "sim_prefix_gensim"
    )

    # Create empty annoy index
    index_annoy = annoy.AnnoyIndex(
        num_features,
        metric='angular'
    )

    # Load created annoy model
    index_annoy.load(train_folder + 'annoy.model')

    # Transform search to lsi vecor
    vec_bow = dictionary.doc2bow(query.lower().split())
    vec_lsi = lsi[vec_bow]

    # We need this to get the article url/name - vectors tend to be hard to read/interpret
    sims = index_gensim[vec_lsi]

    sims = index_annoy.get_nns_by_vector(
        list(
            gensim.matutils.sparse2full(
                vec_lsi,
                num_features
            ).astype(float)
        ), num_lines
    )

    # Read all documents in list
    articles = []
    with open(doc_path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            articles.append(row[0])

    # Return finally our best content based on annoy
    for i, sim in enumerate(sims):
        articlename = articles[sim].rstrip()
        print(articlename)
        sumrating[articlename] -= i / 100

    # This is a kind of "summary" based on all models
    # Keep in mind this is a very simple overview
    # Always read the details for every model above
    # Eventually the results are not that good and you need to retrain your model
    print("")
    print("SUMMARY: the higher the count, the better")
    sumrating = sorted(sumrating.items(), key=lambda sumrating: -sumrating[1])
    for ratingdata in sumrating:
        rating = str(ratingdata[1])
        url = ratingdata[0]
        print(rating + " " + url)
