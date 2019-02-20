class SingleNode():
    def __init__(self, value):
        self.value = value
        self.next = None
        self.previous = None

class NodeIterator():
    def getBegin(self):
        pass

class SingleIterator(NodeIterator):
    def __iter__(self):
        pass

class LinkedList(SingleIterator):
    def __init__(self):
        self.begin = None
        self.end = None

    def fromIterable(iterable):
        # eff: len(iterable)

        temp = SingleNode(None)
        tempBegin = temp

        for value in iterable:
            temp.next = SingleNode(value)
            temp = temp.next

        linkedList = LinkedList()
        linkedList.begin = tempBegin.next
        linkedList.end = temp

        return linkedList

    def getBegin(self):
        return self.begin

    def isEmpty(self):
        return self.begin == None

    def addToEnd(self, value):
        if self.isEmpty():
            self.begin = Node(value)
            self.end = begin
        else:
            self.end.next = Node(value)
            self.end.next.previous = self.end
            self.end = self.end.next

    def addToBegin(self, value):
        if self.isEmpty():
            self.begin = Node(value)
            self.end = begin
        else:
            self.begin.previous = Node(value)
            self.begin.previous.next = self.begin
            self.begin = self.begin.previous



def test():
    linkedList = LinkedList.fromIterable([1, 2, 3, 4, 5])

    for item in linkedList:
        print(item)



if __name__ == '__main__':
    test()
