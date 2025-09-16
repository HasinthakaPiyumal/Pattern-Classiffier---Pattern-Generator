import abc

class Shape(abc.ABC):
    @abc.abstractmethod
    def draw(self):
        pass

class Circle(Shape):
    def draw(self):
        return "Drawing a Circle"

class Square(Shape):
    def draw(self):
        return "Drawing a Square"

class ShapeFactory:
    @staticmethod
    def create_shape(shape_type: str) -> Shape:
        if shape_type == "circle":
            return Circle()
        elif shape_type == "square":
            return Square()
        else:
            raise ValueError("Invalid shape type")

if __name__ == "__main__":
    circle = ShapeFactory.create_shape("circle")
    print(circle.draw())
    square = ShapeFactory.create_shape("square")
    print(square.draw())