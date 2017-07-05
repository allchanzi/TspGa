import csv

class Parser():
    def __init__(self, file):
        self.coords=[]
        coords = []
        with open(file) as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            coords = list(reader)
            print(coords)

        for i in coords:
            self.coords.append([float(i[0]), float(i[1])])



    def get_coords(self):
        return self.coords
"""
p = Parser("berlin52.csv")
p.get_coords()
"""