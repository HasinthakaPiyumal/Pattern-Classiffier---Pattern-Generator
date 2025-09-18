import random

class WeatherGenerator:
    def __init__(self, base_temp_range=(10.0, 25.0)):
        self._base_temp_range = base_temp_range

    def generate_data(self):
        temperature = random.uniform(*self._base_temp_range)
        return {"temperature_celsius": round(temperature, 2)}

class WeatherDecorator:
    def __init__(self, decorated_generator):
        self._decorated_generator = decorated_generator

    def generate_data(self):
        return self._decorated_generator.generate_data()

class HumidityDecorator(WeatherDecorator):
    def __init__(self, decorated_generator, humidity_range=(40.0, 90.0)):
        super().__init__(decorated_generator)
        self._humidity_range = humidity_range

    def generate_data(self):
        data = super().generate_data()
        humidity = random.uniform(*self._humidity_range)
        data["humidity_percent"] = round(humidity, 2)
        return data

class WindSpeedDecorator(WeatherDecorator):
    def __init__(self, decorated_generator, wind_range=(0.0, 30.0)):
        super().__init__(decorated_generator)
        self._wind_range = wind_range

    def generate_data(self):
        data = super().generate_data()
        wind_speed = random.uniform(*self._wind_range)
        data["wind_speed_kph"] = round(wind_speed, 2)
        return data

class PrecipitationDecorator(WeatherDecorator):
    def __init__(self, decorated_generator, precipitation_chance=0.3, max_mm=10.0):
        super().__init__(decorated_generator)
        self._precipitation_chance = precipitation_chance
        self._max_mm = max_mm

    def generate_data(self):
        data = super().generate_data()
        if random.random() < self._precipitation_chance:
            precipitation = random.uniform(0.1, self._max_mm)
            data["precipitation_mm"] = round(precipitation, 2)
        else:
            data["precipitation_mm"] = 0.0
        return data

if __name__ == "__main__":
    print("--- Basic Weather Data ---")
    base_generator = WeatherGenerator((15, 30))
    for _ in range(3):
        print(base_generator.generate_data())

    print("\n--- Weather Data with Humidity ---")
    humidity_generator = HumidityDecorator(base_generator, (50, 95))
    for _ in range(3):
        print(humidity_generator.generate_data())

    print("\n--- Full Weather Data Simulation (Temp, Humidity, Wind, Precipitation) ---")
    full_generator = PrecipitationDecorator(
        WindSpeedDecorator(
            HumidityDecorator(
                WeatherGenerator((5, 20)),
                (60, 100)
            ),
            (5, 50)
        ),
        precipitation_chance=0.5,
        max_mm=25.0
    )

    for i in range(5):
        print(f"Day {i+1}: {full_generator.generate_data()}")