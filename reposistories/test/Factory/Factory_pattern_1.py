class Shape:
    def draw(self):
        raise NotImplementedError

class Circle(Shape):
    def draw(self):
        return "Drawing a Circle"

class Square(Shape):
    def draw(self):
        return "Drawing a Square"

class ShapeFactory:
    @staticmethod
    def get_shape(shape_type):
        if shape_type == "circle":
            return Circle()
        elif shape_type == "square":
            return Square()
        else:
            raise ValueError("Invalid shape type")

if __name__ == "__main__":
    circle = ShapeFactory.get_shape("circle")
    print(circle.draw())
    square = ShapeFactory.get_shape("square")
    print(square.draw())
    try:
        triangle = ShapeFactory.get_shape("triangle")
        print(triangle.draw())
    except ValueError as e:
        print(e)