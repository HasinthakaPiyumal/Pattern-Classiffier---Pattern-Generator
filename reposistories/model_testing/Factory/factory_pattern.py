class Product:
    def operation(self):
        return "Product operation"

class ConcreteProductA(Product):
    def operation(self):
        return "ProductA operation"

class ConcreteProductB(Product):
    def operation(self):
        return "ProductB operation"

class Creator:
    def factory_method(self):
        pass
    def some_operation(self):
        product = self.factory_method()
        return product.operation()

class ConcreteCreatorA(Creator):
    def factory_method(self):
        return ConcreteProductA()

class ConcreteCreatorB(Creator):
    def factory_method(self):
        return ConcreteProductB()
