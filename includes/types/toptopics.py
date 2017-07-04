#!/usr/bin/env python
# coding: utf8


import os
import pickle
import sys

from gensim import corpora, models

from slugify import slugify


def print_top_words(model, feature_names, n_top_words):
    """ Print top topics for sk learn algos """

    for topic_idx, topic in enumerate(model.components_):

        print("Topic #%d:" % topic_idx)

        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))

    print("")


def init_toptopic():
    """ Initialize top topic extraction using different methods """

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

    save_path_models = base_path + "/data/models/" + slug + "/dict/"
    train_folder = base_path + "/data/models/" + slug + "/trained/"

    # basic file checks
    if os.path.exists(save_path_models + "dictionary.dict") is False:
        print("dictionary.dict not found - run prepare_dict_corpus.py first")
        sys.exit()

    if os.path.exists(save_path_models + "corpus.mm") is False:
        print("corpus.mm not found - run prepare_dict_corpus.py first")
        sys.exit()

    # load our corpus created in "prepare.py"
    corpus = corpora.MmCorpus(save_path_models + "corpus.mm")

    print("Extrahierte Themenkomplexe:")
    print("Methode: Hierarchical Dirichlet Process")

    # load hdp model (created in "train.py")
    model = models.HdpModel.load(train_folder + "hdpmodel.model")

    all_topics = model.print_topics(
        num_topics=10,
        num_words=4
    )

    for doc_topics in all_topics:
        print(doc_topics[1])

    print("")
    print("Methode: TFIDF + Latent Semantic Indexing")

    # load lsi model (created in "train.py")
    model = models.LsiModel.load(train_folder + "tfidf-lsi.model")

    all_topics = model.print_topics(
        num_topics=10,
        num_words=4
    )

    for doc_topics in all_topics:
        print(doc_topics[1])

    print("")
    print("Methode: Latent Dirichlet Allocation")

    # load lda model (created in "train.py")
    model = models.LdaModel.load(train_folder + "lda.model")

    top_topics = model.top_topics(
        corpus,
        5
    )

    extracted_top_topics = []

    for i, topic in top_topics:
        for value, name in i:
            if value > 0.001:
                extracted_top_topics.append([value, name])

    extracted_top_topics = sorted(extracted_top_topics, reverse=True)

    parsed_items = []
    skipped_items = 0
    for value, name in extracted_top_topics:
        if name in parsed_items:
            skipped_items += 1
            continue

        print(str(value)[:8] + " " + name)
        parsed_items.append(name)

    print(
        "Skipped " +
        str(skipped_items) +
        " items (duplicated with smaller value)"
    )

    # load sklearns tfidf vectorizer created in "prepare.py"
    tfidf_vectorizer = pickle.load(
        open(
            save_path_models + "tfidf-vectorizer.sk", "rb"
        )
    )

    # get feature names
    tf_feature_names = tfidf_vectorizer.get_feature_names()

    print()
    print("Methode: TFIDF + LDA")

    # load sk learn lda model and print 4 toptopic combinations
    lda = pickle.load(
        open(
            train_folder + "tfidf-lda.model", "rb"
        )
    )

    print_top_words(
        lda,
        tf_feature_names,
        5
    )

    print()
    print("Methode: TFIDF + NMF")

    # load sk learn nmf model and print 4 toptopic combinations
    nmf = pickle.load(
        open(
            train_folder + "tfidf-nmf.model", "rb"
        )
    )

    print_top_words(
        nmf,
        tf_feature_names,
        5
    )
