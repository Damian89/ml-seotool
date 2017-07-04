#!/usr/bin/env python
# coding: utf8

import os
import sys
import urllib.error
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup

from slugify import slugify


def scrape(query):
    """ Scrapes google.de and returns the content """

    try:
        # current google serps url
        googleurl = "https://www.google.de/search?oe=utf-8&pws=0&complete=0&hl=de&num=100&q=" + \
            urllib.parse.quote_plus(query)

        # request method and header
        req = urllib.request.Request(
            googleurl,
            data=None,
            headers={
                'Accept-Language': "de_DE",
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            }
        )

        # send request
        response = urllib.request.urlopen(req)

        # return content
        return response.read()
    except Exception:
        print("Scraping failed.")
        sys.exit()

def extract_links_from_google(google_content, savefile, options):
    """ Extract every link from the google response/html for a given query search """

    # use bs4 for html parsing
    soup_instance = BeautifulSoup(google_content, 'html.parser')

    # temp save for already parsed links
    parsed_links = []

    # save links in this file
    linklist = open(savefile, 'a')

    for link in soup_instance.find_all('a'):
        link = str(link.get('href'))

        # if link was already parsed
        if link in parsed_links:
            continue

        # only accept links which begin with http (or https)
        if link.startswith("http") is False:
            continue

        # skip every link with google in it
        if "google" in link:
            continue

        # skip also youtube links
        if "youtube.com" in link:
            continue

        # blogger.com links are also not that helpful
        if "blogger.com" in link:
            continue

        # we dont need links with anchors in it
        if "#" in link:
            continue

        # skip pdf
        if ".pdf" in link:
            continue

        # skip worddocs
        if ".docx" in link:
            continue

        # skip links that look like boards/forums
        if "skip-forums" in options and (
                "forum" in link or
                "community" in link or
                "board" in link or
                "thread" in link
        ):
            continue

        # skip links which contain .ru
        if "skip-ru-links" in options and ".ru" in link:
            continue

        # skip translation sites
        if "skip-translate" in options and (
                "translate" in link or
                "linguee" in link or
                "leo." in link or
                "pons." in link
        ):
            continue

        # temp save link in list
        parsed_links.append(link)

        # write link to file
        linklist.write('"' + link + '","body"\n')

    # close file
    linklist.close()


def init_scrape():
    """ Initializes scraping for a given query in german google serps """

    try:
        sys.argv[2]
    except IndexError:
        print("Tool needs an argument - second argument (search query) non existent.")
        sys.exit()

    # Raw query
    query = sys.argv[2]

    # Slugified query
    slug = slugify(query)

    app_base_path = os.path.abspath(
        os.path.dirname(sys.modules['__main__'].__file__))
    file_path = app_base_path + "/data/csv/" + slug + "/"

    if not os.path.exists(file_path):
        os.makedirs(file_path)

    file_to_save = file_path + "google-urls.csv"

    if os.path.exists(file_to_save):
        os.remove(file_to_save)

    google_content = scrape(query)

    options = [
        'skip-forums',
        'skip-ru-links',
        'skip-translate',
    ]

    extract_links_from_google(google_content, file_to_save, options)

    print("Scraping for '" + query + "' finished!")
