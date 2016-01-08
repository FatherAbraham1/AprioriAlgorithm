'''
Created on Nov 29, 2015

@author: PranavKulkarni
'''
#-*- coding:utf-8 - *-
import scipy.io as scipyio
import itertools
from test.test_set import powerset

matFile = "/Users/PranavKulkarni/Documents/Notes Books and Assignments/ALDA/Assignment questions and solutions/HW4 question files/transaction.mat"
dataset = None
listOfTransactions = [] 
min_support = 60
min_confidence = 80
globalListOfMinSupport = {}

def load_dataset():
    mat = scipyio.loadmat(matFile)
    global dataset
    global globalListOfMinSupport
    global listOfTransactions
    dataset = mat['transaction']
    listOfTransactions.append(set(['M', 'O', 'N', 'K', 'E', 'Y']))
    listOfTransactions.append(set(['D', 'O', 'N', 'K', 'E', 'Y']))
    listOfTransactions.append(set(['M', 'A', 'K', 'E']))
    listOfTransactions.append(set(['M', 'U', 'C', 'K', 'Y']))
    listOfTransactions.append(set(['C', 'O', 'O', 'K', 'I', 'E']))
    print "list of transactions = ", listOfTransactions                
    
def createC1():
    "Create a list of candidate item sets of size one."
    c1 = set()
    for transaction in listOfTransactions:
        for item in transaction:
            c1.add(item)
    #print "******** candidate items = ", len(c1)
    return c1
  

def createKPlus1FreqItemSet(c, k):
    if(len(c.keys()) ==1):
        return []
    listOfKPlus1Itemsets = list(itertools.combinations(c.keys(), k))
    listOfKPlus1ItemsetsWithMinSupport = {}
    for iset in listOfKPlus1Itemsets:
        iset = list(iset)
        iset = set(iset)
        itemset = iset
        #print "++++++", itemset
        listOfKPlus1ItemsetsWithMinSupport[','.join(itemset)] = 0
        globalListOfMinSupport[','.join(itemset)] = 0
        for transaction in listOfTransactions:
            if itemset.issubset(transaction):
                 listOfKPlus1ItemsetsWithMinSupport[','.join(itemset)] = listOfKPlus1ItemsetsWithMinSupport[','.join(itemset)] + 1
                 globalListOfMinSupport[','.join(itemset)] = globalListOfMinSupport[','.join(itemset)] + 1
    
    minSupportCount = (float(min_support)/100)*len(listOfTransactions)
    for j in listOfKPlus1ItemsetsWithMinSupport.keys():
        if listOfKPlus1ItemsetsWithMinSupport[j] < minSupportCount:
            del listOfKPlus1ItemsetsWithMinSupport[j] 
            del globalListOfMinSupport[j]          
    #print (listOfKPlus1ItemsetsWithMinSupport)
    return listOfKPlus1ItemsetsWithMinSupport.keys()
                 
def scanD(candidates):
    "Returns all candidates that meet a minimum support level"
    sscnt = {}
    
    for candidate in candidates:
        sscnt[candidate] = 0 # default count of each candidate is 0
        globalListOfMinSupport[candidate] = 0
        for transaction in listOfTransactions:
            if candidate in transaction:
                sscnt[candidate] = sscnt[candidate] + 1
                globalListOfMinSupport[candidate] = globalListOfMinSupport[candidate] + 1    
    #min support is in %
    #maintain only those candidates that meet min support
    minSupportCount = (float(min_support)/100)*len(listOfTransactions)
    for candidate in sscnt.keys():
        if sscnt[candidate] < minSupportCount:
            #this candidate is not retained for next round and hence removed
            del sscnt[candidate]
            del globalListOfMinSupport[candidate]
    #print "x ====> ", sscnt
    return sscnt    

def apriori():
    load_dataset()
    c1 = createC1()
    l1 = scanD(c1)
    i = 2
    allFreqItemSets = []
    allFreqItemSetsForConf = []
    allFreqItemSets.append(l1.keys())
    while True:
        x = createKPlus1FreqItemSet(l1, i)
        #print "x =====> ", x
        if x is None or len(x) == 0:
            break
        else:
            i = i+1
            allFreqItemSets.append(x)
    #print allFreqItemSets
    result = open("frequentitemsets.txt", 'w')
    for eachList in allFreqItemSets:
        for eachItemSet in eachList:
            result.write(eachItemSet + '\n')
            allFreqItemSetsForConf.append(eachItemSet) 
            #put all frequent item sets in one list
    result.close()            
    genRules()
    
def genRules():
    #find subset of each frequent itemset by reading the file.
    print "gen rules called"
    rules = []
    with open("frequentitemsets.txt", 'r') as itemsFile:
        print "file open"
        for line in itemsFile:
            line = line.replace('\n', '')
            splitLine = line.split(',')
            #print "#####",splitLine
            if len(splitLine) > 1:
                supportCountTogether = globalListOfMinSupport[line]
                #print line, " SUPPORT COUNT TOGETHER = ", supportCountTogether
                tempSet = set()
                for eachItem in splitLine:
                    tempSet.add(eachItem)    
                powerSet = list(powerset(tempSet))
                #for all non empty subsets
                for s in powerSet:
                    if len(s) > 0 and len(s) != len(tempSet):
                        remain = tempSet - s
                        #print "remaining ==== ", remain
                        #find s's support count
                        sCount = 0
                        for transaction in listOfTransactions:
                            if s.issubset(transaction):
                                sCount = sCount + 1
                        if float(supportCountTogether)/sCount >= float(min_confidence)/100:
                            rules.append('support count together = ' + str(float(supportCountTogether)) + '    support count of s = ' + str(sCount) + '  ' + ','.join(s) + '->' + ','.join(remain))
                        else:
                            rules.append('Rejected****support count together = ' + str(float(supportCountTogether)) + '    support count of s = ' + str(sCount) + '  ' + ','.join(s) + '->' + ','.join(remain))
                                
    print "rules---------------------------------------"
    print globalListOfMinSupport
    for rule in rules:
        print rule                           
                        
                
    
    
    
apriori()