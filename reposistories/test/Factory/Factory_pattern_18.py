import abc

class Coffee(abc.ABC):
    @abc.abstractmethod
    def brew(self):
        pass

class Espresso(Coffee):
    def brew(self):
        return "Brewing a strong Espresso"

class Latte(Coffee):
    def brew(self):
        return "Brewing a creamy Latte"

class CoffeeFactory:
    @staticmethod
    def create_coffee(coffee_type: str) -> Coffee:
        if coffee_type == "espresso":
            return Espresso()
        elif coffee_type == "latte":
            return Latte()
        else:
            raise ValueError("Invalid coffee type")

if __name__ == "__main__":
    espresso = CoffeeFactory.create_coffee("espresso")
    print(espresso.brew())
    latte = CoffeeFactory.create_coffee("latte")
    print(latte.brew())