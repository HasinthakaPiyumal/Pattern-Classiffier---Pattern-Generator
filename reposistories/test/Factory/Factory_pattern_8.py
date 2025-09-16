class Coffee:
    def serve(self):
        raise NotImplementedError

class Espresso(Coffee):
    def serve(self):
        return "Serving a hot Espresso."

class Latte(Coffee):
    def serve(self):
        return "Serving a creamy Latte."

class Cappuccino(Coffee):
    def serve(self):
        return "Serving a frothy Cappuccino."

class CoffeeFactory:
    @staticmethod
    def get_coffee(coffee_type):
        if coffee_type == "espresso":
            return Espresso()
        elif coffee_type == "latte":
            return Latte()
        elif coffee_type == "cappuccino":
            return Cappuccino()
        else:
            raise ValueError("Invalid coffee type")

if __name__ == "__main__":
    espresso = CoffeeFactory.get_coffee("espresso")
    print(espresso.serve())
    latte = CoffeeFactory.get_coffee("latte")
    print(latte.serve())
    cappuccino = CoffeeFactory.get_coffee("cappuccino")
    print(cappuccino.serve())
    try:
        mocha = CoffeeFactory.get_coffee("mocha")
        print(mocha.serve())
    except ValueError as e:
        print(e)