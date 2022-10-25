class Node:
    def __init__(self, key, value, parrent=None):
        self.left = None
        self.right = None
        self.parent = parrent
        self.key = key
        self.value = value
    
class SplayTree:
    def __init__(self, root=None):
        self.root = root
    
    def empty(self):
        return self.root == None

    def get(self, key):
        node = self.find(key)
        if node != None:
            self.root = self.splay(node)
            return node.value
        raise LookupError

    def set(self, key, value):
        node = self.find(key)
        if node != None:
            self.root = self.splay(node)
            node.value = value
        else:
            raise LookupError

    def addNode(self, key, value):
        if self.empty():
            self.root = Node(key, value)
            return
        previous, current = None, self.root
        while current != None:
            previous = current
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:
                self.root = self.splay(current)
                raise LookupError
        if key < previous.key:
            previous.left = Node(key, value, previous)
            self.root = self.splay(previous.left)
        else:
            previous.right = Node(key, value, previous)
            self.root = self.splay(previous.right)

    def delNode(self, key):
        node = self.find(key)
        if node != None:
            self.root = self.splay(node)
            if node.left != None:
                node.left.parent = None
            if node.right != None:
                node.right.parent = None
            self.root = self.merge(node.left, node.right)
            del node
        else:
            raise LookupError

    def max(self):
        if self.empty():
            raise LookupError
        current = self.root
        while current.right != None:
            current = current.right
        self.root = self.splay(current)
        return [current.key, current.value]

    def min(self):
        if self.empty():
            raise LookupError
        current = self.root
        while current.left != None:
            current = current.left
        self.root = self.splay(current)
        return [current.key, current.value]

    def splay(self, node):
        while node.parent != None:
            nParent, nGrandparent = node.parent, node.parent.parent
            if nGrandparent == None:
                self.zig(node)
            elif (nGrandparent.left == nParent and nParent.left == node) or (nGrandparent.right == nParent and nParent.right == node):
                self.zigZig(node)
            else:
                self.zigZag(node)       
        return node

    def zig(self, node):
        parent = node.parent
        if parent.parent:
            if parent.parent.left == parent:
                parent.parent.left = node
            else:
                parent.parent.right = node

        if parent.left == node:
            parent.left = node.right
            if node.right:
                node.right.parent = parent
            node.right = parent
            node.parent = parent.parent
            parent.parent = node
        else:
            parent.right = node.left
            if node.left:
                node.left.parent = parent
            node.left = parent
            node.parent = parent.parent
            parent.parent = node

    def zigZig(self, node):
        self.zig(node.parent)
        self.zig(node)

    def zigZag(self, node):
        self.zig(node)
        self.zig(node)

    def find(self, key):
        previuos, current = None, self.root
        while current != None and current.key != key:
            previuos = current
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
        if current == None and previuos != None:
            self.root = self.splay(previuos)
        return current

    def print(self):
        if self.empty():
            print("_")
            return
        print("[{} {}]".format(self.root.key, self.root.value))
        currentLevel = [self.root.left, self.root.right]
        ifContinue = True
        while ifContinue:
            ifContinue = False
            newLevel, outputLevel = [None] * (len(currentLevel) * 2), [None] * len(currentLevel)
            for _ in range(len(currentLevel)):
                if currentLevel[_]:
                    outputLevel[_] = "[{} {} {}]".format(currentLevel[_].key, currentLevel[_].value, currentLevel[_].parent.key)
                    if currentLevel[_].left:
                        newLevel[_ * 2] = currentLevel[_].left
                        ifContinue = True
                    if currentLevel[_].right:
                        newLevel[_ * 2 + 1] = currentLevel[_].right
                        ifContinue = True
                else:
                    outputLevel[_] = "_"
            currentLevel = newLevel
            print(" ".join(outputLevel))

    def merge(self, tree1, tree2):
        if tree1 == None:
            return tree2
        if tree2 == None:
            return tree1
        current = tree1
        while current.right != None:
            current = current.right
        tree1 = self.splay(current)
        tree1.right = tree2
        if tree2 != None:
            tree2.parent = tree1
        return tree1

def main():
    tree = SplayTree()
    while True:
        try:
            inp = input().split()
        except EOFError:
            break
        if len(inp) == 0:
            continue

        command = inp[0]
        if command == "add":
            try:
                key = int(inp[1])
                if len(inp) == 3:
                    val = inp[2]
                else:
                    val = ""
                tree.addNode(key, val)
            except LookupError:
                print("error")

        elif command == "set":
            try:
                key = int(inp[1])
                if len(inp) == 3:
                    val = inp[2]
                else:
                    val = ""
                tree.set(key, val)
            except:
                print("error")
        elif command == "min":
            try:
                res = tree.min()
                print("{} {}".format(res[0], res[1]))
            except:
                print("error")
        elif command == "max":
            try:
                res = tree.max()
                print("{} {}".format(res[0], res[1]))
            except:
                print("error")
        elif command == "delete":
            try:
                key = int(inp[1])
                tree.delNode(key)
            except:
                print("error")
        elif command == "search":
            try:
                key = int(inp[1])
                res = tree.get(key)
                print("1 {}".format(res))
            except:
                print("0")
        elif command == "print":
            tree.print()
        else:
            print("error")

if __name__ == "__main__":
    main()