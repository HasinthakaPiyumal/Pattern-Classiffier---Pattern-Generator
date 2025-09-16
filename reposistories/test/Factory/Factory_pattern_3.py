class Animal:
    def make_sound(self):
        raise NotImplementedError

class Dog(Animal):
    def make_sound(self):
        return "Woof!"

class Cat(Animal):
    def make_sound(self):
        return "Meow!"

class Cow(Animal):
    def make_sound(self):
        return "Moo!"

class AnimalFactory:
    @staticmethod
    def get_animal(animal_type):
        if animal_type == "dog":
            return Dog()
        elif animal_type == "cat":
            return Cat()
        elif animal_type == "cow":
            return Cow()
        else:
            raise ValueError("Invalid animal type")

if __name__ == "__main__":
    dog = AnimalFactory.get_animal("dog")
    print(dog.make_sound())
    cat = AnimalFactory.get_animal("cat")
    print(cat.make_sound())
    cow = AnimalFactory.get_animal("cow")
    print(cow.make_sound())
    try:
        bird = AnimalFactory.get_animal("bird")
        print(bird.make_sound())
    except ValueError as e:
        print(e)