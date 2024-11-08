import csv
import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


class City:
    def __init__(self, name, country, latitude, temperature):
        self.name = name
        self.country = country
        self.latitude = float(latitude)
        self.temperature = float(temperature)


class Country:
    def __init__(self, name):
        self.name = name
        self.cities = []

    def add_city(self, city):
        self.cities.append(city)

    def get_min_max_latitude(self):
        latitudes = [city.latitude for city in self.cities]
        if latitudes:
            return min(latitudes), max(latitudes)
        return None, None

    def get_avg_temperature(self):
        temps = [city.temperature for city in self.cities]
        if temps:
            return sum(temps) / len(temps)
        return None

    def get_min_temperature(self):
        temps = [city.temperature for city in self.cities]
        return min(temps) if temps else None

    def get_max_temperature(self):
        temps = [city.temperature for city in self.cities]
        return max(temps) if temps else None


class CityProcessor:
    def __init__(self, cities_file, countries_file):
        self.cities = []
        self.countries = {}
        self.load_data(cities_file, countries_file)

    def load_data(self, cities_file, countries_file):
        with open(cities_file) as f:
            rows = csv.DictReader(f)
            for row in rows:
                city = City(row['city'], row['country'], row['latitude'], row['temperature'])
                self.cities.append(city)
                if city.country not in self.countries:
                    self.countries[city.country] = Country(city.country)
                self.countries[city.country].add_city(city)

    def get_country_latitude_statistics(self):
        stats = {}
        for country_name, country in self.countries.items():
            min_lat, max_lat = country.get_min_max_latitude()
            stats[country_name] = {
                'min_latitude': min_lat,
                'max_latitude': max_lat
            }
        return stats

    def get_country_temperature_statistics(self, country_name):
        if country_name in self.countries:
            country = self.countries[country_name]
            return {
                'average_temperature': country.get_avg_temperature(),
                'min_temperature': country.get_min_temperature(),
                'max_temperature': country.get_max_temperature()
            }
        return None

    def filter_cities_by_latitude(self, min_latitude):
        return [city.name for city in self.cities if city.latitude >= min_latitude]


cities_file = os.path.join(__location__, 'Cities.csv')
countries_file = os.path.join(__location__, 'Countries.csv')
city_processor = CityProcessor(cities_file, countries_file)


# Print temperature statistics for Italy
italy_temp_stats = city_processor.get_country_temperature_statistics("Italy")
if italy_temp_stats:
    print("Temperature statistics for Italy:")
    print(f"Average Temperature = {italy_temp_stats['average_temperature']}")
    print(f"Min Temperature = {italy_temp_stats['min_temperature']}")
    print(f"Max Temperature = {italy_temp_stats['max_temperature']}")
print()

# Print temperature statistics for Sweden
sweden_temp_stats = city_processor.get_country_temperature_statistics("Sweden")
if sweden_temp_stats:
    print("Temperature statistics for Sweden:")
    print(f"Average Temperature = {sweden_temp_stats['average_temperature']}")
    print(f"Min Temperature = {sweden_temp_stats['min_temperature']}")
    print(f"Max Temperature = {sweden_temp_stats['max_temperature']}")
print()

# Print cities with latitude >= 60
high_latitude_cities = city_processor.filter_cities_by_latitude(60)
print("Cities with latitude >= 60:")
print(", ".join(high_latitude_cities))
