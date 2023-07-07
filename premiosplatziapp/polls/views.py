from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Main Page! Platzi Awards")


def detail(request, question_id):
    return HttpResponse(f"This is the Question #{question_id}")


def results(request, question_id):
    return HttpResponse(f"Here are the results of Question #{question_id}")


def vote(request, question_id):
    return HttpResponse(f"You're voting for Question #{question_id}")