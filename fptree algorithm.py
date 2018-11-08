#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
the code takes 8 seconds to get the results of question (a) and (b).
'''
import pandas as pd
import numpy as np
import copy

#groceries = pd.read_csv('/Users/junewang/Desktop/5002 Data Mining/MSBD5002_Assignment_1/groceries.csv', header=None,
#                        keep_default_na=False)
groceries = pd.read_csv('./groceries.csv', header=None,
                        keep_default_na=False)

# processing data,get items which occurance num is larger than 300.
def getpruneddf(df, threshold):
    '''
    :param df:
    :param threshold:
    :return:
    '''
    res = {}
    for i in range(len(df)):
        for j in range(len(df.iloc[0, :])):
            res[df.iloc[i, j]] = res.get(df.iloc[i, j], 0) + 1
    # print(res)
    result = {k: v for k, v in res.items() if v >= threshold and len(k)!=0}
    x=sorted(result.items(),key = lambda x:x[1],reverse = True)
    sorteddic=[]
    for i in range(len(x)):
        sorteddic.append(x[i][0])
    pruneddf = df[df.isin(result.keys())]
    return sorteddic,pruneddf

# Definition for trie node.
class trieNode(object):
    def __init__(self):
        self.is_end = False
        self.children = {}

# Defination for Trie tree.
class Trie:
    def __init__(self):
        self.root = trieNode()
    # insert every transaction into the fptree
    def insert(self, recordlist):
        cur = self.root
        # key value pairs: key:item;value:(adress,number)
        for i in range(len(recordlist)):
            if recordlist[i] not in cur.children:
                cur.children[recordlist[i]] = [trieNode(), 0]
                # print(cur.children)
            if recordlist[i] in cur.children:
                cur.children[recordlist[i]][1] += 1

            if i != len(recordlist) - 1:
                cur = cur.children[recordlist[i]][0]
            else:
                cur.is_end = True
        return cur
    # the same way to insert items, the difference is that insert2 is used for building condition tree.
    def insert2(self,recordlist,numlist):
        cur = self.root
        for i in range(len(recordlist)):
            if recordlist[i] not in cur.children:
                cur.children[recordlist[i]] = [trieNode(), 0]
            if recordlist[i] in cur.children:
                cur.children[recordlist[i]][1] += numlist[i]

            if i != len(recordlist) - 1:
                cur = cur.children[recordlist[i]][0]
            else:
                cur.is_end = True
        return cur

# Insert every transaction to the main trie tree.        
def getfptree(pruneddf,sorteddic):
    S = Trie()
    for i in range(len(pruneddf)):
        # single_trans represents every transaction in the groceries.
        single_trans = list(pruneddf.iloc[i, :])
        single_trans1 = [x for x in single_trans if x != "" and str(x) != "nan"]
        # print(single_trans1)
        if len(single_trans1) > 0:
            #print(single_trans1)
            single_trans1 = sorted(single_trans1,key=sorteddic.index)
            S.insert(single_trans1)
    return S

# recursion method to get all possible path of the trie tree.
class recursion:
    def recursion(self, root):
        res = []

        if len(root.children) == 0:
            return res
        for key in root.children.keys():
            self.getTriepath({'key': key, 'children': root.children[key][0].children, 'num': root.children[key][1]}, [],
                             res)
        return res

    def getTriepath(self, node, path, res):

        curPath = copy.deepcopy(path)
        curPath.append((node['key'], node['num']))
        res.append(curPath)
        if len(node['children']) == 0:
            return

        for key in node['children'].keys():
            self.getTriepath(
                {'key': key, 'children': node['children'][key][0].children, 'num': node['children'][key][1]}, curPath,
                res)
'''
calculate frequent items,result is the frequent item for every condition item.
dic is the pruned path for every condition item.
'''
def getfrequentitem(input_list, threshold):
    dic = {}
    for i in range(len(input_list)):
        if input_list[i][-1][0] in dic.keys():
            dic[input_list[i][-1][0]].append(input_list[i])
        if input_list[i][-1][0] not in dic.keys():
            dic[input_list[i][-1][0]] = [input_list[i]]
            # print(dic[input_list[i][-1][0]])
    result = {}
    for key in dic.keys():  # key是每一个condition number
        for i in range(len(dic[key])):
            for j in range(len(dic[key][i])):
                dic[key][i][j] = list(dic[key][i][j])
                dic[key][i][j][1] = dic[key][i][-1][1]
                
    for key in dic.keys():
        sumlist = []
        for i in range(len(dic[key])):
            sumlist = sumlist + dic[key][i]
        dic_sumlist = {}
        for i in range(len(sumlist)):
            dic_sumlist[sumlist[i][0]] = dic_sumlist.get(sumlist[i][0], 0) + sumlist[i][1]
        dic_sumlist = {k: v for k, v in dic_sumlist.items() if v >= threshold}
        result[key] = dic_sumlist
    return dic, result

def dealwithdic(dic,result):
    for key in dic.keys():
        for i in range(len(dic[key])):
            for j in range(len(dic[key][i])):
                if dic[key][i][j][0] not in list(result[key].keys()):
                    dic[key][i][j]=[]
        for i in range(len(dic[key])):
            l=[]
            for j in range(len(dic[key][i])):
                if dic[key][i][j]!=[]:
                    l.append(dic[key][i][j])
            dic[key][i]=l
    return dic

#build condition tree for every condition item,return the path of condition tree.
def buildconditiontree(result,dic,threshold,sorteddic):
    r={}
    for key in dic.keys():  # key is the condition item.
        S=Trie()
        for i in range(len(dic[key])):
            l=[]
            num=[]
            for j in range(len(dic[key][i])):
                #print(dic[key][i][j])
                if len(dic[key][i][j])!=0:
                    l.append(dic[key][i][j][0])
                    num.append(dic[key][i][j][1])
            if len(l)!=0:
                #l=sorted(l,key=sorteddic.index)
                S.insert2(l,num)
        Rs = recursion()
        temp = Rs.recursion(S.root)
        lx=[]
        for k in range(len(temp)):
            if temp[k][-1][0]==key:
                lx.append(temp[k])
        r[key]=lx
    return r

'''
using recursion method to find the frequent itemsets.
the code for question(a) is as follows.
'''
#get all items in the condition tree.
def getItemlist(key,r):
    dic_value={}
    for i in range(len(r[key])):
        for j in range(len(r[key][i])):
            dic_value[r[key][i][j][0]] = dic_value.get(r[key][i][j][0], 0) + r[key][i][j][1]
    itemlist=dic_value.keys()
    return list(itemlist)

#get the subset of frequent items by using recursion method.
class Solution(object):
    def subsetsWithDup(self, nums):
        l = []
        nums=sorted(nums)
        self.huisu(nums, [], l, 0)
        re=[]
        for x in l:
            if x not in re:
                if x!=[]:
                    re.append(x)
        return re    
    def huisu(self, nums, item, l, num):
        if num >= len(nums):
            l.append(item)
            return
        item1 = item.copy()
        item2 = item.copy()
        item1.append(nums[num])
        self.huisu(nums, item1, l, num + 1)
        self.huisu(nums, item2, l, num + 1)

# judge whether the item is in the path.If not, return [],else,return [item,num]
def ifInpath(itemlist,path):
    l=[]
    num=[]
    x=[]
    for i in range(len(path)):
        l.append(path[i][0])
        num.append(path[i][1])
    for i in range(len(itemlist)):
        if itemlist[i] not in l:
            x=[]
            return x
        if itemlist[i] in l:
            ind=l.index(itemlist[i])
            #print(ind)
            x.append([itemlist[i],num[ind]])
        if i==len(itemlist)-1:
            
            return x

#get frequent itemsets for every condition item.
def getIncondition(r,key,threshold):
    result=[]
    solution=Solution()
    itemlist=solution.subsetsWithDup(getItemlist(key,r)) 
    for item in itemlist:
        fre=[]
        for i in range(len(r[key])): 
            freone=ifInpath(item,r[key][i])
            if freone!=[] and freone!=None:
                fre.extend(freone)
        if len(fre)>0:
            dic_fre={}
            for j in range(len(fre)):
                dic_fre[fre[j][0]]=dic_fre.get(fre[j][0],0)+fre[j][1]
            result.append(dic_fre)  
    dic_fre=result
    for i in range(len(dic_fre)):
        for key in dic_fre[i].keys():
            if dic_fre[i][key]<threshold:
                dic_fre[i]={}
                break    
    re=[]
    for i in range(len(dic_fre)):
        if dic_fre[i]!={}:
            re.append(list(dic_fre[i].keys()))  
    return re

#get all frequent itemsets.     
def getFreqset(r,threshold):
    result=[]
    for key in r.keys():
        re=getIncondition(r,key,threshold)
        result.extend(re)
    result=sorted(result)   
    re=[result[0]]
    for i in range(1,len(result)):
        if result[i]!=result[i-1]:
            re.append(result[i])
    for i in range(len(re)):
        re[i]=" ,".join(re[i])
    return re

'''
The above functions finish the calculation of question (a).
It has 61 frequent itemsets and 11 condition tree which height is higher than 2.
'''

'''
for question b, newly definated fptree for a better output.
'''
class fpNode(object):
    def __init__(self):
        self.children = {}
        self.val=0
        self.val1=""

# Defination for Trie tree.
class fpTrie:
    def __init__(self):
        # 定义Trie树的根节点
        self.root = fpNode()
    # insert every transaction into the fptree
    def insert(self, recordlist,l):
        cur = self.root
        # 每一个节点的children都是一个键值对，键是商品，值是一个tuple(地址，个数）
        for i in range(len(recordlist)):
            if recordlist[i] not in cur.children.keys():
                cur.children[recordlist[i]] = fpNode()
                cur.children[recordlist[i]].val=l[i]
                cur.children[recordlist[i]].val1=recordlist[i]

            if i != len(recordlist) - 1:
                cur = cur.children[recordlist[i]]
        return cur
# level print for the condition tree.    
def level_print(root):
    res = []
    if root.val==0:
        res.append('null set 1')
    if root == None:
        return res

    if root.val != 0:
        res.append(root.val1 + ' ' + str(root.val))

    if len(root.children.keys())!=0:
        for x in root.children.keys():
            if root.children[x] != {}:
                res.append(level_print(root.children[x]))
            else:
                return
    #print(res)
    return res

# divide the input path into l and num,l is the item path,num is the corresponding numder of the item in the path.
def dealconpath(path):
    l=[]
    num=[]
    for i in range(len(path)):
        l.append(path[i][0])
        num.append(path[i][1])
    return l,num

# inser path into condition tree.
def getpath(conpath):
    S=fpTrie()
    for i in range(len(conpath)):
        l,num=dealconpath(conpath[i])
        S.insert(l,num)

    res=level_print(S.root)
    #print(res)
    return(res)

#get rootpath for condition tree which heigh is higher than 2.
def getrootpath(r):
    rootpath={}
    for key in r.keys():
        if len(r[key])>1:
            rootpath[key]=[]
            for i in range(len(r[key])):
                if r[key][i][:-1]!=[]:
                    rootpath[key].append(r[key][i][:-1])
    return rootpath

# get final result
def getallresult(rootpath):
    for key in rootpath.keys():
        print(getpath(rootpath[key]))

def getalldf(rootpath):
    re=[]
    for key in rootpath.keys():
        re.append(getpath(rootpath[key]))
    return re


sorteddic,pruneddf = getpruneddf(groceries, 300)
#insert every record to the main fptree
trie_tree = getfptree(pruneddf,sorteddic)
#get the root of trie tree
root = trie_tree.root
#res is the main trie tree path
R = recursion()
res = R.recursion(root)
#get the frequent path result and dic is the pruned original path
dic, result = getfrequentitem(res, 300)
#main trie tree finished
dic=dealwithdic(dic,result)
# build condition tree,r is the condition path.
# the question is the occurance of tree with item>300
r=buildconditiontree(result,dic,300,sorteddic)
print("----------------------------------")
print("The output of question (a) are as follows:")
freqset=sorted(getFreqset(r,300))
output = pd.DataFrame(data=freqset,columns=["itemsets"])
output.to_csv("./Submission_Q1A.csv")
print(freqset)
print("----------------------------------")
print("The output of question (b) are as follows:")  
rootpath=getrootpath(r)  
getallresult(rootpath)        
conditiontree=getalldf(rootpath)   
  
    


