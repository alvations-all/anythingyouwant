#!/usr/bin/env python -*- coding: utf-8 -*-

from __future__ import unicode_literals

import io, sys
from itertools import chain
reload(sys); sys.setdefaultencoding("utf-8")

from threading import Thread
from Queue import Queue

import lucene
from java.io import File
# For Indexing.
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig
from org.apache.lucene.store import FSDirectory
from org.apache.lucene.util import Version
# For Querying.
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher

from nltk.corpus import wordnet as wn
from nltk import sent_tokenize, word_tokenize

from texeval import TexEval2015
from luluwiki import retrieve_wiki

texeval_corpus = TexEval2015()

wiki_index = '/home/alvas/engwiki/english-wiki'
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


def build_corpus(sbc, searcher, analyzer):
    fout = io.open('WIKI_'+sbc, 'w', encoding='utf8')
    for termid, term in texeval_corpus.terms('test', sbc):
        docs = []
        for curl, doc in retrieve_wiki(term, searcher, analyzer):
            for fdoc in filter_doc(term, doc):
                docs.append(fdoc)
        
        print termid, term, len(docs)
        fout.write("{}\t{}\n".format(termid, term).decode('utf8'))
        for i in docs:
    
            fout.write(i.decode('utf8')+ '\n')
        fout.write('\n'.decode('utf8'))
    return sbc
        
def wrapper(func, arg, queue):
    """" Wrapper class for multi-threaded functions """
    queue.put(func(arg))

n = 0
sbcs = texeval_corpus.test_subcorpora
sbc = sbcs[n]
# Hack for parallelizing queries, uses one index per domain.
directory = FSDirectory.open(File(wiki_index+'-'+sbc))
searcher = IndexSearcher(DirectoryReader.open(directory))
analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
build_corpus(sbcs[n], searcher, analyzer)
