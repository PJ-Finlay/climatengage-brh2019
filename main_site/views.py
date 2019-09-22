from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
import requests
import json
import csv
import os

class Politician:
    name = None
    party = None
    score_2018 = None
    score_lifetime = None
    civics_info = None

    def __str__(self):
        return self.name + " (" + self.party + ")"

class Senator(Politician):
    def __init__(self, csv_row):
        self.state = csv_row[0]
        self.party = csv_row[1]
        self.name = csv_row[2]
        self.name = self.name.split(",")
        self.name = self.name[1] + " " + self.name[0]
        self.score_2018 = csv_row[3]
        self.score_lifetime = csv_row[4]

class HouseMember(Politician):
    def __init__(self, csv_row):
        self.district= csv_row[0]
        self.party = csv_row[1]
        self.name = csv_row[2]
        self.name = self.name.split(",")
        self.name = self.name[1] + " " + self.name[0]
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

def more_common_words(search, option1, option2):
  search = set(search.split(" "))
  option1 = set(option1.split(" "))
  option2 = set(option2.split(" "))
  return len(search and option1) > len(search and option2)

def index(request):
    is_error = request.GET.get('error')
    template = loader.get_template('main_site/index.html')
    context = {
      'is_error': is_error
    }
    return HttpResponse(template.render(context, request))

def reps(request):
    try:
      address = request.GET.get('address')
      civics = civics_api(address)
      
      # Parse data from civics API
      state = civics['normalizedInput']['state']
      senate_scores = get_senate_scores(state)

      house_available = False
      try:
        district = state + '-' + ''.join(c for c in civics['offices'][3]['name'] if c.isnumeric())
        house_scores = get_house_scores(district)
        houseIndex = civics['offices'][3]['officialIndices'][0]
        house_scores[0].civics_info = civics['officials'][houseIndex]
        house_available = True
      except:
        pass

      # Match senators up with their senate index
      senateIndices = civics['offices'][2]['officialIndices']
      senateCivics = [civics['officials'][senateIndex] for senateIndex in senateIndices]
      if more_common_words(senate_scores[0].name, senateCivics[0]['name'], senateCivics[1]['name']):
        senate_scores[0].civics_info = senateCivics[0]
        senate_scores[1].civics_info = senateCivics[1]
      else:
        senate_scores[0].civics_info = senateCivics[1]
        senate_scores[1].civics_info = senateCivics[0]


      context = {
        'senate_scores': senate_scores,
        'house_scores': house_scores,
        'house_available': house_available
      }
      template = loader.get_template('main_site/reps.html')
      return HttpResponse(template.render(context, request))
    except:
      return redirect('/?error=1')

def about(request):
    template = loader.get_template('main_site/about.html')
    context = {
    }
    return HttpResponse(template.render(context, request))