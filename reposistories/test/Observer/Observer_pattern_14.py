class TrafficLight:
    def __init__(self):
        self._observers = []
        self._current_color = "RED"

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def change_color(self, new_color):
        if new_color.upper() not in ["RED", "YELLOW", "GREEN"]:
            raise ValueError("Invalid traffic light color")
        self._current_color = new_color.upper()
        print(f"\nTraffic Light changed to: {self._current_color}")
        self.notify()

    def get_color(self):
        return self._current_color

    def notify(self):
        for observer in self._observers:
            observer.update(self._current_color)

class CarSensor:
    def __init__(self, location):
        self.location = location

    def update(self, color):
        if color == "GREEN":
            print(f"Car Sensor at {self.location}: Cars can proceed.")
        else:
            print(f"Car Sensor at {self.location}: Cars must stop.")

class PedestrianSensor:
    def __init__(self, location):
        self.location = location

    def update(self, color):
        if color == "RED":
            print(f"Pedestrian Sensor at {self.location}: Pedestrians can cross.")
        else:
            print(f"Pedestrian Sensor at {self.location}: Pedestrians must wait.")

if __name__ == '__main__':
    light = TrafficLight()
    car_sensor = CarSensor("Intersection A")
    ped_sensor = PedestrianSensor("Crosswalk B")

    light.attach(car_sensor)
    light.attach(ped_sensor)

    light.change_color("GREEN")
    light.change_color("YELLOW")
    light.change_color("RED")
    light.detach(car_sensor)
    light.change_color("GREEN")