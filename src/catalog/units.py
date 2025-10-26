from json import load


UNITS = []
# This should be a database in the future
with open("static/data/models.json", encoding="utf-8") as data_file:
    UNITS = load(data_file)
