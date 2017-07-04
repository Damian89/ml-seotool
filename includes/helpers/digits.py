#!/usr/bin/env python
# coding: utf8


def has_digits(token):
    """ Check if token contains any digit """

    for char in token:
        if char.isdigit():
            return True

    return False
