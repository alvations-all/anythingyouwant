#!/usr/bin/env python -*- coding: utf-8 -*-

from __future__ import unicode_literals

import io, sys
from itertools import chain
reload(sys); sys.setdefaultencoding("utf-8")

import lucene
from nltk.corpus import wordnet as wn
from nltk import sent_tokenize, word_tokenize

from texeval import TexEval2015
from luluwiki import retrieve_wiki

texeval_corpus = TexEval2015()

wiki_index = '/home/alvas/english-wiki'
lucene.initVM()

def filter_doc(term, doc):
    for i in sent_tokenize(doc):
        for j in i.split('\n'):
            if term.lower() in j.lower():
                yield j
            
def isa_doc(term, doc):
    for i in sent_tokenize(doc):
        if term+" is a" in i or "is a "+term in i or "is an "+term in i:
            yield i


def build_corpus():
    for sbc in texeval_corpus.test_subcorpora:
        fout = io.open('WIKI_'+sbc, 'w', encoding='utf8')
        for termid, term in texeval_corpus.terms('test', sbc):
            docs = []
            for curl, doc in retrieve_wiki(term, wiki_index):
                for fdoc in filter_doc(term, doc):
                    docs.append(fdoc)
            
            print termid, term, len(docs)
            fout.write("{}\t{}\n".format(termid, term).decode('utf8'))
            for i in docs:
        
                fout.write(i.decode('utf8')+ '\n')
            fout.write('\n'.decode('utf8'))
            