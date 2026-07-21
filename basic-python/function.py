def printme(str):
    print(str)
    return
printme("define function")

#Example for reference :
def changeme(list):
    list.append([4,5,6])
    print("values inside the function : ", list)
    return
list = [1,2,3]
changeme(list)
print("Values outside the function : ", list)    #change reference

def changeme( mylist ):
   list2 = [1,2,3,4]
   print ("Values inside the function: ", list2)
   return
list2 = [10,20,30];
changeme( list2 );
print ("Values outside the function: ", list2) #change list2 in function doesn't affect  list2

#Example for Agruments:
def printme( str ): #Required arguments(bat buoc)
   print (str)
   return;
printme('abc')

def printme( str ): #Keyword arguments(tu khoa)
   print (str)
   return;
printme( str = "My string")

def printinfo( name, age = 20 ): #Default function
   "This prints a passed info into this function"
   print ("Name: ", name)
   print ("Age ", age)
   return;
printinfo( age=40, name="Tung" )
printinfo( name="Tung" )

def printinfo(arg , *vartuples): #Variable-length argruments (ham co do dai bien doi)
    print("out put is : " , arg)
    for var in vartuples:
        print (var)
    return
printinfo(1)
printinfo(1 ,2, 3)    

#Example for the return Statement :
#parameters = 0 #global variables
def parameters( length, width ):
   parameters = length * width #local variables
   print ("Inside the function : ", parameters)
   return parameters
parameters(10 , 20)
print ("Outside the function : ", parameters) 