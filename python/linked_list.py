class LinkedList(object):

    def __init__(self):
        self.length = 0
        self.list = []

    def insert(self, data):

        self.list.append(data)
        self.length += 1

    def pop(self):
        if self.length > 0:
            data = self.list[self.length - 1]
            self.length -= 1
            return data
        else:
            return None

    def head(self):
        return self.list[0]

    def tail(self):
        return self.list[self.length - 1]


