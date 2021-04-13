from django.shortcuts import render
from django.http import HttpResponse

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.http import Http404

from django.views.decorators.csrf import csrf_exempt
import json
import datetime

from .models import *
from .forms import StudentForm
# Create your views here.

def index(request):
    exam_list = Exam.objects.all()
    return render(request, 'exam_c/index.html')

def exampage(request, exam_id, student_id):
    exam_list = Exam.objects.all()
    return render(request, 'exam_c/index.html')

def exam_room(request, exam_id):
    try:
        exam = Exam.objects.get(id=exam_id)
    except Exam.DoesNotExist:
        raise Http404("exam does not exist")
    
    exam_papers = exam.exampaper_set.all()
    # for exam_paper in exam_papers:
        # print(exam_paper.student, exam_paper.student.id)
    context = {
        'exam': exam,
        'exam_id': exam_id,
        'exam_papers': exam_papers,
        }
    return render(request, 'exam_c/exam_room_detail.html', context)



@csrf_exempt
def handle_choice_ans_change(request):

    time = datetime.datetime.now()
    a = {}
    a["result"] = str(time) ##"post_success"
    return HttpResponse(json.dumps(a), content_type='application/json')



def login(request):

    if request.method == 'POST':
        # 如果登录成功，绑定参数到cookie中，set_cookie
        form = StudentForm(request.POST)

        if form.is_valid():
            cleaned_data = form.cleaned_data
            # print(cleaned_data)

            # 查询用户是否在数据库中
            exam_id = cleaned_data['exam_id']
            student_id = cleaned_data['student_id']

            return HttpResponseRedirect(reverse('c:exampage', args=(exam_id, student_id)))
    else:
        form = StudentForm()

    context = {
        'form': form,
        }
    return render(request, 'exam_c/login.html', context)