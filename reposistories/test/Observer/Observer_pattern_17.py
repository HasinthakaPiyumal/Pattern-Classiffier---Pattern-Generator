class TemperatureSensor:
    def __init__(self, initial_temp=20):
        self._observers = []
        self._current_temperature = initial_temp

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def set_temperature(self, temp):
        print(f"\nSensor reading: {temp}°C")
        self._current_temperature = temp
        self.notify(temp)

    def notify(self, temp):
        for observer in self._observers:
            observer.update(temp)

class AlertSystem:
    def __init__(self, name, threshold):
        self.name = name
        self.threshold = threshold

    def update(self, temperature):
        if temperature > self.threshold:
            print(f"ALERT! {self.name}: Temperature ({temperature}°C) exceeds threshold ({self.threshold}°C)!")
        else:
            print(f"{self.name}: Temperature ({temperature}°C) is normal.")

if __name__ == '__main__':
    sensor = TemperatureSensor()
    high_temp_alert = AlertSystem("High Temp Monitor", 28)
    critical_temp_alert = AlertSystem("Critical Temp Monitor", 35)

    sensor.attach(high_temp_alert)
    sensor.attach(critical_temp_alert)

    sensor.set_temperature(25)
    sensor.set_temperature(30)
    sensor.set_temperature(38)
    sensor.detach(high_temp_alert)
    sensor.set_temperature(32)