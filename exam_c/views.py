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


def exampage(request, exampage_id):
    try:
        exam_page = ExamPaper.objects.get(id=exampage_id)
    except ExamPaper.DoesNotExist:
        raise Http404("exam page {} does not exist".format(exampage_id))

    exam = exam_page.exam
    student = exam_page.student
    context = {
        'exam': exam,
        'student': student,
        'exam_page': exam_page,
        }
    return render(request, 'exam_c/exam_page.html', context)


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

            exam = Exam.objects.get(pk=exam_id)
            student = Student.objects.get(student_id=student_id)

            # 检查该考场和学号对应的试卷是否存在，不存在就创建新的
            # 同时随机抽取题目
            choice_question_numb, coding_question_numb = 10, 4
            if not ExamPaper.objects.filter(student=student, exam=exam).exists():
                exam_paper = ExamPaper.objects.create(student=student, exam=exam)
                exam_paper.problem_type = exam.problem_type
                exam_paper.start_time = datetime.datetime.now()

                choice_questions_ids = [str(x['id']) for x in ChoiceQuestion.objects.values('id')]
                choice_questions_ids = choice_questions_ids[:choice_question_numb]
                exam_paper.choice_questions = ','.join(choice_questions_ids)
                exam_paper.choice_question_answers = ','.join(['+' for i in range(len(choice_questions_ids))])
                # print('choice_questions_ids', choice_questions_ids)
                exam_paper.save()
            else:
                exam_paper = ExamPaper.objects.get(student=student, exam=exam)

            return HttpResponseRedirect(reverse('c:exampage', args=(exam_paper.id,)))
    else:
        form = StudentForm()

    context = {
        'form': form,
        }
    return render(request, 'exam_c/login.html', context)





@csrf_exempt
def handle_choice_ans_change(request):

    time = datetime.datetime.now()
    a = {}
    a["result"] = str(time) ##"post_success"
    return HttpResponse(json.dumps(a), content_type='application/json')