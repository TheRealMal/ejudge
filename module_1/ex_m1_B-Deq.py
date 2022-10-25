class Deque:
    def __init__(self, max_size):
        self.data = [None] * max_size
        self.max_size = max_size
        self.__first = -1
        self.__last = 0

    def isFull(self):
        return (self.__first == 0 and self.__last == self.max_size - 1) or self.__first == self.__last + 1 or self.max_size < 1

    def isEmpty(self):
        return self.__first == -1
        
    def print(self):
        if self.isEmpty():
            print("empty")
        else:
            if self.__first < self.__last:
                for _ in range(self.__first, self.__last+1):
                    if _ != self.__last:
                        print(self.data[_], end=" ")
                    else:
                        print(self.data[_], end="\n")
            elif self.__first == self.__last:
                print(self.data[self.__first])
            else:
                for _ in range(self.__first, self.max_size):
                    print(self.data[_], end=" ")
                for _ in range(0, self.__last+1):
                    if _ != self.__last:
                        print(self.data[_], end=" ")
                    else:
                        print(self.data[_], end="\n")

    def pushb(self, item):
        if not self.isFull():
            if self.__first == -1:
                self.__first = 0
                self.__last = 0
            elif self.__last == self.max_size - 1:
                self.__last = 0
            else:
                self.__last = self.__last + 1
            self.data[self.__last] = item
        else:
            print("overflow")

    def pushf(self, item):
        if not self.isFull():
            if self.__first == -1:
                self.__first = 0
                self.__last = 0
            elif self.__first == 0:
                self.__first = self.max_size - 1
            else:
                self.__first = self.__first -1
            self.data[self.__first] = item
        else:
            print("overflow")

    def popf(self):
        if self.isEmpty():
            print("underflow")
        else:
            print(self.data[self.__first])
            self.data[self.__first] = None
            if self.__first == self.__last:
                self.__first = -1
                self.__last = -1
            elif self.__first == self.max_size - 1:
                self.__first = 0
            else:
                self.__first = self.__first + 1
    def popb(self):
        if self.isEmpty():
            print("underflow")
        else:
            print(self.data[self.__last])
            self.data[self.__last] = None
            if self.__last == self.__first:
                self.__first = -1
                self.__last = -1
            elif self.__last == 0:
                self.__last = self.max_size -1
            else:
                self.__last = self.__last -1

if __name__ == "__main__":
    while True:
        try:
            inp = input()
        except EOFError:
            exit()
        if len(inp) > 0:
            if inp[:9] == "set_size " and len(inp) > 9:
                try:
                    deq = Deque(int(inp[9:]))
                    break
                except Exception as e:
                    print("error")
            else:
                print("error")
        else:
            pass

    while True:
        try:
            inp = input()
        except EOFError:
            break
        if len(inp) > 0:
            if inp[:6] == "pushb " and " " not in inp[6:]:
                deq.pushb(inp[6:])
            elif inp[:6] == "pushf " and " " not in inp[6:]:
                deq.pushf(inp[6:])
            elif inp[:4] == "popb" and len(inp) == 4:
                deq.popb()
            elif inp[:4] == "popf" and len(inp) == 4:
                deq.popf()
            elif inp[:5] == "print" and len(inp) == 5:
                deq.print()
            else:
                print("error")
        else:
            pass