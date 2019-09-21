from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


def index(request):
    template = loader.get_template('main_site/index.html')
    context = {

    }
    return HttpResponse(template.render(context, request))

def reps(request):
    template = loader.get_template('main_site/reps.html')
    context = {

    }
    return HttpResponse(template.render(context, request))