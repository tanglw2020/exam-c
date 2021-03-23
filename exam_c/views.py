from django.shortcuts import render
from django.http import HttpResponse

from .models import *
# Create your views here.

def index(request):
    exam_list = Exam.objects.all()
    
    return render(request, 'exam_c/index.html')