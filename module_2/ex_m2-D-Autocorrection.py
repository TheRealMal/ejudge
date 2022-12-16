class Node:
    def __init__(self, word=None, parent=None, childs={}, isWord=False):
        self.word = word
        self.parent = parent
        self.childs = childs
        self.isWord = isWord

class RadixTree:
    def __init__(self):
        self.root = Node(word=None, parent=None, childs={}, isWord=False)

    '''
    Функция add добавляет слова в деревно рекурсивно
    (С помощью вспомогательной функции __addToNode)
    Сложность O(n * m), где n - длина слова, m - высота дерева
    '''
    def add(self, s):
        self.__addToNode(self.root, s.lower())

    def __addToNode(self, node, s):
        if s[0] not in node.childs:
            node.childs[s[0]] = Node(word=s, parent=node, childs={}, isWord=True)
            return
        tmp = node.childs[s[0]].word
        prefixLen = len(tmp)
        for _ in range(1, len(tmp)):
            if len(s) <= _ or s[_] != tmp[_]:
                prefixLen = _ - 1
                break
        if prefixLen == len(tmp):
            if len(s) > len(tmp):
                return self.__addToNode(node.childs[s[0]], s[len(tmp):])
            return
        else:
            self.__splitNode(node.childs[s[0]], s, prefixLen + 1)
            return
    
    '''
    Функция __splitNode разбивает узел на узлы с общим префиксом
    Сложность O(1)
    '''
    def __splitNode(self, node, s, len):
        prefix = s[:len]
        newNode = Node(word=prefix, parent=node.parent, childs={}, isWord=False)
        node.parent.childs[prefix[0]] = newNode
        node.word = node.word[len:]
        node.parent = newNode
        newNode.childs[node.word[0]] = node
        s = s[len:]

        newNode.isWord = not s
        if s:
            newNode.childs[s[0]] = Node(word=s, parent=newNode, childs={}, isWord=True)

    '''
    Функция check проверяет слово
    Состоит из двух частей: поиск этого слова в дереве и, если слово не найдено,
    поиск 'подсказок' для автозамены ошибки в слове
    '''
    def check(self, s):
        if self.__search(s.lower()):
            return [s]
        else:
            return self.__searchCorrections(s.lower())

    '''
    Функция __search обеспечивает поиск слова в дереве
    (С помощью вспомогательной функции __searchInNode)
    Сложность O(n), где n - длина искомого слова
    '''
    def __search(self, s):
        return self.__searchInNode(self.root, s)
       
    def __searchInNode(self, node, s):
        if s[0] not in node.childs:
            return False
        tmp = node.childs[s[0]]
        if tmp.isWord and tmp.word == s:
            return True
        elif len(tmp.word) < len(s) and s[:len(tmp.word)] == tmp.word:
            return self.__searchInNode(tmp, s[len(tmp.word):])
        return

    '''
    Функция __searchCorrections обеспечивает поиск 'подсказок' в дереве
    для слова с ошибкой (С помощью вспомогательной функции __searchCorrectionsInNode)
    Сложность O(n^2 * m), где n - длина слова, m - арность дерева

    Алгоритм проходится по всем вершинам дерева с max накопленной ошибкой = 1
    В худшем случае дерево выродится в полное m-арноен дерево, а слово при проверке
    дойдет до листа дерева. Для этого нужно пройти n ярусов дерева. При каждом переходе на
    следующий ярус счетчик ошибок будет равен нулю до последнего яруса (Для корректного пути слова),
    а для остальных m - 1 вершин счетчик будет увеличиваться на 1. На всех ярусах дерева для каждой из
    m - 1 вершин будет max один путь, доходящий до листа и его длина будет n-i (i - счетчик ярусов).
    Всего имеется 4 ошибки.
    Тогда: Сумма от 0 до n (1 + 4 * (m-1) * (n - i)) = n + 4 * Сумма от 0 до n (mn - n - i - im) =
    = n + 4 * n^2 * m - 4 * m * (n * (n + 1) / 2) - 4 * n^2 - 4 * n * (n + 1) / 2 = 
    = O(n^2 * m)
    '''
    def __searchCorrections(self, s):
        return self.__searchCorrectionsInNode(self.root, s, prefix="", prefixLen=0, m=False)

    def __searchCorrectionsInNode(self, node, s, prefix="", prefixLen=0, m=False):
        result = []
        if m:
            if prefixLen < len(s) and s[prefixLen] in node.childs:
                i = node.childs[s[prefixLen]]
                if s[prefixLen:prefixLen + len(i.word)] != i.word:
                    return []
                elif i.isWord and i.word == s[prefixLen:]:
                    result.append(prefix + i.word)
                result += self.__searchCorrectionsInNode(i, s, prefix=prefix + i.word, prefixLen=prefixLen + len(i.word), m=True)
        else:
            for child in node.childs.values():
                i = len(child.word)
                for _ in range(i):
                    if len(s) <= (prefixLen + _) or s[prefixLen + _] != child.word[_]:
                        i = _
                        break
                else:
                    if child.isWord and len(s) - 1 <= len(prefix + child.word) <= len(s):
                        result.append(prefix + child.word)
                    result += self.__searchCorrectionsInNode(child, s, prefix=prefix + child.word, prefixLen=prefixLen + i, m=False)
                    continue
                self.__mistakeDiffSymbol(child, s, prefix, prefixLen, i, result)
                self.__mistakeMissingSymbol(child, s, prefix, prefixLen, i, result)
                self.__mistakeExtraSymbol(child, s, prefix, prefixLen, i, result)
                self.__mistakeTransposition(child, s, prefix, prefixLen, i, result)
        return result    

    def __mistakeDiffSymbol(self, child, s, prefix, prefixLen, i, result):
        if child.word[i+1:] == s[prefixLen + i + 1:len(prefix + child.word)]:
            if child.isWord and len(prefix + child.word) == len(s): result.append(prefix + child.word)
            result += self.__searchCorrectionsInNode(child, s, prefix=prefix + child.word, prefixLen=prefixLen + len(child.word), m=True)
    
    def __mistakeMissingSymbol(self, child, s, prefix, prefixLen, i, result):
        if child.word[i+1:] == s[prefixLen + i:len(prefix + child.word) - 1]:
            if child.isWord and len(prefix + child.word) == len(s) + 1: result.append(prefix + child.word)
            result += self.__searchCorrectionsInNode(child, s, prefix=prefix + child.word, prefixLen=prefixLen + len(child.word) - 1, m=True)
    
    def __mistakeExtraSymbol(self, child, s, prefix, prefixLen, i, result):
        if child.word[i:] == s[prefixLen + i + 1:len(prefix + child.word) + 1]:
            if child.isWord and len(prefix + child.word) == len(s) - 1: result.append(prefix + child.word)
            result += self.__searchCorrectionsInNode(child, s, prefix=prefix + child.word, prefixLen=prefixLen + len(child.word) + 1, m=True)
    
    def __mistakeTransposition(self, child, s, prefix, prefixLen, i, result): #
        if prefixLen + i + 1 < len(s) and s[prefixLen + i] in child.childs and s[prefixLen + i + 1] == child.word[i]:
            if child.isWord and len(prefix + child.word) == len(s): result.append(prefix + child.word)
            result += self.__searchCorrectionsInNode(child, "{}{}{}{}".format(s[:prefixLen+i], s[prefixLen+i+1], s[prefixLen+i], s[prefixLen+i+2:]), prefix=prefix + child.word, prefixLen=prefixLen + len(child.word), m=True)
        elif i + 1 < len(child.word) and prefixLen + i + 1 < len(s) and child.word[i] == s[prefixLen + i + 1] and child.word[i + 1] == s[prefixLen + i] and child.word[i + 2:] == s[prefixLen + i + 2:len(prefix + child.word)]:
            if child.isWord and len(prefix + child.word) == len(s): result.append(prefix + child.word)
            result += self.__searchCorrectionsInNode(child, s, prefix=prefix + child.word, prefixLen=prefixLen + len(child.word), m=True)
    
def main():
    trie = RadixTree()
    while True:
        try:
            wordsQuantity = int(input())
        except ValueError:
            continue
        except EOFError:
            return
        break

    for _ in range(wordsQuantity):
        try:
            word = input()
        except EOFError:
            return
        if len(word) == 0:
            continue
        trie.add(word)
    
    while True:
        try:
            inp = input()
        except EOFError:
            return
        if len(inp) == 0:
            continue
        result = trie.check(inp)
        if len(result) > 0:
            if result[0] == inp:
                print("{} - ok".format(inp))
                continue
            result.sort()
            print("{} -> {}".format(inp, ", ".join(result)))
        else:
            print("{} -?".format(inp))

if __name__ == "__main__":
    main()