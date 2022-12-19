class Item:
    def __init__(self, c, w):
        self.cost = c
        self.weight = w

class Items:
    def __init__(self, c=0, w=0, data=None):
        if data is None:
            self.data = []
        else:
            self.data = data
        self.cost = c
        self.weight = w
    
class Knapsack:
    def __init__(self, items, capacity, eps):
        self.items = items
        self.capacity = capacity
        self.eps = eps

    def __mostExpensive(self):
        return max(self.items, key=lambda item: item.cost).cost
    
    def solve(self):
        newList, k = [], self.eps * self.__mostExpensive() / len(self.items) / (1 + self.eps)
        for i in self.items:
            newList.append(Item(int(i.cost / k), i.weight))
        data = {
            0: Items()
        }
        for _ in range(len(newList)):
            for dataVal in list(data.values()):
                c, w = dataVal.cost + newList[_].cost, dataVal.weight + newList[_].weight
                if w <= self.capacity:
                    if c not in data.keys() or data[c].weight > w:
                        data[c] = Items(c, w, dataVal.data + [_])
        res = data[max(data.keys())]
        res.cost = 0
        for _ in res.data:
            res.cost += self.items[_].cost
        return res

def main():
    try:
        eps, cap = float(input()), int(input())
    except:
        return
    items = []
    while True:
        try:
            inp = input().split()
        except EOFError:
            break
        items.append(Item(int(inp[1]), int(inp[0])))
    res = Knapsack(items, cap, eps).solve()
    print("{} {}".format(res.weight, res.cost))
    for _ in res.data:
        print("{}".format(_ + 1))

if __name__ == "__main__":
    main()
