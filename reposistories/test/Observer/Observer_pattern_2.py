class WeatherData:
    def __init__(self):
        self._temperature = 0
        self._humidity = 0
        self._pressure = 0
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def _notify(self):
        for observer in self._observers:
            observer.update(self._temperature, self._humidity, self._pressure)

    def set_measurements(self, temperature, humidity, pressure):
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
        print(f"{self._name}: Current conditions: {self._temperature}°C and {self._humidity}% humidity.")

class ForecastDisplay:
    def __init__(self, name):
        self._name = name
        self._pressure = None

    def update(self, temperature, humidity, pressure):
        self._pressure = pressure
        if self._pressure > 1015:
            print(f"{self._name}: Forecast: Improving weather on the way!")
        else:
            print(f"{self._name}: Forecast: Watch out for cooler, rainy weather.")

if __name__ == "__main__":
    weather_data = WeatherData()

    current_display = CurrentConditionsDisplay("Current Display")
    forecast_display = ForecastDisplay("Forecast Display")

    weather_data.attach(current_display)
    weather_data.attach(forecast_display)

    weather_data.set_measurements(25, 65, 1020)
    weather_data.set_measurements(28, 70, 1005)
    weather_data.set_measurements(22, 60, 1018)