
dict1 = {'Name' : 'trinh' ,'Age' : 21 , 'class' : 14 }
print("dict1['Name] :" , dict1['Name'])
dict1['Age'] = 20 #update a exist entry
dict1['School'] = 'VNU IS' #add a new entry
del dict1['Name']; # remove entry with key 'Name'
dict1.clear();     # remove all entries in dict
del dict1 ;        # delete entire dictionary
print ("dict1['Age']: ", dict1['Age'])
print ("dict['School']: ", dict1['School'])

dict2 = {['Name'] : 'Tung' , 'Age' : 21}
print(dict2['Name'])
cmp(dict1, dict2) #Compares elements of both dict.

len(dict1) #Gives the total length of the dictionary. This would be equal to the number of items in the dictionary.

str(dict1) #Produces a printable string representation of a dictionary

type(variable) #Returns the type of the passed variable. If passed variable is dictionary, then it would return a dictionary type

dict1.clear() #Removes all elements of dictionary dict

dict1.copy() #Returns a shallow copy of dictionary dict

dict1.fromkeys() #Create a new dictionary with keys from seq and values set to value.

dict1.get(key, default=None) #For key key, returns value or default if key not in dictionary

dict1.has_key(key) #Returns true if key in dictionary dict, false otherwise

dict1.items() #Returns a list of dict's (key, value) tuple pairs

dict1.keys() #Returns list of dictionary dict's keys

dict1.setdefault(key, default=None) #Similar to get(), but will set dict[key]=default if key is not already in dict

dict1.update(dict2) #Adds dictionary dict2's key-values pairs to dict

dict1.values() #Returns list of dictionary dict's values
