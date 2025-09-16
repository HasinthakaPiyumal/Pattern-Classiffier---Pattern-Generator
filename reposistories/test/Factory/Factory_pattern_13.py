import abc

class Vehicle(abc.ABC):
    @abc.abstractmethod
    def drive(self):
        pass

class Car(Vehicle):
    def drive(self):
        return "Driving a Car"

class Motorcycle(Vehicle):
    def drive(self):
        return "Riding a Motorcycle"

class VehicleFactory:
    @staticmethod
    def create_vehicle(vehicle_type: str) -> Vehicle:
        if vehicle_type == "car":
            return Car()
        elif vehicle_type == "motorcycle":
            return Motorcycle()
        else:
            raise ValueError("Invalid vehicle type")

if __name__ == "__main__":
    car = VehicleFactory.create_vehicle("car")
    print(car.drive())
    motorcycle = VehicleFactory.create_vehicle("motorcycle")
    print(motorcycle.drive())