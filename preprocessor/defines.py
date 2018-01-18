# -*- coding: utf-8 -*-
"""
preprocessor.constants
~~~~~~~~~~~~
This module includes the constant variables used in Preprocessor
"""
import regex
import sys
from .enum import enum

opts = {
    'URL':'urls',
    'MENTION':'mentions',
    'HASHTAG':'hashtags',
    'RESERVED':'reserved_words',
    'EMOJI':'emojis',
#    'SMILEY':'smileys',
#    'NUMBER': 'numbers',
    'ELLIPSIS': 'ellipsis',
    'REPETITION': 'repetition',
#    'PUNCTUATION': 'punctuation',
    'LOWERCASE': 'lowercase',
    'HTML_ENTITY': 'html_entities'
}
Options = enum(**opts)
Functions = enum('CLEAN', 'TOKENIZE', 'PARSE')


class Defines:
    PARSE_METHODS_PREFIX = 'parse_'
    FILTERED_METHODS = opts.values()
    PREPROCESS_METHODS_PREFIX = 'preprocess_'
    IS_PYTHON3 = sys.version_info > (3, 0, 0)
    PRIORITISED_METHODS = ['html_entities', 'reserved_words', 'urls', 'mentions', 'hashtags', 'ellipsis', 'emojis', 'smileys']


class Patterns:
    URL_PATTERN=regex.compile(r'\s*(?i)\b((?:https?:/{1,3}|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))*(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')
    HASHTAG_PATTERN = regex.compile(r'(#|＃)[\w_]*[\w][\w_]*')
    MENTION_PATTERN = regex.compile(r"@[a-zA-Z0-9_]*[a-zA-Z][a-zA-Z0-9_]*")
    RESERVED_WORDS_PATTERN = regex.compile(r"^(?:RT|rt)\s+(@[a-zA-Z0-9_]*[a-zA-Z][a-zA-Z0-9_]*):\s*(?=\s)") # FAV (favouriting) is deprecated by Twitter so dropped

    if (sys.maxunicode > 65535):
        # UCS-4
        EMOJIS_PATTERN = regex.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')
        ELLIPSIS_PATTERN = regex.compile(u"((?:\s+[^\w#@]?[\w#@]*|https?:[^\s()<>]+|[\w#@]*)(?:\.\.\.|\U00002026)\s*)$")
    else:
        # UCS-2
        EMOJIS_PATTERN = regex.compile(u'([\u2600-\u27BF])|([\uD83C][\uDF00-\uDFFF])|([\uD83D][\uDC00-\uDE4F])|([\uD83D][\uDE80-\uDEFF])')
        ELLIPSIS_PATTERN = regex.compile(u"((?:\s+[^\w#@]?[\w#@]*|[\w#@]*)(?:\.\.\.|\u2026)\s*)$")

    SMILEYS_PATTERN = regex.compile(r"(?:X|:|;|=)(?:-)?(?:\)|\(|O|D|P|S){1,}", regex.IGNORECASE)
    NUMBERS_PATTERN = regex.compile(r"(^|\s|(?<!http[^\s]+)/|[^\w/])(?:(?:[\p{Sc}]|EUR|USD|GBP)\s*)?(\-?[,.]?\d+(?:[,.]\d+)*)(?:\s*(?:%|[\p{Sc}]|EUR|USD|GBP))?(?![,.]\d|-\w)(?=[\s\p{P}]|$)")
    REPETITION_PATTERN = regex.compile(r'((\w)\2{2,})')
    PUNCTUATION_PATTERN = regex.compile(r'(?:(?<!\d)\.(?!\d))|(?:(?<=^|\W)-)|(?:-(?=\W|$))|[^\P{P}-.]') # matches all punctuation except dashes that are part of a token
