class Node:
    def __init__(self, name, isDir=False):
        self.name = name
        self.isDir = isDir
        self.childs = set()
        self.parents = set()

class Graph:
    def __init__(self):
        self.nodes = {}

    def addNode(self, node):
        self.nodes[node.name] = node
        return self.nodes[node.name]

    def checkNode(self, nodeName):
        if self.nodes.get(nodeName, None) is None:
            return self.addNode(Node(nodeName))
        return self.nodes[nodeName]
    
    def addChildNode(self, parent, child):
        pNode = self.checkNode(parent)
        pNode.childs.add(self.checkNode(child))

    def addParentNode(self, child, parent):
        cNode = self.checkNode(child)
        cNode.parents.add(self.checkNode(parent))

def buildPaths(node, current_path, checked):
    if node.name in checked:
        return
    checked.add(node.name)
    if node.isDir:
        print(" ".join(current_path[::-1]))
    for parent in node.parents:
        current_path.append(parent.name)
        buildPaths(parent, current_path, checked)
        current_path.pop()
    checked.remove(node.name)

def buildAllPaths(graph, arr_vuln):
    for vuln in arr_vuln:
        buildPaths(graph.nodes.get(vuln), [vuln], set())

def main():
    try:
        arr_vuln = input().split(" ")
        arr_dirs = input().split(" ")
    except EOFError:
        return
    if arr_vuln[0] == '' or arr_dirs[0] == '':
        return

    graph = Graph()
    arr_vuln = set(arr_vuln)

    for vuln in arr_vuln:
        graph.addNode(Node(vuln))
    for dir in arr_dirs:
        graph.addNode(Node(dir, True))

    while True:
        try:
            inp = input().split(" ")
        except EOFError:
            break
        if len(inp) == 0:
            continue
        for item in inp[1:]:
            graph.addChildNode(inp[0], item)
            graph.addParentNode(item, inp[0])

    buildAllPaths(graph, arr_vuln)

if __name__ == "__main__":
    main()