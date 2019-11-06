#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import os
import numpy as np

def getwordcountvector(filename=".\\vectors_books\\Alaska Indian Dictionary.txt"):
    words = []
    wordscount = []
    wordscountratio = []
    with open(filename, encoding='utf-8', mode='r') as f:
        txt = f.read()
    contents = re.split("\n", txt)

    for line in contents:
        content = re.split("\s+", line)
        if len(content[0])>0:
            words.append(content[0])
            wordscount.append(int(content[1]))
            wordscountratio.append(float(content[2]))

    return words, wordscount, wordscountratio


def getwordset():
    with open("word_set.txt", encoding='utf-8', mode='r') as f:
        txt = f.read()
    content = re.split("\s+", txt)
    wordset = []
    for word in content:
        wordset.append(word.strip())
    return wordset

def cleanwords(words):
    wordsarr = re.split("\s+", words)

    newwordsarr = []
    for word in wordsarr:
        tempword = word.strip(" ,.“”!‘’\'\":;*#()?[]_")
        if len(tempword) < 1:
            continue
        if tempword.isnumeric():
            continue
        newwordsarr.append(tempword.lower())
    return newwordsarr

def countwords(wordsarr):
    worddic = {}
    for word in wordsarr:
        if word in worddic:
            worddic[word] = worddic[word] + 1
        else:
            worddic[word] = 1
    return worddic

def shakespeare():
    bookdir = ".\\books\\"
    vectordir = ".\\vectors_cluster\\"
    allfilenames = os.listdir(bookdir)

    standard100wordset = getwordset()
    standard100worddic = {}
    for file in allfilenames:
        print("processing", file)
        with open(bookdir+file, encoding='utf-8', mode='r', errors="ignore") as f:
            txt = f.read()
        newwordsarr = cleanwords(txt)
        wordcount = len(newwordsarr)
        worddic = countwords(newwordsarr)
        for word in standard100wordset:
            if word in worddic:
                standard100worddic[word] = worddic[word]
            else:
                standard100worddic[word] = 0
        with open(vectordir + file, encoding='utf-8', mode='w') as f:
            for word in standard100worddic:
                f.write(word + "\t" + str(standard100worddic[word]) + "\t" + str(standard100worddic[word]/wordcount) + "\n")
        print("Processing", file, "finished!")




def normalizevector(p):
    sum = 0
    length = len(p)
    i = 0
    while i<length:
        sum += p[i]
        i += 1
    result = []
    for k in p:
        result.append(k/sum)
    return result

def generateexponentialD(range, size=100):
    i = 0
    p = []
    tempP = 0.5
    while i<range:
        p.append(tempP)
        tempP /= 2
        i += 1
    data = np.random.choice(range, size, p=normalizevector(p))
    with open("exponentialD.txt", encoding='utf-8', mode='w') as f:
        for a in data:
            f.write(str(a) + "\n")

def generatenormalD(range, size):
    p = []
    i=0
    while i < range:
        p.append(1/range)
        i += 1
    data = np.random.choice(range, size, p=p)
    with open("normalD.txt", encoding='utf-8', mode='w') as f:
        for a in data:
            f.write(str(a) + "\n")

def get100WordsSet():
    wordcountupperbound = 120

    wordset = set()
    with open("wordcount.txt", encoding='utf-8', mode ='r') as f:
        txt = f.readline()
        while txt is not None:
            content = re.split("\s+", txt)
            wordset.add(content[0])
            print(len(wordset))

            if len(wordset)>wordcountupperbound-3:
                break
            txt = f.readline()

    with open("word_set.txt", encoding='utf-8', mode='w') as f:
        for word in wordset:
            f.write(word+"\n")



if __name__=='__main__':
    shakespeare()
    # getwordcountvector()
    print("Success!")