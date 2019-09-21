import csv

class Politician:
    name = None
    party = None
    score_2018 = None
    score_lifetime = None

    def __str__(self):
        return self.name + " (" + self.party + ")"

class Senator(Politician):
    def __init__(self, csv_row):
        self.state = csv_row[0]
        self.party = csv_row[1]
        self.name = csv_row[2]
        self.score_2019 = csv_row[3]
        self.score_lifetime = csv_row[4]

class HouseMember(Politician):
    def __init__(self, csv_row):
        self.district= csv_row[0]
        self.party = csv_row[1]
        self.name = csv_row[2]
        self.score_2019 = csv_row[3]
        self.score_lifetime = csv_row[4]

def get_senate_scores(state):
    with open('senate.csv') as senate_csv:
        csv_reader = csv.reader(senate_csv)
        senators = [Senator(row) for row in csv_reader]
        return list(filter(lambda x: x.state == state, senators))
        
def get_house_scores(district):
    with open('house.csv') as senate_csv:
        csv_reader = csv.reader(senate_csv)
        reps = [HouseMember(row) for row in csv_reader]
        return list(filter(lambda x: x.district == district, reps))

print(get_senate_scores('NY'))
print(get_house_scores("NY-23"))
