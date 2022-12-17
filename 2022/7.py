# Part 1: Find all of the directories with a total size of at most 100000. What is the sum of the total sizes of those directories?
# Answer: 1583951

# Part 2: Find the smallest directory that, if deleted, would free up enough space on the filesystem to run the update. What is the total size of that directory?
# Answer: ???

# Execution time: ???

class Node(object):
    def __init__(self, path, size, parent):
        self.children = []
        self.size = size
        self.parent = parent
        self.path = path

    def create_child(self, name):
        new_child = Node(name, 0, self)
        self.children.append(new_child)
        return new_child


root_node = Node("/", 0, None)
current_node = root_node

with open("inputs/7_input.txt") as f:
    lst = []
    for line in f:
        line = line.strip().split(" ")
        
        if line[0] == "$":
            if line[1] == "cd":
                # ROOT NODE
                if line[2] == "/":
                    pass
                # GO TO CHILD NODE
                elif line[2].isalpha():
                    current_node = current_node.create_child(line[2])
                # GO TO PARENT NODE
                elif line[2] == "..":
                    current_node = current_node.parent
            # LS
            else:
                pass

        if line[0].isdigit():
            current_node.size += int(line[0])


answer_size = 0
working_node = root_node
node_sizes = []

def calc_children(node):
    global answer_size, node_sizes
    if len(node.children) > 0:
        for child in node.children:
            calc_children(child)
    if node.size <= 100000:
        answer_size += node.size
    if node.parent is not None:
        node.parent.size += node.size
    node_sizes.append(node.size)

calc_children(working_node)
print(answer_size)

# total_space = 70000000
# space_rem = total_space - root_node.size
# space_diff = 30000000 - space_rem

# node_sizes.sort()
# for node in node_sizes:
#     if node >= space_diff:
#         print(node)
#         break