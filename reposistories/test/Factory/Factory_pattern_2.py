class Vehicle:
    def drive(self):
        raise NotImplementedError

class Car(Vehicle):
    def drive(self):
        return "Driving a Car"

class Bike(Vehicle):
    def drive(self):
        return "Riding a Bike"

class Truck(Vehicle):
    def drive(self):
        return "Driving a Truck"

class VehicleFactory:
    @staticmethod
    def get_vehicle(vehicle_type):
        if vehicle_type == "car":
            return Car()
        elif vehicle_type == "bike":
            return Bike()
        elif vehicle_type == "truck":
            return Truck()
        else:
            raise ValueError("Invalid vehicle type")

if __name__ == "__main__":
    car = VehicleFactory.get_vehicle("car")
    print(car.drive())
    bike = VehicleFactory.get_vehicle("bike")
    print(bike.drive())
    truck = VehicleFactory.get_vehicle("truck")
    print(truck.drive())
    try:
        boat = VehicleFactory.get_vehicle("boat")
        print(boat.drive())
    except ValueError as e:
        print(e)