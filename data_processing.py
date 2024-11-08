import csv
import os


class Table:
    def __init__(self, table_name, table):
        self.table_name = table_name
        self.table = table

    def filter(self, condition):
        return [item for item in self.table if condition(item)]

    def aggregate(self, aggregation_key, aggregation_function):
        values = [float(item[aggregation_key]) for item in self.table if aggregation_key in item]
        return aggregation_function(values)

    def __str__(self):
        return f"Table: {self.table_name}, with {len(self.table)} entries"


class TableDB:
    def __init__(self):
        self.table_database = []

    def insert(self, table):
        if self.search(table.table_name) == -1:
            self.table_database.append(table)
        else:
            print(f"{table.table_name}: Duplicated table entry")

    def search(self, table_name):
        for table in self.table_database:
            if table.table_name == table_name:
                return table
        return -1


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


def load_csv_data(filename):
    filepath = os.path.join(__location__, filename)
    with open(filepath) as f:
        rows = csv.DictReader(f)
        return [dict(row) for row in rows]


cities = load_csv_data('Cities.csv')
countries = load_csv_data('Countries.csv')

cities_table = Table("cities", cities)
countries_table = Table("countries", countries)

db = TableDB()
db.insert(cities_table)
db.insert(countries_table)

cities_in_italy = cities_table.filter(lambda x: x['country'] == 'Italy')
cities_in_sweden = cities_table.filter(lambda x: x['country'] == 'Sweden')

cities_italy_table = Table("italy_cities", cities_in_italy)
cities_sweden_table = Table("sweden_cities", cities_in_sweden)

db.insert(cities_italy_table)
db.insert(cities_sweden_table)

avg_temp_italy = cities_italy_table.aggregate("temperature", lambda x: sum(x) / len(x))
print(f"The average temperature of all cities in Italy:\n{avg_temp_italy}\n")

avg_temp_sweden = cities_sweden_table.aggregate("temperature", lambda x: sum(x) / len(x))
print(f"The average temperature of all cities in Sweden:\n{avg_temp_sweden}\n")

min_temp_italy = cities_italy_table.aggregate("temperature", min)
print(f"The minimum temperature of all cities in Italy:\n{min_temp_italy}\n")

max_temp_sweden = cities_sweden_table.aggregate("temperature", max)
print(f"The maximum temperature of all cities in Sweden:\n{max_temp_sweden}\n")

max_latitude = cities_table.aggregate("latitude", max)
print("Maximum latitude for all cities:")
print(f"{max_latitude}\n")

min_latitude = cities_table.aggregate("latitude", min)
print("Minimum latitude for all cities:")
print(f"{min_latitude}\n")
