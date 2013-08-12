__author__ = 'DaiYang'
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 09 16:38:07 2013

@author: DaiYang
"""
import sys


#class Apriori(object):
#==============================================================================
#     def __init__(self, dataSet
#         self.supportValue = {}
#         self.dataSet = dataSet
#==============================================================================
def getKFrequentSet(Ck, minSupport, dataSet):
    cnt = {}
    supportValues = {}
    for ck in Ck:
        for transaction in dataSet:
            if ck & transaction == ck: #?
                if cnt.has_key(ck): cnt[ck] += 1 #? type inference
                else: cnt[ck] = 1
    Sk = []
    for ck in Ck:
        support = cnt[ck] / float(len(dataSet))
        if support >= minSupport:
            Sk.append(ck)
            supportValues[ck] = support
    return Sk, supportValues

#dateSet[[]]
def getFrequentSet(dataSet, minSupport = 0.5):
    #get candidate set of size 1
    Ck = []
    for transaction in dataSet:
        for item in transaction:
            if [item] not in Ck:
                Ck.append([item])
    Ck = map(frozenset, Ck)
    #get 1-size frequent-set
    dataSet = map(set, dataSet)
    supportValues = {} #support vals of each freq-set
    Sk, SV = getKFrequentSet(Ck, minSupport, dataSet);
    supportValues.update(SV)

    res = [Sk]
    k = 2
    #layer-wise constract frequent-set
    while(len(res[k - 2]) > 0):
        pre = res[k - 2]
        Ck = []
        #get candidate set of size k
        for i in range(0, len(pre)):
            for j in range(i + 1, len(pre)):
                #?not necessarily to sort to compare
                l1 = sorted(pre[i])
                l2 = sorted(pre[j])
                if(l1[: k - 2] == l2[: k - 2]):
                    Ck.append(pre[i] | pre[j])
        #get k-size frequent-set
        Sk, SV = getKFrequentSet(Ck, minSupport, dataSet);
        supportValues.update(SV)
        res.append(Sk)
        k += 1
    return res, supportValues

def getAssociationRules(frequentSet, supportValues, minConfidence = 0.7):
    res = {}
    rules = []
    for i in frequentSet:
        for allSet in i:
            #allSet = frozenset(j)
            if len(allSet) < 2: continue
            Ck = [frozenset([k]) for k in allSet]
            assk, confv = getKAssRules(Ck, allSet, minConfidence, supportValues)
            res.update(confv)
            rules = [assk]

            k = 2;
            while(k < len(allSet) and len(rules[k - 2]) > 0):
                pre = rules[k - 2]
                Ck = []
                #get candidate set of size k
                for i in range(0, len(pre)):
                    for j in range(i + 1, len(pre)):
                        #?not necessarily to sort to compare
                        l1 = sorted(pre[i])
                        l2 = sorted(pre[j])
                        if(l1[: k - 2] == l2[: k - 2]):
                            Ck.append(pre[i] | pre[j])
                #get k-size frequent-set
                Sk, SV = getKAssRules(Ck, allSet, minConfidence, supportValues);
                res.update(SV)
                rules.append(Sk)
                k += 1
    return res

def getKAssRules(posts, allSet, minConfidence, supportValues):
    assk = []
    confv = {}
    for post in posts:
        priori = allSet - post
        confidence = supportValues[allSet] / supportValues[priori]
        if(confidence >= minConfidence):
            assk.append(post)
            confv[(priori, post)] = confidence
    return assk, confv

def printRules(confValues):
    print "ass rules:"
    for key in confValues:
        print list(key[0]), "->", list(key[1]), ":", confValues[key]

def loadData(file = sys.stdin):
    for line in file:
        r = line.split("\t")
        yield (int(r[1]) * 5 + int(r[2]), int(r[0]))
    #xs = [[1, 4, 3], [2, 3, 5], [1, 2, 3, 5], [2, 5]]
    #return xs

if __name__ == "__main__":
    dataSet = {}
    for r in loadData():
        if not dataSet.has_key(r[0]): dataSet[r[0]] = [r[1]]
        else: dataSet[r[0]].append(r[1])
    dataSet = dataSet.values();
    #print dataSet

    freqSet, supportValues = getFrequentSet(dataSet, minSupport = 0.02)
    print "freqSet:\n", [map(list, i) for i in freqSet], '\n'
    for i in supportValues:
        print i, supportValues[i]

    confValues = getAssociationRules(freqSet, supportValues, minConfidence = 0.7)
    printRules(confValues)
   # print confValues

