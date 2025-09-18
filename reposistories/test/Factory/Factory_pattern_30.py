class Meal:
    def prepare(self) -> str:
        pass
    def serve(self) -> str:
        pass

class Pizza(Meal):
    def prepare(self) -> str:
        return "Preparing a delicious pizza with toppings and cheese."
    def serve(self) -> str:
        return "Serving a hot, freshly baked pizza!"

class Burger(Meal):
    def prepare(self) -> str:
        return "Grilling a patty, assembling a burger with fresh veggies."
    def serve(self) -> str:
        return "Serving a juicy burger with fries!"

class Salad(Meal):
    def prepare(self) -> str:
        return "Washing greens, chopping vegetables, preparing a healthy salad."
    def serve(self) -> str:
        return "Serving a refreshing garden salad!"

class MealFactory:
    def create_meal(self, meal_type: str) -> Meal:
        if meal_type == "pizza":
            return Pizza()
        elif meal_type == "burger":
            return Burger()
        elif meal_type == "salad":
            return Salad()
        else:
            raise ValueError(f"Unknown meal type: {meal_type}")

factory = MealFactory()

pizza_order = factory.create_meal("pizza")
burger_order = factory.create_meal("burger")
salad_order = factory.create_meal("salad")

print(pizza_order.prepare())
print(pizza_order.serve())
print(burger_order.prepare())
print(burger_order.serve())
print(salad_order.prepare())
print(salad_order.serve())

try:
    pasta_order = factory.create_meal("pasta")
except ValueError as e:
    print(e)