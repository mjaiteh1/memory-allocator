import operator #https://stackoverflow.com/questions/4010322/sort-a-list-of-class-instances-python
class Simulation(object):
    def __init__(self, algorithm, size):
        self.algorithm = algorithm
        self.size = size
        self.free_list = []
        self.used_list = []

    def block_split(self, block, name, size):
        if block.size < size:
            print("Too Small")
        elif block.size == size:
            self.free_list.remove(block)
            self.used_list.append(block)
        else:
            block.size -= size
            block.offset += size
            used = Block(name, size, block.offset)
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
        
    def find_block(self, size):
        for block in self.free_list:
            if block.size >= size:
                self.block_split(block, "block",size)
                return
        print("No Block Found")

    def first_fit_alloc(self, size):
        self.free_list = sorted(self.free_list, key=operator.attrgetter('offset'))
        self.find_block(size)
        
class Block(object):
    def __init__(self, name, size, offset):
        self.name = name
        self.size = size
        self.offset = offset
    def block_meets(self, block):
        if self.offset < block.offset:
            return self.offset + self.size == block.offset
        elif self.offset > block.offset:
            return block.offset + block.size == self.offset
    def block_adjacent(self, block):
        return block.block_meets(self) or self.block_meets(block)

new_block = Block("b1",10,2)
new_block1 = Block("b2",1,1)
print(new_block1.block_adjacent(new_block))

new_simulation = Simulation("free list",5)
new_simulation.free_list.append(new_block)
new_simulation.free_list.append(new_block1)
new_simulation.block_split(new_block,"block",4)
print("Free_list",new_simulation.free_list)
print("Used List",new_simulation.used_list)

print("Compact List ", new_simulation.compact_free_list())

print("First Fit",new_simulation.first_fit_alloc(3))


