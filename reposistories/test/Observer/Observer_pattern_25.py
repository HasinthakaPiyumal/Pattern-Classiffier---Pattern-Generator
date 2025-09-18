class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update(self)

class TemperatureSensor(Subject):
    def __init__(self, location, initial_temp):
        super().__init__()
        self.location = location
        self._temperature = initial_temp

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        if self._temperature != value:
            print(f"Smart Home: Sensor at {self.location}: Temperature changed from {self._temperature}°C to {value}°C")
            self._temperature = value
            self.notify()

class ThermostatController:
    def __init__(self, target_temp):
        self.target_temp = target_temp

    def update(self, sensor):
        print(f"Smart Home: Thermostat: Sensor at {sensor.location} reports {sensor.temperature}°C.")
        if sensor.temperature < self.target_temp - 1:
            print(f"Smart Home: Thermostat: Turning on heating to reach {self.target_temp}°C.")
        elif sensor.temperature > self.target_temp + 1:
            print(f"Smart Home: Thermostat: Turning on cooling to reach {self.target_temp}°C.")
        else:
            print(f"Smart Home: Thermostat: Temperature is within acceptable range of {self.target_temp}°C.")

class SmartDisplay:
    def update(self, sensor):
        print(f"Smart Home: Display: Showing {sensor.location} temperature: {sensor.temperature}°C")

class DataLogger:
    def update(self, sensor):
        print(f"Smart Home: Data Logger: Recorded temperature {sensor.temperature}°C from {sensor.location}.")

room_sensor = TemperatureSensor("Living Room", 22.0)

thermostat = ThermostatController(24.0)
smart_display = SmartDisplay()
data_logger = DataLogger()

room_sensor.attach(thermostat)
room_sensor.attach(smart_display)
room_sensor.attach(data_logger)

print("--- Smart Home Simulation: Initial Temperature ---")
room_sensor.temperature = 22.0

print("\n--- Smart Home Simulation: Temperature drops ---")
room_sensor.temperature = 20.5

print("\n--- Smart Home Simulation: Temperature rises ---")
room_sensor.temperature = 25.0

print("\n--- Smart Home Simulation: Detach display, temperature stabilizes ---")
room_sensor.detach(smart_display)
room_sensor.temperature = 23.8

print("\n--- Smart Home Simulation: Temperature drops again ---")
room_sensor.temperature = 19.9