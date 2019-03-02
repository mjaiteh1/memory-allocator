import operator #https://stackoverflow.com/questions/4010322/sort-a-list-of-class-instances-python
from random import shuffle
import sys
class Simulation(object):
    def __init__(self, algorithm, size):
        self.algorithm = algorithm
        self.size = int(size)
        self.failed_alloc = 0
        self.free_list = []
        self.used_list = []
        self.free_list.append(Block("Memory", size, 0))
        
    def block_split(self, block, name, size):
        if block.size < size:
            print("Too Small")
        elif block.size == size:
            self.free_list.remove(block)
            self.used_list.append(block)
        else:
            block.size -= size
            used = Block(name, size, block.offset)
            block.offset += size
            self.used_list.append(used)
            
    def compact_free_list(self):
        self.free_list = sorted(self.free_list, key=operator.attrgetter('offset'))
        keep_list = []
        accum = Block("accum",0,0)
        for block in self.free_list:
            if block.block_meets(accum):
                accum.size += block.size
            else:
                if accum.size > 0:
                    keep_list.append(accum)
            accum = block
        if accum.size > 0:
            keep_list.append(accum)
        self.free_list = keep_list
        
    def find_block(self, name, size):
        for block in self.free_list:
            if block.size >= size:
                self.block_split(block,name,size)
                return 
        print("No Block found to fit {0}".format(name))
        self.failed_alloc += 1
    def find_block_next_fit(self, name, size):
        for block in self.free_list:
            if block.size >= size:
                self.block_split(block,name,size)
                self.free_list.remove(block)
                self.free_list.append(block)
                return 
        
    def free_block(self, name):
        for block in self.used_list:
            if block.name == name:
                self.used_list.remove(block)
                self.free_list.append(block)
                return
        print("Error: There's no block {0} to be freed".format(name))
        
    def first_fit_alloc(self, name, size):
        self.free_list = sorted(self.free_list, key=operator.attrgetter('offset'))
        self.find_block(name,size)
 
    def best_fit_alloc(self, name, size):
        self.free_list = sorted(self.free_list, key=operator.attrgetter('size'))
        self.find_block(name,size)
    def worst_fit_alloc(self, name,size):
        self.free_list = sorted(self.free_list, key=operator.attrgetter('size'))[::-1]
        self.find_block(name,size)
    def random_fit_alloc(self, name, size):
        shuffle(self.free_list)
        self.find_block(name, size)

    def next_fit_alloc(self,name,size):
        self.find_block_next_fit(name, size)
        
    def run_algorithm(self, name, size):
        if self.algorithm == "first":
            self.first_fit_alloc(name, size)
        elif self.algorithm == "worst":
            self.worst_fit_alloc(name, size)
        elif self.algorithm == "next":
            self.next_fit_alloc(name, size)
        elif self.algorithm == "random":
            self.random_fit_alloc(name, size)
        elif self.algorithm == "best":
            self.best_fit_alloc(name,size)
        else:
            print("There's no algorithm called {0}. Try again".format(self.algorithm))

            
    def percentage_mem(self):
        size_count_used = 0
        size_count_free = 0
        free_max = 0
        self.compact_free_list()
        for block in self.used_list:
            size_count_used += block.size
        for block in self.free_list:
            size_count_free +=  block.size
            if block.size > free_max:
                free_max = block.size
        print("\nPercentage of Used Memory:", round( ((size_count_used/self.size)*100), 2), "%")
        print("Percentage of Free Memory:", round( ((size_count_free/self.size)*100), 2),"%")
        print("Percentage of Fragmention:",round( (((size_count_free-free_max)/size_count_free)*100), 2),"%")
        print("Number of Failed Allocations:", self.failed_alloc)
        
    def print_memory(self):
        self.free_list = sorted(self.free_list, key=operator.attrgetter('offset'))
        self.used_list = sorted(self.used_list, key=operator.attrgetter('offset'))
        print("Printing Free Memory List: \n")
        for block in self.free_list:
              print("Block name {}, size: {}, offset {}".format(block.name,block.size,block.offset))
        print("\nPrinting Used Memory List: \n")
        for block in self.used_list:
              print("Block name {}, size: {}, offset {}".format(block.name,block.size,block.offset))
        

class Block(object):
    def __init__(self, name, size, offset):
        self.name = name
        self.size = int(size)
        self.offset = offset
    def block_meets(self, block):
        if self.offset < block.offset:
            return self.offset + self.size == block.offset
        elif self.offset > block.offset:
            return block.offset + block.size == self.offset
    def block_adjacent(self, block):
        return block.block_meets(self) or self.block_meets(block)

def main():
    
    path = sys.argv[1]
    lines = [line.rstrip('\n') for line in open(path)]
    lines = lines[:-1]
    cols = lines[0].strip().split()
    algorithm = cols[1]
    size = cols[2]
 
    memory_sim = Simulation(algorithm, size)
 
    for line in lines[1:]:
        cols = line.strip().split()
        if cols[0] == "alloc":
            name = cols[1]
            size = int(cols[2])
            memory_sim.run_algorithm(name, size)
        elif cols[0] == "free":
            name = cols[1]
            memory_sim.free_block(name)
        else:
            raise ValueError("What do you mean?:",line)
    memory_sim.percentage_mem()
    print()
    memory_sim.print_memory()


main()
