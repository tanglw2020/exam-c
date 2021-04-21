from django.shortcuts import render
from django.http import HttpResponse

from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.urls import reverse
from django import forms
from django.http import Http404

from django.views.decorators.csrf import csrf_exempt
import json
import datetime
import time
import random

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
        return HttpResponseRedirect(reverse('c:login'))

    exam = exam_page.exam
    student = exam_page.student
    choice_question_ids = [int(x) for x in exam_page.choice_questions.split(',') if len(x)]
    choice_questions = []
    for i in choice_question_ids:
        choice_questions.append(ChoiceQuestion.objects.get(pk=i))

    coding_question_ids = [int(x) for x in exam_page.coding_questions.split(',') if len(x)]
    coding_questions = []
    for i in coding_question_ids:
        coding_questions.append(CodingQuestion.objects.get(pk=i))

    context = {
        'exam': exam,
        'student': student,
        'exam_page': exam_page,
        'choice_questions': choice_questions,
        'coding_questions': coding_questions,
        'choice_questions_answers': exam_page.choice_question_answers.split(','),
        'coding_questions_answers': exam_page.coding_question_answers.split(','),
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

            # 检查该考场和学号对应的试卷是否存在，不存在就创建新的试卷
            # 同时随机抽取题目
            choice_question_numb, coding_question_numb = 10, 2
            if not ExamPaper.objects.filter(student=student, exam=exam).exists():
                exam_paper = ExamPaper.objects.create(student=student, exam=exam)
                exam_paper.problem_type = exam.problem_type
                exam_paper.start_time = datetime.datetime.now()

                #########
                choice_questions_ids = [str(x['id']) for x in ChoiceQuestion.objects.values('id')]
                choice_questions_ids = random.sample(choice_questions_ids, choice_question_numb)
                exam_paper.choice_questions = ','.join(choice_questions_ids)
                exam_paper.choice_question_answers = ','.join(['+' for i in range(len(choice_questions_ids))])

                #########
                code_questions_ids = [str(x['id']) for x in CodingQuestion.objects.values('id')]
                code_questions_ids = random.sample(code_questions_ids, coding_question_numb)
                exam_paper.coding_questions = ','.join(code_questions_ids)
                exam_paper.coding_question_answers = ','.join(['+' for i in range(len(code_questions_ids))])
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
def api_choiceanswer(request, exampage_id):

    try:
        exam_page = ExamPaper.objects.get(id=exampage_id)
    except ExamPaper.DoesNotExist:
        raise Http404("exam page {} does not exist".format(exampage_id))
    return HttpResponse(json.dumps(a), content_type='application/json')


@csrf_exempt
def api_get_server_time(request, exampage_id):

    try:
        exam_page = ExamPaper.objects.get(id=exampage_id)
    except ExamPaper.DoesNotExist:
        a = {"result":"null"}
        return HttpResponse(json.dumps(a), content_type='application/json')

    diff = int(datetime.datetime.now().timestamp() - exam_page.start_time.timestamp())
    a = {}
    a["result"] = str(int(diff/60))+'min'+str(diff%60)+'s'  ##"post_success"
    return HttpResponse(json.dumps(a), content_type='application/json')


def api_download_scorelist(request, exam_id):
    try:
        exam = Exam.objects.get(id=exam_id)
    except Exam.DoesNotExist:
        raise Http404("exam does not exist")

    exam_papers = exam.exampaper_set.all()
    line_head ="#,班级,姓名,学号,开考时间"
    lines = [line_head]
    for i,exam_paper in enumerate(exam_papers):
        one_line = ','.join([str(i), exam_paper.student.class_name, exam_paper.student.student_name, 
        exam_paper.student.student_id, exam_paper.start_time_()])
        # print(one_line)
        lines.append(one_line)
    
    file_path = 'media/temp_scorelist/scorelist{}.txt'.format(exam_id)
    with open(file_path, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line+'\n')

    response = FileResponse(open(file_path, 'rb'))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="scorelist{}.txt"'.format(exam_id)
    return response