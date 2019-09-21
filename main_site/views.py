from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import requests
import json
import csv
import os

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
        self.score_2018 = csv_row[3]
        self.score_lifetime = csv_row[4]

class HouseMember(Politician):
    def __init__(self, csv_row):
        self.district= csv_row[0]
        self.party = csv_row[1]
        self.name = csv_row[2]
        self.score_2018 = csv_row[3]
        self.score_lifetime = csv_row[4]

def get_senate_scores(state):
    pwd = os.path.dirname(__file__)
    with open(pwd + '/senate.csv') as senate_csv:
        csv_reader = csv.reader(senate_csv)
        senators = [Senator(row) for row in csv_reader]
        return list(filter(lambda x: x.state == state, senators))
        
def get_house_scores(district):
    pwd = os.path.dirname(__file__)
    with open(pwd + '/house.csv') as senate_csv:
        csv_reader = csv.reader(senate_csv)
        reps = [HouseMember(row) for row in csv_reader]
        return list(filter(lambda x: x.district == district, reps))

def civics_api(address):
    params = {
            'key': 'AIzaSyAqooD1FdQHijP32vQk95Af5geX0gofCME',
            'address': address
        }

    response = requests.get('https://www.googleapis.com/civicinfo/v2/representatives', params=params)
    return json.loads(response.text)


def index(request):
    template = loader.get_template('main_site/index.html')
    context = {

    }
    return HttpResponse(template.render(context, request))

def reps(request):
    template = loader.get_template('main_site/reps.html')
    address = request.POST.get('address')
    civics = civics_api(address)
    
    # Parse data from civics API
    state = civics['normalizedInput']['state']
    senate_scores = get_senate_scores(state)
    district = state + '-' + ''.join(c for c in civics['offices'][3]['name'] if c.isnumeric())
    house_scores = get_house_scores(district)
    # houseIndex = civics['offices'][3]['officialIndices'][0]


    context = {
      'senate_scores': senate_scores,
      'house_scores': house_scores
    }
    return HttpResponse(template.render(context, request))