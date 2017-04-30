import csv


def list_province_data():
    list_province = []
    with open('data/example.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            name = ' '.join(row[1].split(' ')[:-1])
            list_province.append((name.lower(), name))
        tup_province = tuple(list_province[1: -4])
        return tup_province
