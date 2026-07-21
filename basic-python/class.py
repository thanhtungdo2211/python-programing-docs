class Employee:
   'Common base class for all employees'
   empCount = 0

   def __init__(self, name, salary):
      self.name = name
      self.salary = salary
      Employee.empCount += 1
   
   def displayCount(self):
     print ("Total Employee %d" % Employee.empCount)

   def displayEmployee(self):
      print ("Name : ", self.name,  ", Salary: ", self.salary)
em1 = Employee("Tung" , 21)


class People :
    def __init__(self , name , age) :
        self.name = name
        self.age = age 

p1 = People("Do Thanh Tung" , 21)     
print(p1.name , p1.age)  

print(hasattr(p1 , 'name'))
print(getattr(p1 ,'name'))
setattr(p1 , 'name' , 'Do Thanh Binh')
print(p1.name)