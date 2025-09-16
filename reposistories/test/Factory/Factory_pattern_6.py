class Furniture:
    def assemble(self):
        raise NotImplementedError

class Chair(Furniture):
    def assemble(self):
        return "Assembling a Chair."

class Table(Furniture):
    def assemble(self):
        return "Assembling a Table."

class Sofa(Furniture):
    def assemble(self):
        return "Assembling a Sofa."

class FurnitureFactory:
    @staticmethod
    def get_furniture(furniture_type):
        if furniture_type == "chair":
            return Chair()
        elif furniture_type == "table":
            return Table()
        elif furniture_type == "sofa":
            return Sofa()
        else:
            raise ValueError("Invalid furniture type")

if __name__ == "__main__":
    chair = FurnitureFactory.get_furniture("chair")
    print(chair.assemble())
    table = FurnitureFactory.get_furniture("table")
    print(table.assemble())
    sofa = FurnitureFactory.get_furniture("sofa")
    print(sofa.assemble())
    try:
        bed = FurnitureFactory.get_furniture("bed")
        print(bed.assemble())
    except ValueError as e:
        print(e)