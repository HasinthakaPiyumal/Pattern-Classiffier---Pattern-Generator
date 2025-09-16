import time

class TrafficLight:
    def __init__(self, intersection_id):
        self._intersection_id = intersection_id
        self._current_color = "RED"
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def _notify(self):
        for observer in self._observers:
            observer.update(self._current_color)

    def change_color(self, new_color):
        if new_color != self._current_color:
            self._current_color = new_color.upper()
            print(f"Traffic Light {self._intersection_id} changed to {self._current_color}")
            self._notify()

class Vehicle:
    def __init__(self, vehicle_id):
        self._vehicle_id = vehicle_id

    def update(self, light_color):
        if light_color == "GREEN":
            print(f"Vehicle {self._vehicle_id}: Proceeding through intersection.")
        elif light_color == "RED":
            print(f"Vehicle {self._vehicle_id}: Stopping at intersection.")
        else: # YELLOW
            print(f"Vehicle {self._vehicle_id}: Preparing to stop/proceed with caution.")

if __name__ == "__main__":
    main_intersection_light = TrafficLight("Main St.")

    car1 = Vehicle("Car A")
    car2 = Vehicle("Car B")
    bus1 = Vehicle("Bus 1")

    main_intersection_light.attach(car1)
    main_intersection_light.attach(car2)
    main_intersection_light.attach(bus1)

    main_intersection_light.change_color("GREEN")
    time.sleep(1)
    main_intersection_light.change_color("YELLOW")
    time.sleep(1)
    main_intersection_light.change_color("RED")
    time.sleep(1)
    main_intersection_light.change_color("GREEN")