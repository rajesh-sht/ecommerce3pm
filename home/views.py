from django.shortcuts import render
from .models import *
# Create your views here.

class BaseView(View):
    views = {}

class HomeView(BaseView):
    def get(self,request):

        return render(request, 'index.html')