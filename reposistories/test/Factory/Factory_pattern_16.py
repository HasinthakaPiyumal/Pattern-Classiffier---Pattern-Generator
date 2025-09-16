import abc

class Animal(abc.ABC):
    @abc.abstractmethod
    def make_sound(self):
        pass

class Dog(Animal):
    def make_sound(self):
        return "Woof!"

class Cat(Animal):
    def make_sound(self):
        return "Meow!"

class AnimalFactory:
    @staticmethod
    def create_animal(animal_type: str) -> Animal:
        if animal_type == "dog":
            return Dog()
        elif animal_type == "cat":
            return Cat()
        else:
            raise ValueError("Invalid animal type")

if __name__ == "__main__":
    dog = AnimalFactory.create_animal("dog")
    print(dog.make_sound())
    cat = AnimalFactory.create_animal("cat")
    print(cat.make_sound())