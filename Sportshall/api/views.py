from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics
#from .serializers import SportSerializer
#from .models import Sport, Student, Registration

# Create your views here.
class SportView(generics.CreateAPIView):
    #queryset = Sport.objects.all()
    #serializer_class = SportSerializer
    pass
    
def main(request):
    return HttpResponse("<h1>Hello</h>")