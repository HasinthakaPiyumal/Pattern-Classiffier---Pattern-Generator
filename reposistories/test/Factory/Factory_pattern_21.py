class Vehicle:
    def assemble(self):
        pass

class Car(Vehicle):
    def assemble(self):
        return "Assembling a Car: Chassis, Engine, Four Wheels."

class Truck(Vehicle):
    def assemble(self):
        return "Assembling a Truck: Heavy Duty Chassis, Powerful Engine, Cargo Bed."

class Motorcycle(Vehicle):
    def assemble(self):
        return "Assembling a Motorcycle: Frame, Engine, Two Wheels."

class VehicleFactory:
    def create_vehicle(self, vehicle_type: str) -> Vehicle:
        if vehicle_type == "car":
            return Car()
        elif vehicle_type == "truck":
            return Truck()
        elif vehicle_type == "motorcycle":
            return Motorcycle()
        else:
            raise ValueError(f"Unknown vehicle type: {vehicle_type}")

factory = VehicleFactory()

car = factory.create_vehicle("car")
truck = factory.create_vehicle("truck")
motorcycle = factory.create_vehicle("motorcycle")

print(car.assemble())
print(truck.assemble())
print(motorcycle.assemble())

try:
    boat = factory.create_vehicle("boat")
except ValueError as e:
    print(e)