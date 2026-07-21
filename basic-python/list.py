
list = ['abcd', 1 , 2.234 ]
tinylist = [123 ,  'hello']
list[0] =  2
print (list)
print (list[2])
print (list[1:3])
print (list + tinylist)
print(len([1, 2, 3]))	
print([1, 2, 3] + [4, 5, 6])	
print(['Hi!'] * 4)	
print(3 in [1, 2, 3])
for x in [1, 2, 3]: print (x)
cmp(list, tinylist) #Compares elements of both lists.

len(list) #Gives the total length of the list.

max(list) #Returns item from the list with max value.

min(list) #Returns item from the list with min value.

tuples =( 1 , 2 , 3)
list(tuples) #Converts a tuple into list.

list.append(obj) #Appends object obj to list

list.count(obj) #Returns count of how many times obj occurs in list

list.extend(seq) #Appends the contents of seq to list

list.index(obj) #Returns the lowest index in list that obj appears

list.insert(index, obj) #Inserts object obj into list at offset index

list.pop(obj=list[-1]) #Removes and returns last object or obj from list

list.remove(obj) #Removes object obj from list

list.reverse() #Reverses objects of list in place

list.sort([func]) #Sorts objects of list, use compare func if given