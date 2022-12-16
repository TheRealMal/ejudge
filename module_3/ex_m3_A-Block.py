class BlockAlg:
    def __init__(self, attemptsToBlock, p, bStart, bMax, currentTimestamp):
        self.timestamps = []
        self.__attemptsToBlock = attemptsToBlock
        self.__interval = p
        self.__ct = currentTimestamp
        self.__blockPeriod = bStart
        self.__maxBlockPeriod = bMax

    def add(self, timestamp):
        if self.__ct - timestamp < 2 * self.__maxBlockPeriod:
            self.timestamps.append(timestamp)

    def __sort(self):
        self.timestamps.sort()

    '''
        Алгоритм сортирует массив и максимум за один полный проход по массиву выдает ответ. Если еще учитывать
        то, что нужно заполнить начальный массив, то сложность по времени будет O(2n + nlog(n)).
        Асимптотическая сложность равна O(nlog(n)), потому что сортировка будет самой затратной операцией.
        Сложность по памяти равна O(n), потому что нужно хранить весь массив таймстампов (попыток) и
        питоновская сортировка (Timsort) требует O(n) памяти.
    '''
    def getBlockEndTimestamp(self):
        self.__sort()
        startBlockTimestamp, i = 0, 0
        while len(self.timestamps) - self.__attemptsToBlock >= i:
            if self.__interval > self.timestamps[self.__attemptsToBlock + i - 1] - self.timestamps[i]:
                if startBlockTimestamp > 0:
                    self.__blockPeriod *= 2
                    if self.__blockPeriod > self.__maxBlockPeriod:
                        self.__blockPeriod = self.__maxBlockPeriod
                startBlockTimestamp = self.timestamps[self.__attemptsToBlock + i - 1]
                i += self.__attemptsToBlock - 1
            i += 1
        
        if (startBlockTimestamp + self.__blockPeriod < self.__ct) or startBlockTimestamp == 0:
            return None
        return startBlockTimestamp + self.__blockPeriod
            
'''
N P B B_Max NOW
N - количество попыток для блока
P - интервал в секундах для блока за N попыток
B - начально время блокировки
B_Max - макс время блокировки
NOW - текущее время
'''

def main():
    try:
        inpArgs = input().split()
        if len(inpArgs) != 5:
            return
        a = BlockAlg(int(inpArgs[0]), int(inpArgs[1]), int(inpArgs[2]), int(inpArgs[3]), int(inpArgs[4]))
    except:
        return
    while True:
        try:
            t = int(input())
        except EOFError:
            break
        a.add(t)
    blockEnd = a.getBlockEndTimestamp()
    if blockEnd:
        print(blockEnd)
    else:
        print("ok")
        
if __name__ == "__main__":
    main()