class Thermometer:
    def __init__(self, location):
        self._location = location
        self._temperature = 20.0
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def _notify(self):
        for observer in self._observers:
            observer.update(self._temperature)

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, new_temp):
        if new_temp != self._temperature:
            self._temperature = new_temp
            print(f"Thermometer at {self._location}: Temperature changed to {self._temperature}°C")
            self._notify()

class HVACSystem:
    def __init__(self, name, desired_temp):
        self._name = name
        self._desired_temp = desired_temp

    def update(self, current_temp):
        if current_temp < self._desired_temp - 2:
            print(f"HVAC {self._name}: It's too cold ({current_temp}°C). Turning on heating.")
        elif current_temp > self._desired_temp + 2:
            print(f"HVAC {self._name}: It's too hot ({current_temp}°C). Turning on cooling.")
        else:
            print(f"HVAC {self._name}: Temperature ({current_temp}°C) is comfortable. System idle.")

class AlarmSystem:
    def __init__(self, high_threshold, low_threshold):
        self._high_threshold = high_threshold
        self._low_threshold = low_threshold

    def update(self, current_temp):
        if current_temp > self._high_threshold:
            print(f"ALARM SYSTEM: DANGER! Temperature ({current_temp}°C) is critically high!")
        elif current_temp < self._low_threshold:
            print(f"ALARM SYSTEM: WARNING! Temperature ({current_temp}°C) is critically low!")

if __name__ == "__main__":
    room_thermometer = Thermometer("Living Room")

    hvac_unit = HVACSystem("Main Unit", 22.0)
    fire_alarm = AlarmSystem(high_threshold=30.0, low_threshold=10.0)

    room_thermometer.attach(hvac_unit)
    room_thermometer.attach(fire_alarm)

    room_thermometer.temperature = 25.0
    room_thermometer.temperature = 18.0
    room_thermometer.temperature = 31.0
    room_thermometer.temperature = 22.0
    room_thermometer.temperature = 9.0