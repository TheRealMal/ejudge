class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value

class MinHeap:
    def __init__(self):
        self.table = {} # key -> index
        self.arr = [] # index -> node

    def set(self, key, value):
        x = self.table.get(key, None)
        if not x:
            raise LookupError
        self.arr[x].value = value

    def empty(self):
        if self.arr:
            return False
        return True
    
    def extract(self):
        if self.empty():
            raise LookupError
        tmp = self.arr[0]
        self.table[self.arr[-1].key] = 0
        del self.table[tmp.key]
        self.heapify(0)
        return tmp
    
    def find(self, key):
        x = self.table.get(key, None)
        if x is None:
            raise LookupError
        return [x, self.arr[x]]

    def add(self, key, value):
        if self.table.get(key, None) is not None:
            raise LookupError
        self.table[key] = len(self.arr)
        self.arr.append(Node(key, value))
        self.heapifyUp(len(self.arr)-1)
    
    def min(self):
        if self.empty():
            raise LookupError
        return [0, self.arr[0]]
    
    def max(self):
        if self.empty():
            raise LookupError
        maxIndex = 0
        for _ in range(len(self.arr)):
            if self.arr[_].key > self.arr[maxIndex].key:
                maxIndex = _
        return [maxIndex, self.arr[maxIndex]]
    
    def remove(self, key):
        x = self.table.get(key, None)
        if x is None:
            raise LookupError
        self.table[self.arr[-1].key] = x
        del self.table[key]
        self.heapify(x)

    def __swap(self, first, second):
        self.table[self.arr[first].key], self.table[self.arr[second].key] = self.table[self.arr[second].key], self.table[self.arr[first].key]
        self.arr[first], self.arr[second] = self.arr[second], self.arr[first]

    def heapifyUp(self, x):
        if not x:
            return
        parent = (x - 1) >> 1
        while x and self.arr[x].key < self.arr[parent].key:
            self.__swap(x, parent)
            x = parent
            parent = (parent - 1) >> 1
    
    def heapifyDown(self, x):
        left = (x << 1) + 1
        right = left + 1
        while left < len(self.arr):
            if right < len(self.arr):
                if self.arr[x].key < self.arr[left].key and self.arr[x].key < self.arr[right].key:
                    break
                elif self.arr[left].key < self.arr[right].key:
                    self.__swap(x, left)
                    x = left
                else:
                    self.__swap(x, right)
                    x = right
            else:
                if self.arr[x].key < self.arr[left].key:
                    break
                else:
                    self.__swap(x, left)
                x = left
            left = (x << 1) + 1
            right = left + 1

    def heapify(self, index):
        self.arr[index], self.arr[-1] = self.arr[-1], self.arr[index]
        self.arr.pop()
        if index != len(self.arr):
            parent = (index - 1) >> 1
            if index == 0 or self.arr[parent].key < self.arr[index].key:
                self.heapifyDown(index)
            else:
                self.heapifyUp(index)

def printHeap(heap):
    if heap.empty():
        print("_")
        return
    print("[{} {}]".format(heap.arr[0].key, heap.arr[0].value))
    level, i = 2, 1
    while i < len(heap.arr):
        if i + level <= len(heap.arr):
            for _ in range(level-1):
                el = heap.arr[i + _]
                parentIndex = (i + _ - 1) >> 1
                print("[{} {} {}]".format(el.key, el.value, heap.arr[parentIndex].key), end=" ")
            print("[{} {} {}]".format(heap.arr[i + level - 1].key, heap.arr[i + level - 1].value, heap.arr[((i + level - 2) >> 1)].key), end="\n")
        else:
            differce = len(heap.arr) - i
            for _ in range(differce):
                el = heap.arr[i + _]
                parentIndex = (i + _ - 1) >> 1
                print("[{} {} {}]".format(el.key, el.value, heap.arr[parentIndex].key), end=" ")
            print((level - differce - 1) * '_ ', end='_\n')
        i += level
        level = level << 1

def main():
    heap = MinHeap()
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
                heap.add(key, val)
            except LookupError:
                print("error")
        elif command == "set":
            try:
                key = int(inp[1])
                if len(inp) == 3:
                    val = inp[2]
                else:
                    val = ""
                heap.set(key, val)
            except LookupError:
                print("error")
        elif command == "min":
            try:
                res = heap.min()
                print("{} {} {}".format(res[1].key, res[0], res[1].value))
            except LookupError:
                print("error")
        elif command == "max":
            try:
                res = heap.max()
                print("{} {} {}".format(res[1].key, res[0], res[1].value))
            except LookupError:
                print("error")
        elif command == "delete":
            try:
                key = int(inp[1])
                heap.remove(key)
            except LookupError:
                print("error")
        elif command == "search":
            try:
                key = int(inp[1])
                res = heap.find(key)
                print("1 {} {}".format(res[0], res[1].value))
            except LookupError:
                print("0")
        elif command == "extract":
            try:
                res = heap.extract()
                print("{} {}".format(res.key, res.value))
            except LookupError:
                print("error")
        elif command == "print":
            printHeap(heap)
        else:
            print("error")

if __name__ == "__main__":
    main()