from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def draw(self):
        pass

class Circle(Shape):
    def draw(self):
        return "Drawing a Circle"

class Square(Shape):
    def draw(self):
        return "Drawing a Square"

class Rectangle(Shape):
    def draw(self):
        return "Drawing a Rectangle"

class ShapeFactory:
    def get_shape(self, shape_type: str) -> Shape:
        if shape_type.lower() == "circle":
            return Circle()
        elif shape_type.lower() == "square":
            return Square()
        elif shape_type.lower() == "rectangle":
            return Rectangle()
        else:
            raise ValueError(f"Unknown shape type: {shape_type}")

if __name__ == "__main__":
    factory = ShapeFactory()
    shapes = ["circle", "square", "rectangle"]
    for s in shapes:
        shape_obj = factory.get_shape(s)
        print(shape_obj.draw())
