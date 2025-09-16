import abc

class Furniture(abc.ABC):
    @abc.abstractmethod
    def assemble(self):
        pass

class Chair(Furniture):
    def assemble(self):
        return "Assembling a Chair"

class Table(Furniture):
    def assemble(self):
        return "Assembling a Table"

class FurnitureFactory:
    @staticmethod
    def create_furniture(furniture_type: str) -> Furniture:
        if furniture_type == "chair":
            return Chair()
        elif furniture_type == "table":
            return Table()
        else:
            raise ValueError("Invalid furniture type")

if __name__ == "__main__":
    chair = FurnitureFactory.create_furniture("chair")
    print(chair.assemble())
    table = FurnitureFactory.create_furniture("table")
    print(table.assemble())