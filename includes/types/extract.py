#!/usr/bin/env python
# coding: utf8

import csv
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
import re
#from tidylib import tidy_document

from bs4 import BeautifulSoup, Comment

from slugify import slugify

csv.field_size_limit(sys.maxsize)

def get_site_content(url):
    """ request url and get site content """

    req = urllib.request.Request(
        url,
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )

    response = urllib.request.urlopen(
        req,
        timeout=4
    )
    
    return response.read().decode("utf-8", "ignore")


def extract_content_from(html, area):
    """ Extract content with area from html document """

    if area[0] == '#':
        areatype = 'id'
        areaname = area[1:]

    if area[0] == '.':
        areatype = 'class'
        areaname = area[1:]

    if area[0] != '.' and area[0] != '#':
        areatype = 'element'
        areaname = area

    """ tidy html, but makes problems with html5 """
    #html, errors = tidy_document(html,options={'numeric-entities':1})

    parsed_html = BeautifulSoup(html, 'html.parser', from_encoding="utf-8")

    # remove all javascript, stylesheet code, some elements
    for script in parsed_html(["script", "style", "semantics", "code", "head", "nav"]):
        script.extract()

    for element in parsed_html(text=lambda text: isinstance(text, Comment)):
        element.extract()

    if areatype == 'id':
        html = str(parsed_html.find(id=areaname))

    if areatype == 'class':
        html = str(parsed_html.find(class_=areaname))

    if areatype == 'element':
        html = str(parsed_html.find(areaname))

    html = re.sub('<[^<]+?>', ' ', html)
    html = re.sub('<[^<]+-->', ' ', html)
    html = re.sub('"', '', html)
    html = html.strip()
    html = re.sub(r"\s\s+", " ", html)

    return html


def is_english(content):
    """ Simple check if english content found """

    points = 0

    if content.count(" of ") > 4:
        points += 1

    if content.count(" and ") > 4:
        points += 1

    if content.count(" are ") > 4:
        points += 1

    if content.count(" is ") > 4:
        points += 1

    if content.count(" to ") > 4:
        points += 1

    if points >= 3:
        return True

    return False


def is_unknown_language(content):
    """ Simple check if language is known == german """

    points = 0

    if content.count(" und ") > 1:
        points += 1

    if content.count(" oder ") > 0:
        points += 1

    if content.count(" von ") > 0:
        points += 1

    if content.count(" es ") > 0:
        points += 1

    if content.count(" für ") > 0:
        points += 1

    if points >= 2:
        return False

    return True


def extract_content_from_urls(urllist_file, newurllist_file, contentfile, max_links=100, min_content_length=650):
    """ Extracts text from an url """

    write_file = open(contentfile, 'w')
    write_url_file = open(newurllist_file, 'w')

    with open(urllist_file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        current_link = 0
        links_skipped = 0
        for row in reader:

            if current_link > max_links - 1:
                break

            link = row[0]
            area = row[1]

            print("Currently: " + link)

            # try to extract the content of every link based on give class, id or simple element (div, body, ...)
            try:

                # simple http get request
                html = get_site_content(link)

                # content extraction using bs4
                content = extract_content_from(html, area)

                if len(content) < min_content_length:
                    print("INFO: Link skipped because content length.")
                    links_skipped += 1
                    continue

                if is_english(content):
                    print("INFO: Link skipped because its english!")
                    links_skipped += 1
                    continue

                if is_unknown_language(content):
                    print("INFO: Link skipped because not german.")
                    links_skipped += 1
                    continue

                # extract function uses bs4, whoch returns "None" for empty/unsuccessful results
                # skip those
                if content != "None":
                    write_file.write('"' + link + '","' + content + '"' + "\n")
                    write_url_file.write(
                        '"' + link + '","' + area + '"' + "\n")
                    current_link += 1
                else:
                    print("INFO: Content is 'None'")
                    links_skipped += 1

            except Exception as err:
                print("ERROR: " + str(err) + " (Link skipped)")
                links_skipped += 1

    print("Successfully scraped " + str(current_link) +
          " links - skipped " + str(links_skipped) + " links")
    write_file.close()
    write_url_file.close()


def init_extract():
    """ Initialize content extraction """

    try:
        sys.argv[2]
    except IndexError:
        print("Tool needs an argument - second argument (search query) non existent.")
        sys.exit()

    query = sys.argv[2]
    slug = slugify(query)

    base_path = os.path.abspath(
        os.path.dirname(sys.modules['__main__'].__file__))
    save_path = base_path + "/data/csv/" + slug + "/"

    file_to_load = save_path + "google-urls.csv"
    file_to_save_content = save_path + "content.csv"
    file_to_save_used_urls = save_path + "used-urls.csv"

    if os.path.exists(file_to_save_content):
        os.remove(file_to_save_content)

    if os.path.exists(file_to_save_used_urls):
        os.remove(file_to_save_used_urls)

    max_links = sys.argv[3] if len(sys.argv) >= 4 else 100
    min_length = sys.argv[4] if len(sys.argv) >= 5 else 650

    max_links = int(max_links)
    min_length = int(min_length)

    extract_content_from_urls(
        file_to_load, file_to_save_used_urls, file_to_save_content, max_links, min_length)
