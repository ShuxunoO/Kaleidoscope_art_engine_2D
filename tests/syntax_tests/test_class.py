class Cat:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def __str__(self):
        return "I am a cat, my name is " + str(self.name) + ", I am " + str(self.age) + " years old"

print(Cat("Tom", 2))