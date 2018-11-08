import numpy as np
#Definition for hash tree node
class hashNode(object):
    def __init__(self, level):
        self.val = []
        #child has the format{0:adress,1:adress,2:adress}
        self.child = {}
        #level is the split inedx
        self.level = level
        self.split = False
    #build new key value pairs for child,return root adress.
    def getChild(self, childKey):
        if childKey not in self.child.keys():
            self.child[childKey] = hashNode(self.level + 1)
        return self.child[childKey]


class hashTree():
    def __init__(self, threshold):
        self.root = hashNode(0)
        self.threshold = threshold
    
    # inser every item from itemset.
    def scratch(self, itemset):
        for item in itemset:
            self.insert(self.root, item)
    '''
    if node has splited,then insert item based on next level value.
    if node hasn't been splited,append item.
    if node value>threshold,insert item in the node value to the hash tree.
    '''
    def insert(self, node, item):
        if node.split:
            childKey = item[node.level] % self.threshold
            self.insert(node.getChild(childKey), item)
            return

        node.val.append(item)
        if len(node.val) > self.threshold:
            itemset = node.val
            node.val = []
            node.split = True
            for item in itemset:
                childKey = item[node.level] % self.threshold
                self.insert(node.getChild(childKey), item)

# Recursion to print hash tree.
def level_print(root):     
    res=[]    
    #print(root.val)
    if len(root.val)>0:
        res.append(root.val)
    elif root.val==[]:
        #print(root)
        for x in root.child.keys():
            #print(x)
            res.append(level_print(root.child[x]))
    return res

itemset=[[1,2,4],[1,2,9],[1,3,5],[ 1,3,9],[1,4,7],[1,5,8],[1,6,7],[1,7,9],[1,8,9],
         [2,3,5],[2,4,7],[2,5,6],[2,5,7],[2,5,8],[2,6,7],[2,6,8],[2,6,9],[2,7,8],
         [3,4,5],[3,4,7],[3,5,7],[3,5,8],[3,6,8],[3,7,9],[3,8,9],[4,5,7],[4,5,8],
         [4,6,7],[4,6,9],[4,7,8],[5,6,7],[5,7,9],[5,8,9],[6,7,8],[6,7,9]]
       
tree = hashTree(3)
tree.scratch(itemset)
print("success")
#print(tree.root)
#print(tree.root.child)
x=level_print(tree.root)
print(x)


