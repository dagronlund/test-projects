__author__ = 'David'

import math

class HuffmanTreeNode:

    def __init__(self, value=None, freq=None, a=None, b=None):
        self.value = value
        self.freq = freq
        self.code = None

        self.a = a
        if a is not None:
            a.parent = self

        self.b = b
        if b is not None:
            b.parent = self

    def get_freq(self):
        if self.is_parent():
            return self.a.get_freq() + self.b.get_freq()
        else:
            return self.freq

    def get_value(self):
        if self.is_parent():
            return "Parent"
        else:
            return self.value

    def is_parent(self):
        return hasattr(self, 'a') and isinstance(self.a, HuffmanTreeNode) \
            and hasattr(self, 'b') and isinstance(self.b, HuffmanTreeNode)

    def has_parent(self):
        return hasattr(self, 'parent') and isinstance(self.parent, HuffmanTreeNode)

    def get_parent(self):
        return self.parent

    def get_code(self):#, code=None):
        if self.code is not None:
            return self.code

        if self.has_parent():
            #code.insert(0, self.get_bit())
            #return self.get_parent().get_code(code)
            self.code = [self.get_bit()] + self.get_parent().get_code()
        else:
            return []

        return self.code

    def get_bit(self):
        if self.get_parent() is not None:
            if self.get_parent().b is self:
                return 1
            else:
                return 0
        else:
            return None

    def __str__(self):
        if self.is_parent():
            return "{ Parent: , Freq: " + str(self.get_freq()) + " }"
        else:
            value = self.value
            if value == '\n':
                value = "\\n"
            return "{ Value: " + value + ", Freq: " + str(self.get_freq()) + " }"

    def __repr__(self):
        return self.__str__()

# Returns the index to insert a value at in a list, assumes list is already sorted
def binary_search(search_list, value, lower=None, upper=None, function=None):

    # Double check all optional parameters
    if function is None:
        function = lambda x: x
    if lower is None:
        lower = 0
    if upper is None:
        upper = len(search_list)

    # Calculate center value
    center = math.floor((upper + lower) / 2.0)

    # Base case for empty list or gap for search value
    if upper <= lower:
        return upper

    # Branch according to center case
    if function(search_list[center]) > value:
        return binary_search(search_list, value, lower, center - 1, function)
    elif function(search_list[center]) < value:
        return binary_search(search_list, value, center + 1, upper, function)
    else:
        return center

# Binary search test cases
#print(binary_search([1, 2, 5, 6, 8, 9], 4))
#print(binary_search([1, 2, 5, 6, 8, 9], -1))
#print(binary_search([1, 2, 5, 6, 8, 9], 10))

# Read the entire data file
data = open("input.dat", "r")
text = data.read()

# Count occurences of each character
tabulation = dict()
for c in text:
    if c in tabulation.keys():
        tabulation[c] += 1
    else:
        tabulation[c] = 1

# Build a list of huffman nodes
mergeQueue = []
for key in tabulation.keys():
    mergeQueue.append(HuffmanTreeNode(key, tabulation[key]))
nodes = mergeQueue.copy()

# Sort list of nodes based on frequency
mergeQueue.sort(key=lambda x: x.get_freq())

# Repeatedly pair smallest two nodes until one node is left
while len(mergeQueue) > 1:
    tempNode = HuffmanTreeNode(a=mergeQueue.pop(0), b=mergeQueue.pop(0))
    index = binary_search(mergeQueue, tempNode.get_freq(), function=lambda x: x.get_freq())
    mergeQueue.insert(index, tempNode)

def is_level_empty(level):
    for node in level:
        if node is not None:
            return False
    return True

def generate_levels(rootNode):
    levels = []
    current_level = []
    current_level.append(rootNode)
    levels.append(current_level)
    while True:
        oldLevel = current_level
        current_level = []
        for node in oldLevel:
            if node is not None and node.is_parent():
                current_level.append(node.a)
                current_level.append(node.b)
        if is_level_empty(current_level):
            return levels
        levels.append(current_level)
    return levels

print(len(generate_levels(mergeQueue[0])))
for level in generate_levels(mergeQueue[0]):
    print(level)

for node in nodes:
    print(node.get_code())

def get_node(nodes, c):
    for node in nodes:
        if node.get_value() == c:
            return node
    return None

complete_code = []
for c in text:
    for b in get_node(nodes, c).get_code():
        complete_code.append(b)

print(complete_code)
print(len(text))
print(len(complete_code)/8)
