#!/usr/bin/env python
# coding: utf8

import itertools
import os
import pickle
import sys

import gensim
import numpy
from gensim import corpora, models

import annoy
from sklearn.decomposition import NMF, LatentDirichletAllocation
from slugify import slugify


def init_train():
    """ initialize training of content """

    try:
        sys.argv[2]
    except IndexError:
        print("Tool needs an argument - second argument (search query) non existent.")
        sys.exit()

    # max number of topics to use while training
    num_topics = sys.argv[3] if len(sys.argv) >= 4 else 40
    num_topics = int(num_topics)

    query = sys.argv[2]
    slug = slugify(query)

    base_path = os.path.abspath(
        os.path.dirname(
            sys.modules['__main__'].__file__
        )
    )

    save_path_models = base_path + "/data/models/" + slug + "/dict/"
    train_folder = base_path + "/data/models/" + slug + "/trained/"
    doc_path = base_path + "/data/csv/" + slug + "/content.csv"

    # if training folder does not exists, create it.
    if not os.path.exists(train_folder):
        os.makedirs(train_folder)

    # basic file checks
    if os.path.exists(save_path_models + "dictionary.dict") is False:
        print("dictionary.dict not found - run prepare_dict_corpus.py first")
        sys.exit()

    if os.path.exists(save_path_models + "corpus.mm") is False:
        print("corpus.mm not found - run prepare_dict_corpus.py first")
        sys.exit()

    # load dict and corpus (created in prepare.py)
    dictionary = corpora.Dictionary.load(save_path_models + "dictionary.dict")
    corpus = corpora.MmCorpus(save_path_models + "corpus.mm")

    # setting random seed to get the same results each time.
    numpy.random.seed(1)

    # train hdp model and save for future use
    model = models.HdpModel(
        corpus,
        id2word=dictionary
    )

    model.save(train_folder + "hdpmodel.model")

    # make tfidf corpus using gensim method and train lsi model
    # also save for future use
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]

    model = models.LsiModel(
        corpus_tfidf,
        id2word=dictionary,
        num_topics=num_topics
    )

    model.save(train_folder + "tfidf-lsi.model")

    # train lda model and save for future use
    model = models.LdaModel(
        corpus,
        id2word=dictionary,
        num_topics=num_topics
    )

    model.save(train_folder + "lda.model")

    # train lsi model and save for future use
    model = models.LsiModel(
        corpus,
        id2word=dictionary,
        num_topics=num_topics
    )

    model.save(train_folder + "lsi.model")

    # prepare spotify annoy training
    num_lines = sum(1 for line in open(doc_path))

    # we are using lsi to create matrix market format if corpus
    gensim.corpora.MmCorpus.serialize(
        train_folder + "lsi-vectors.mm",
        (gensim.matutils.unitvec(vec) for vec in model[corpus])
    )

    # reload matric market
    matric_market = gensim.corpora.MmCorpus(
        gensim.utils.smart_open(train_folder + "lsi-vectors.mm")
    )

    # extract max features and documents
    num_features, num_docs = matric_market.num_terms, matric_market.num_docs

    # create simple float32 array
    clipped = numpy.empty((num_docs, num_features), dtype=numpy.float32)

    for docno, doc in enumerate(itertools.islice(matric_market, num_docs)):
        clipped[docno] = gensim.matutils.sparse2full(doc, num_features)

    clipped_corpus = gensim.matutils.Dense2Corpus(
        clipped,
        documents_columns=False
    )

    # create similarity matrix based on clipped corpus
    index_gensim = gensim.similarities.Similarity(
        train_folder + "sim_prefix_gensim",
        clipped_corpus,
        num_best=num_lines,
        num_features=num_features
    )

    # save sim matric for future use
    index_gensim.save(train_folder + "sim_prefix_gensim")

    # load it instantly
    index_gensim = gensim.similarities.Similarity.load(
        train_folder + "sim_prefix_gensim"
    )

    # we want data for every line = url
    index_gensim.num_best = num_lines

    # create empty annoy index
    index_annoy = annoy.AnnoyIndex(num_features, metric='angular')

    # add vectors to index
    for i, vec in enumerate(clipped_corpus):
        index_annoy.add_item(
            i, list(gensim.matutils.sparse2full(vec, num_features).astype(float)))

    # build index
    index_annoy.build(10)

    # save index
    index_annoy.save(train_folder + 'annoy.model')

    # Lets train some sklearn algos -->

    # load tokens
    tfidf = pickle.load(open(save_path_models + "tfidf-tokens.sk", "rb"))

    # train non negative matrix factorization on tfidf matrix
    nmf = NMF(
        n_components=10,
        random_state=1,
        alpha=.1,
        l1_ratio=.5
    ).fit(tfidf)

    # train lda on tfidf matrix
    lda = LatentDirichletAllocation(
        n_topics=10,
        max_iter=5,
        learning_method='online',
        learning_offset=50.,
        random_state=0
    ).fit(tfidf)

    # save both models for future use
    pickle.dump(nmf, open(train_folder + "tfidf-nmf.model", "wb"))
    pickle.dump(lda, open(train_folder + "tfidf-lda.model", "wb"))
