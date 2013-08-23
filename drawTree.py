__author__ = 'DaiYang'

import matplotlib.pyplot as plt

class DrawTree:

    def __init__(self):
        #every node's leaf-number
        self.leafNum = {}
        #style of elements of tree
        self.decisionNode = dict(boxstyle = "sawtooth", fc = "0.8")
        self.leafNode = dict(boxstyle = "round4", fc = "0.8")
        self.arrowArgs = dict(arrowstyle = "<-")
        #a frame(figure) can consist of several canvas
        self.canvas = plt.subplot(111, frameon=False)
        self.xOff = 0.0
        self.widthTot = float(self.getLeafNum(root))
        self.heightTot = float(self.getTreeDepth(root))


    def drawNode(self, val, (x, y), (xp, yp), nodeType):
        self.canvas.annotate(val, xy = (xp, yp), xycoords = 'axes fraction', xytext = (x, y), textcoords = 'axes fraction',
                        va = 'center', ha = 'center', bbox = nodeType, arrowprops = self.arrowArgs)

    #root: tree = (val, {annotation: tree}) || (val, {})
    def getLeafNum(self, root):
        if root[1] == {}: #leaf
            return 1
        ret = 0
        for key in root[1]: #not leaf
            ret += self.getLeafNum(root[1].get(key))

        self.leafNum[root[0]] = ret
        return ret


    def getTreeDepth(self, root):
        if root[1] == {}:
            return 0
        ret = 0
        for key in root[1]:
            ret = max(self.getTreeDepth(root[1].get(key)) + 1, ret)
        return ret

    #annotation: the text on arrow-line
    def drawTextOnLine(self, (x, y), (xp, yp), textOnLine):
        self.canvas.text((x + xp) / 2, (y + yp) / 2, textOnLine)


    def drawTree(self, root, (xp, yp), textOnLine, depth):
        #leaf
        if root[1] == {}:
            x = self.xOff
            #update x's offset
            self.xOff += 1.0 / self.widthTot
            #node's y-position = its layer in tree
            y = 1 - float(depth) / self.heightTot
            #tree-root need no arrow to be pointed to
            if (xp, yp) == (0.5, 1.0):
                (xp, yp) = (x, y)
            self.drawNode(root[0], (x, y), (xp, yp), self.leafNode)
            self.drawTextOnLine((x, y), (xp, yp), textOnLine)
        #not leaf
        else:
            #leafNum = self.getLeafNum(root)
            leafNum = self.leafNum[root[0]]
            #node's x-position = half of positions of all leafs of its subtrees
            x = self.xOff + (leafNum - 1.0) / self.widthTot / 2
            y = 1 - float(depth) / self.heightTot
            if (xp, yp) == (0.5, 1.0):
                (xp, yp) = (x, y)
            self.drawNode(root[0], (x, y), (xp, yp), self.decisionNode)
            #plot subtree
            for key in root[1]:
                self.drawTree(root[1].get(key), (x, y), key, depth + 1)

#test
# drawNode('a decision node', (0.5, 0.1), (0.1, 0.5), decisionNode)
# drawNode('a leaf node', (0.8, 0.1), (0.3, 0.8), leafNode)

root = (1, {2: (3, {}), 4: (5, {6: (8, {}), 7:(9, {})})})
#create a frame(window) firstly
frame = plt.figure(1, facecolor='white')
#clear the frame
frame.clf()
obj = DrawTree()
obj.drawTree(root, (0.5, 1.0), '', 0)
#display a frame
plt.show()