class Animal(object):
    def __init__(self, name):
        self.name = name


class Dog(Animal):
    def __init__(self, name):
        super(Dog, self).__init__(name)
        self.breed = 'Dog'


class Cat(Animal):
    def __init__(self, name):
        super(Cat, self).__init__(name)
        self.breed = 'Cat'


ins1 = Dog('John')
print(ins1.name)
print(ins1.breed)

ins2 = Cat('Jack')
print(ins2.name)
print(ins2.breed)
