from math import ceil, log, log2, sqrt
from builtins import bytearray

class Bitarray:
    def __init__(self, size):
        self.size = size
        self.arr = bytearray(ceil(size / 8))
    
    def __bit(self, i):
        return 2 ** (i % 8)

    def __getitem__(self, i):
        if i >= self.size:
            raise IndexError
        bit = self.__bit(i)
        if bit <= self.arr[i // 8] % (2 * bit):
            return 1
        return 0

    def __setitem__(self, k, v):
        if k >= self.size:
            raise IndexError
        if v == 0:
            if not self[k]:
                return
            self.arr[k // 8] -= self.__bit(k)
        elif v == 1:
            if self[k]:
                return
            self.arr[k // 8] += self.__bit(k)
        else:
            raise ValueError

class Bloom():
    def __init__(self, n: int, p: float):
        if n <= 0 or p >= 1:
            raise ValueError
        
        self.size = round(-1 * n * log2(p) / log(2))
        self.hSize = round(-1 * log2(p))

        if self.hSize == 0 or self.size == 0:
            raise ValueError

        self.arr = Bitarray(self.size)
        self.__prime = self.__find_prime()

    def __find_prime(self):
        result = [2, 3, 5, 7, 11, 13]
        if self.hSize <= len(result):
            return result[:self.hSize]
        
        tmp = result[-1]
        while True:
            if len(result) >= self.hSize:
                break
            tmp += 2
            for _ in result:
                if tmp % _ == 0:
                    break
            else:
                for _ in range(result[-1], ceil(sqrt(tmp)), 2):
                    if tmp % _ == 0:
                        break
                else:
                    result.append(tmp)
        return result
    
    def __hash(self, k, v):
        return (((k + 1) * v + self.__prime[k]) % (2 ** 31 - 1)) % self.size

    def add(self, k: int):
        for _ in range(self.hSize):
            self.arr[self.__hash(_, k)] = 1

    def find(self, k: int):
        for _ in range(self.hSize):
            if self.arr[self.__hash(_, k)] == 0:
                return False
        return True

def printFilter(obj):
    for _ in range(obj.arr.size):
        print(obj.arr[_], end="")
    print("", end="\n")

def main():
    while True:
        try:
            inp = input()
        except EOFError:
            return
        if len(inp) > 0:
            inp = inp.split(" ")
            if len(inp) == 3 and inp[0] == "set":
                try:
                    bloomFilter = Bloom(int(inp[1]), float(inp[2]))
                    print("{} {}".format(bloomFilter.size, bloomFilter.hSize))
                    break
                except:
                    print("error")
            else:
                print("error")
    while True:
        try:
            inp = input()
        except EOFError:
            return
        if len(inp) > 0:
            if inp[:4] == "add " and " " not in inp[4:]:
                try:
                    bloomFilter.add(int(inp[4:]))
                except:
                    print("error")
            elif inp[:7] == "search " and " " not in inp[7:]:
                try:
                    res = int(bloomFilter.find(int(inp[7:])))
                    print(res)
                except:
                    print("error")
            elif inp[:5] == "print" and len(inp) == 5:
                printFilter(bloomFilter)
            else:
                print("error")

if __name__ == "__main__":
    main()