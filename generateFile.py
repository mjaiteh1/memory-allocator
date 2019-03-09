import random
import string

def generate_file():

    algorithms = ["first", "best", "worst", "random"]
    action = ["alloc" ,"free", "alloc", "alloc","alloc","alloc","alloc","free"]
    file = open("input2.txt","w")
    pool_size = random.randint(100,1000)
    alloc_names = []
    file.write("pool  " + random.choice(algorithms) + "  " + str(pool_size) + "\n")
    
    for i in range(random.randint(5,20)):
        choice = random.choice(action)
        name = random.choice(string.ascii_uppercase)
        size = random.randint(1,pool_size//2)
        if choice == "alloc":
            if name not in alloc_names:
                file.write(choice + " " + name + " " + str(size) + "\n")
            alloc_names.append(name)
        else:
            if len(alloc_names) != 0:
                free_block = random.choice(alloc_names)
                alloc_names.remove(free_block)
                file.write(choice + " " + free_block + "\n")
    
    file.close()

generate_file()
