import random
import time

class WeatherStation:
    def __init__(self):
        self._temperature = 0.0
        self._humidity = 0.0
        self._pressure = 0.0
        self._observers = []

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def _notify(self):
        for observer in self._observers:
            observer.update(self._temperature, self._humidity, self._pressure)

    def set_measurements(self, temperature, humidity, pressure):
        print(f"\nWeatherStation: New measurements received - Temp: {temperature:.1f}°C, Hum: {humidity:.1f}%, Pres: {pressure:.1f}hPa")
        self._temperature = temperature
        self._humidity = humidity
        self._pressure = pressure
        self._notify()

class CurrentConditionsDisplay:
    def __init__(self, name):
        self._name = name
        self._temperature = None
        self._humidity = None

    def update(self, temperature, humidity, pressure):
        self._temperature = temperature
        self._humidity = humidity
        print(f"Display ({self._name}): Current conditions - Temp: {self._temperature:.1f}°C, Hum: {self._humidity:.1f}%")

class WeatherAlertSystem:
    def __init__(self):
        self._last_temp = None

    def update(self, temperature, humidity, pressure):
        if self._last_temp is not None and abs(temperature - self._last_temp) > 5.0:
            print(f"ALERT SYSTEM: Significant temperature change detected! From {self._last_temp:.1f}°C to {temperature:.1f}°C")
        if temperature > 30.0 and humidity > 70.0:
            print(f"ALERT SYSTEM: Heatwave warning! Temp: {temperature:.1f}°C, Hum: {humidity:.1f}%")
        elif temperature < 0.0 and pressure < 990.0:
            print(f"ALERT SYSTEM: Potential for severe winter weather! Temp: {temperature:.1f}°C, Pres: {pressure:.1f}hPa")
        self._last_temp = temperature

class AgricultureIrrigationSystem:
    def __init__(self):
        self._irrigation_status = "OFF"

    def update(self, temperature, humidity, pressure):
        if humidity < 40.0 and self._irrigation_status == "OFF":
            self._irrigation_status = "ON"
            print(f"Irrigation System: Humidity low ({humidity:.1f}%). Turning irrigation ON.")
        elif humidity >= 60.0 and self._irrigation_status == "ON":
            self._irrigation_status = "OFF"
            print(f"Irrigation System: Humidity sufficient ({humidity:.1f}%). Turning irrigation OFF.")


weather_station = WeatherStation()

display1 = CurrentConditionsDisplay("Main")
display2 = CurrentConditionsDisplay("Backup")
alert_system = WeatherAlertSystem()
irrigation_system = AgricultureIrrigationSystem()

print("--- Simulation Start: Weather Station Alerts ---")

weather_station.attach(display1)
weather_station.attach(alert_system)
weather_station.attach(irrigation_system)

print("\n--- Initial measurements ---")
weather_station.set_measurements(25.0, 65.0, 1012.0)

print("\n--- Some time passes... ---")
time.sleep(1)
weather_station.set_measurements(27.5, 60.0, 1010.0)

print("\n--- Display 2 is added ---")
weather_station.attach(display2)
time.sleep(1)
weather_station.set_measurements(28.0, 55.0, 1009.0)

print("\n--- Weather gets hot and humid ---")
time.sleep(1)
weather_station.set_measurements(31.0, 75.0, 1008.0)

print("\n--- Humidity drops, triggering irrigation ---")
time.sleep(1)
weather_station.set_measurements(29.0, 35.0, 1011.0)

print("\n--- Temperature drops significantly ---")
time.sleep(1)
weather_station.set_measurements(5.0, 40.0, 1005.0)

print("\n--- Irrigation system detaches ---")
weather_station.detach(irrigation_system)
time.sleep(1)
weather_station.set_measurements(7.0, 70.0, 1000.0)

print("--- Simulation End ---")