__author__ = 'DaiYang'



from itertools import combinations
import sys

class TreeNode():
    def __init__(self, name, cnt, parent):
        self.name = name
        self.cnt = cnt
        self.parent = parent
        self.kids = {}
        self.nxt = None

    def addCnt(self, cnt):
        self.cnt += cnt

    def printTree(self, indent = 1):
        print "  " * indent, self.name, ":", self.cnt
        for key in self.kids:
            childNode = self.kids[key]
            childNode.printTree(indent + 1)


#root= TreeNode, record = [item], cnt = int, head = {item, [freq, TreeNode]}
def createPath(root, record, cnt, head):
    if record == []: #? is
        return
    if not record[0] in root.kids.keys():
        root.kids[record[0]] = TreeNode(record[0], cnt, root)
        #update the head-table
        tail = head[record[0]][1]
        if tail is None:
            head[record[0]][1] = root.kids[record[0]]
        else:
            while tail.nxt is not None: #? != replace
                tail = tail.nxt
            tail.nxt = root.kids[record[0]]
    else:
        root.kids[record[0]].addCnt(cnt)

    createPath(root.kids[record[0]], record[1:], cnt, head)


#dateSet = {[item], cnt}
def createTree(dataSet, minSupport=1):
    #head = {item: [freq, TreeNode]}
    head = {}
    #get freqs of single-item
    for key in dataSet:
        for item in key:
            head[item] = head.get(item, 0) + dataSet[key]

    #sorted(head.items(), key = lambda x: x[1], reverse = False)

    for key in head.keys():
        if head[key] < minSupport:
            del (head[key])
    for key in head:
        head[key] = [head[key], None]

    #refine the dataSet
    dataSet1 = {}
    for record, cnt in dataSet.items():
            record = list(record)
            record = [i for i in record if i in head.keys()]
            record = frozenset(record)
            dataSet1[record] = dataSet1.get(record, 0) + cnt #handle duplicated keys
    dataSet = dataSet1

    #update the tree
    root = TreeNode("root", -1, None)
    for record, cnt in dataSet.items():
        record = list(record)
        record = sorted(record, key = lambda x: head[x][0], reverse=True)
        createPath(root, record, cnt, head)

    return root, head

#get conditional-pattern-bases
def getFPBase(prefixNode):
    pathBegin = prefixNode #ref-type
    res = {}
    while pathBegin is not None:
        p = pathBegin.parent
        path = []
        while p.name != "root":
            path.append(p.name)
            p = p.parent
        res[frozenset(path)] = prefixNode.cnt
        pathBegin = pathBegin.nxt

    return res


def getFrequentSet(dataSet, minSupport=1):
    root, head = createTree(dataSet, minSupport)
    #root.printTree();
    if len(root.kids) == 0:
        return [[]]
    if len(root.kids) == 1:
        res = []
        for i in range(len(head) + 1):
            #print map(lambda x: list(x), combinations(head.keys(), i))
            res.extend(map(lambda x: list(x), combinations(head.keys(), i)))
        return res

    ans = []
    for prefix in head.keys():
        newDataSet = getFPBase(head[prefix][1])
        res = getFrequentSet(newDataSet, minSupport)
        #print res
        #print map(lambda x: x.append(prefix), res)
        ans.extend(map(lambda x: x + [prefix], res))

    return ans

#input format: map
def loadData(file = sys.stdin):
    res = {}
    for line in file:
        res[frozenset(line)] = 1
    return res


if __name__ == "__main__":
    dataSet = [[1, 4, 3], [2, 3, 5], [1, 2, 3, 5], [2, 5]]
    dataSet = [['r', 'z', 'h', 'j', 'p'],
               ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
               ['z'],
               ['r', 'x', 'n', 'o', 's'],
               ['y', 'r', 'x', 'z', 'q', 't', 'p'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']
               ]
    dataSet = loadData(dataSet)
    res = getFrequentSet(dataSet, minSupport=0.5 * len(dataSet))
    print "frequent-set:\n", res