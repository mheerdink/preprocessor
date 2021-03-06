# -*- coding: utf-8 -*-

"""
preprocessor.preprocess
~~~~~~~~~~~~
This module includes preprocess functionality

"""

import regex
from html import unescape
from .defines import *
from .utils import Utils

class Preprocess:

    tweet = None

    def __init__(self):
        self.repl = None
        self.u = Utils()

    def clean(self, tweet_string, repl):
        assert isinstance(tweet_string, str)

        cleaner_methods = self.u.get_worker_methods(self, Defines.PREPROCESS_METHODS_PREFIX)

        for a_cleaner_method in cleaner_methods:
            token = self.get_token_string_from_method_name(a_cleaner_method, Defines.PREPROCESS_METHODS_PREFIX)
            method_to_call = getattr(self, a_cleaner_method)

            if repl == Functions.CLEAN:
                tweet_string = method_to_call(tweet_string, '')
            else:
                tweet_string = method_to_call(tweet_string, token)

        tweet_string = self.remove_unneccessary_characters(tweet_string)
        return tweet_string

    def preprocess_reserved_words(self, tweet_string, repl):
        return regex.sub(Patterns.RESERVED_WORDS_PATTERN, lambda m: repl + m.groups()[0], tweet_string)

    def preprocess_urls(self, tweet_string, repl):
        return Patterns.URL_PATTERN.sub(repl, tweet_string)

    def preprocess_hashtags(self, tweet_string, repl):
        return Patterns.HASHTAG_PATTERN.sub(repl, tweet_string)

    def preprocess_mentions(self, tweet_string, repl):
        return Patterns.MENTION_PATTERN.sub(repl, tweet_string)

    def preprocess_ellipsis(self, tweet_string, repl):
        return Patterns.ELLIPSIS_PATTERN.sub(repl, tweet_string)

    def preprocess_emojis(self, tweet_string, repl):
        if not Defines.IS_PYTHON3:
            tweet_string = tweet_string.decode('utf-8')
        return Patterns.EMOJIS_PATTERN.sub(repl, tweet_string)

    def preprocess_smileys(self, tweet_string, repl):
        return Patterns.SMILEYS_PATTERN.sub(repl, tweet_string)

    def preprocess_numbers(self, tweet_string, repl):
        return regex.sub(Patterns.NUMBERS_PATTERN, lambda m: m.groups()[0] + repl, tweet_string)

    def preprocess_repetition(self, tweet_string, repl):
        return regex.sub(Patterns.REPETITION_PATTERN, lambda m: m.groups()[1] + m.groups()[1], tweet_string) # ignore repl to avoid messing up the tokenizer

    def preprocess_punctuation(self, tweet_string, repl):
        return Patterns.PUNCTUATION_PATTERN.sub(' ', tweet_string) # replace with space to avoid messing up the tokenizer

    def preprocess_lowercase(self, tweet_string, repl):
        return tweet_string.lower() # lowercase the string

    def preprocess_html_entities(self, tweet_string, repl):
        return unescape(tweet_string)

    def remove_unneccessary_characters(self, tweet_string):
        return ' '.join(tweet_string.split())

    def get_token_string_from_method_name(self, method_name, prefix='preprocess_'):
        needle = method_name.replace(prefix, '', 1)
        token_string = ' $' + list(opts.keys())[list(opts.values()).index(needle)] + '$ '
        return token_string