#!/usr/bin/env python
# coding: utf8

import csv
import os
import pickle
import sys
from collections import defaultdict

from gensim import corpora
from nltk.tokenize import PunktSentenceTokenizer, RegexpTokenizer
from stop_words import get_stop_words

from sklearn.feature_extraction.text import TfidfVectorizer
from slugify import slugify

csv.field_size_limit(sys.maxsize)


def tokenize_content(file_to_content, stopword_list, token_min_length, token_min_count, max_docs):
    """ Tokenize content using different stoplists and tokenizers """

    """
    You may use sterms, but its not recommended unless you know what you are doing.
    Consider taking a look at the docs.
    """
    #from nltk.stem.porter import PorterStemmer
    #from nltk.stem.snowball import SnowballStemmer
    #p_stemmer = PorterStemmer()
    #s_stemmer = SnowballStemmer("german")

    terms = []
    # load input data and parse every line/text -> tokens
    with open(file_to_content, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        current_row = 0
        for row in reader:

            if current_row >= max_docs:
                break

            current_row += 1

            # makes content lowercase
            document = row[1].lower()

            # Split doc content into terms/words
            tokens = RegexpTokenizer('\w+').tokenize(document)

            # If you need stemmers, remove comments
            #tokens = [p_stemmer.stem(token) for token in tokens]
            #tokens = [s_stemmer.stem(token) for token in tokens]

            # include term only, when not in stopword_list
            tokens = [token for token in tokens if not token in stopword_list]

            # include term ony, when length bigger than min_length
            tokens = [
                token for token in tokens if len(token) > token_min_length
            ]

            # Exclude all links from within text
            tokens = [
                token for token in tokens if not token.startswith('http')
            ]

            # You can use this to remove digit-only terms
            #tokens = [token for token in tokens if not token.isdigit()]

            terms.append(tokens)

    frequency = defaultdict(int)

    for termgroup in terms:
        for term in termgroup:
            frequency[term] += 1

    return [[term for term in termgroups if frequency[term] >= token_min_count] for termgroups in terms]


def init_prepare():
    """ Initialize content preparation """

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

    save_path = base_path + "/data/csv/" + slug + "/"
    save_path_models = base_path + "/data//models/" + slug + "/dict/"
    statics_path = base_path + "/data/statics/"
    file_to_content = save_path + "content.csv"

    # create dict dir if not existent
    if not os.path.exists(save_path_models):
        os.makedirs(save_path_models)

    # load custom wordlist from file
    custom_stoplist = []

    with open(statics_path + "german-stopwords.txt", 'r') as csvfile:

        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        for row in reader:

            custom_stoplist.extend(row)

    slug_stoplist = []

    if os.path.exists(statics_path + slug + ".txt") is True:

        with open(statics_path + slug + ".txt", 'r') as csvfile:

            reader = csv.reader(csvfile, delimiter=',', quotechar='"')

            for row in reader:

                slug_stoplist.extend(row)
    else:
        print('No slug-specific stoplist found, creating...')

        os.mknod(statics_path + slug + ".txt")

        print(
            'You can add stopwords to ' +
            statics_path +
            slug +
            ".txt" + ', and rerun training!'
        )

    # load standard german stoplist
    de_stop = get_stop_words('de')

    # set min length for tokens/terms (aka "Wörter")
    token_min_length = sys.argv[3] if len(sys.argv) >= 4 else 3
    token_min_length = int(token_min_length)

    # set the min occurence count for a word
    token_min_count = sys.argv[4] if len(sys.argv) >= 5 else 1
    token_min_count = int(token_min_count)

    max_docs = sys.argv[5] if len(sys.argv) >= 6 else 100
    max_docs = int(max_docs)

    # concatenate stoplists
    stopword_list = de_stop + custom_stoplist + slug_stoplist

    """
    Part 1: Prepare input data/content for gensim ml algorithms
    """

    # get tokens/terms
    terms = tokenize_content(
        file_to_content=file_to_content,
        stopword_list=stopword_list,
        token_min_length=token_min_length,
        token_min_count=token_min_count,
        max_docs=max_docs
    )

    # create dictionary and save for future use
    dictionary = corpora.Dictionary(terms)
    dictionary.save(save_path_models + "dictionary.dict")

    # create corpus and save for future use
    corpus = [dictionary.doc2bow(term) for term in terms]
    corpora.MmCorpus.serialize(save_path_models + "corpus.mm", corpus)

    """
    Part 2: Prepare data/content for some sklearn ml algorithms
    """

    # use sklearns tfidf vecotrizer
    tfidf_vectorizer = TfidfVectorizer(
        max_df=0.95,
        min_df=token_min_count,
        max_features=100,
        stop_words=stopword_list,
        ngram_range=(1, 3),
        sublinear_tf=True,
        norm='l2'
    )

    # tokenize senctences using PunktSentenceTokenizer
    sentences = []

    with open(file_to_content, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        current_row = 0

        for row in reader:

            if current_row >= max_docs:
                break

            current_row += 1

            tokens = PunktSentenceTokenizer().tokenize(row[1])

            for sent in tokens:
                sentences.append(sent)

    # transform tokens into tf idf matric
    tfidf_tokens = tfidf_vectorizer.fit_transform(sentences)

    # save tokens for future use
    pickle.dump(tfidf_tokens, open(save_path_models + "tfidf-tokens.sk", "wb"))

    # save this vectorizer for future use
    pickle.dump(
        tfidf_vectorizer,
        open(
            save_path_models + "tfidf-vectorizer.sk", "wb"
        )
    )
