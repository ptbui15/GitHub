class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def changeAge(self,age):
        self.age = age    

class Student(Person):
    pass


testVariable = 5

def testFunc(num):
    print(num)

def testArgs(var1, **kwargs):
    print(var1.name)
    print(kwargs['test'])
    print(kwargs['test2'])