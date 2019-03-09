#  CSC262: Mariama Jaiteh, Eindra Kyi

## How to Build and Run the Program:
We used Python and our program can be run from the command line, 
**e.g. python mem.py input.txt**, arguments in that order.

### If you want to generate a random txt file:

Run: python generateFile.py
Then Run: python mem.py input2.txt


## Give me an input file that you have used:
```
pool first 1000
alloc A 200
alloc B 300
alloc C 100
free B
alloc D 150
alloc E 100
alloc F 200
free D
alloc G 100
alloc H 100
```
For example, if you want to run "first", "next","worst","random", then **change the "first" in the first line of the file** into the algorithm you want.

Input file is in the folder. 


# Extra Credit Opportunities:

## 1. Figure out how to measure **fragmentation**. Is there a single number you could use to represent how fragmented your simulator is?

We looked up ways to do this. We finally came upon a [StackOverflow post](https://stackoverflow.com/questions/4586972/how-to-calculate-fragmentation) which suggested a percentage measure we found convincing:

## **( (free - freemax)/(free) ) * 100%**, 
where __free__ represented the total number of free blocks and __freemax__ represented the size of the largest free block. This measure will allow us to know that when the percentage fragmentation is 0%, all the memory is in a single big block, and if the percentage fragmentation is in many small little blocks, the metric becomes closer to 100%.

## 2. Generate Random File 

We created a file called generateFile.py that generates a random file of commands. 
When randomly choosing whether to "alloc" or "free", there is a higher probability to choose alloc because we didn't want to free everything we alloc which seemed to be happening when we only had "alloc" and "free" in the list. Instead we added more "alloc"'s to the list. We couldn't find a good way to do a weighted probability when doing a random choice so this was simple enough to get the job done. 


### Note:

1. We not entirely sure if our next fit works. :( 
2. Using the random file generator we were able to debug some issues so hopefully there's not a lot of small test cases missed. 
2. If you're getting an index out of range error . Make sure there are no extra lines after last command. 



