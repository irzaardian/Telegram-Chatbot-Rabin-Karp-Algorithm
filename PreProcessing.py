import nltk
import math
import string
import re
from nltk import *
from nltk.corpus import stopwords

def tokenizing (input):
    text = nltk.word_tokenize(input)
    return text

def case_folding (input):
    text = [i.casefold() for i in input]
    return text

def punctuation_removal_inputan(input):
    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    for i in input:
        if i in punc:
            input = input.replace(i, "")
    return input

def punctuation_removal(input):
    input = list(filter(lambda token: token not in string.punctuation, input))
    return input

def remove_space(input):
    x = 0
    while x < len(input):
        if input[x] == '':
            del input[x]
        x = x+1
    return input

def stopword_removal(input):
    stop_words = set(stopwords.words('indonesian'))
    filtered_sentence = [w for w in input if not w.lower() in stop_words]
    return filtered_sentence

def konversi_ascii(input):
    hasil_konversi_inputan = []
    i=0
    while i < len(input):
        j=0
        pow = 1
        ascii = []
        while j < len(input[i]):
            convert = ord(input[i][j])
            hash = convert * math.pow(26,pow)
            ascii.append(hash)
            j = j + 1
            pow = 1 - pow
        hasil_konversi_inputan.append(ascii)
        i = i+1
    return hasil_konversi_inputan

def rolling_hash(input):
    hasil_hashing = []
    i=0
    while i < len(input):
        j=0
        while j < len(input[i]):
            tambah = int(input[i][j] + input[i][j+1])
            hasil_hashing.append(tambah)
            j = j + 2
        i = i+1
    return hasil_hashing