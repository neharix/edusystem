from django.http import HttpRequest
from django.shortcuts import render


# Create your views here.
def main(request: HttpRequest):
    return render(request, "views/index.html")
