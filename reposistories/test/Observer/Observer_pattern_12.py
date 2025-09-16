class WeatherStation:
    def __init__(self):
        self._observers = []
        self._temperature = 0
        self._humidity = 0

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def set_measurements(self, temperature, humidity):
        self._temperature = temperature
        self._humidity = humidity
        self.notify()

    def get_temperature(self):
        return self._temperature

    def get_humidity(self):
        return self._humidity

    def notify(self):
        for observer in self._observers:
            observer.update(self)

class Display:
    def __init__(self, name):
        self.name = name
        self._temperature = None
        self._humidity = None

    def update(self, weather_station):
        self._temperature = weather_station.get_temperature()
        self._humidity = weather_station.get_humidity()
        self.display()

    def display(self_):
        print(f"Display {self_.name}: Temp {self_._temperature}°C, Humidity {self_._humidity}%")

if __name__ == '__main__':
    station = WeatherStation()
    display1 = Display("Living Room")
    display2 = Display("Kitchen")

    station.attach(display1)
    station.attach(display2)

    station.set_measurements(25, 60)
    station.set_measurements(26, 65)
    station.detach(display1)
    station.set_measurements(24, 58)