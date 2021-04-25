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
from pathlib import Path

from .models import *
from .forms import StudentForm, UploadOutputFileForm
# Create your views here.

BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT  = BASE_DIR / 'media'

def index(request):
    exam_list = Exam.objects.all()
    return render(request, 'exam_c/index.html')


def exampage(request, exampage_id):
    try:
        exam_page = ExamPaper.objects.get(id=exampage_id)
    except ExamPaper.DoesNotExist:
        return HttpResponseRedirect(reverse('c:login'))

    # coding_question_ids = [int(x) for x in exam_page.coding_questions.split(',') if len(x)]
    # coding_questions = []
    # for i in coding_question_ids:
    #     coding_questions.append(CodingQuestion.objects.get(pk=i))

    # 'choice_questions': exam_page.choice_questions_all_(),
    # 'coding_questions': coding_questions,

    context = {
        'exam': exam_page.exam,
        'student': exam_page.student,
        'exam_page': exam_page,
        'choice_questions_answers': exam_page.choice_question_answers_(),
        'coding_questions_answers': exam_page.coding_question_answers_(),
        }
    return render(request, 'exam_c/exam_page.html', context)

def exampage_choice_question(request, exampage_id, choice_question_id):
    try:
        exam_page = ExamPaper.objects.get(id=exampage_id)
    except ExamPaper.DoesNotExist:
        return HttpResponseRedirect(reverse('c:login'))

    context = {
        'exam': exam_page.exam,
        'student': exam_page.student,
        'exam_page': exam_page,
        'choice_questions_answers': exam_page.choice_question_answers_(),
        'coding_questions_answers': exam_page.coding_question_answers_(),
        'choice_question': exam_page.choice_questions_pk_(choice_question_id),
        'choice_question_id': choice_question_id,
        }
    return render(request, 'exam_c/exam_page_choice_question.html', context)


def handle_uploaded_file(f, output_save_path):
    # print(os.path.join(root_path,filename))
    with open(output_save_path, 'wb') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def exampage_coding_question(request, exampage_id, coding_question_id):
    try:
        exam_page = ExamPaper.objects.get(id=exampage_id)
    except ExamPaper.DoesNotExist:
        return HttpResponseRedirect(reverse('c:login'))

    coding_question = exam_page.coding_questions_pk_(coding_question_id)
    if request.method == 'POST':
        form = UploadOutputFileForm(request.POST, request.FILES)
        if form.is_valid():
            output_save_path = exam_page.coding_output_path_(coding_question_id)
            handle_uploaded_file(request.FILES['file'], output_save_path)
            ## update coding answers
            old_answers = exam_page.coding_question_answers.split(',')
            old_answers[coding_question_id-1] = str(output_save_path)
            exam_page.coding_question_answers = ','.join(old_answers)
            exam_page.save()
    else:
        form = UploadOutputFileForm()

    context = {
         'exam': exam_page.exam,
        'student': exam_page.student,
        'exam_page': exam_page,
        'choice_questions_answers': exam_page.choice_question_answers_(),
        'coding_questions_answers': exam_page.coding_question_answers_(),
        'coding_question': exam_page.coding_questions_pk_(coding_question_id),
        'coding_question_id': coding_question_id,
        'form': form,
        }
    return render(request, 'exam_c/exam_page_coding_question.html', context)



import socket
def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

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
        'login_url': get_host_ip()+':8000/c/login',
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
def api_get_server_time(request, exampage_id):

    try:
        exam_page = ExamPaper.objects.get(id=exampage_id)
    except ExamPaper.DoesNotExist:
        a = {"result":"null"}
        return HttpResponse(json.dumps(a), content_type='application/json')

    diff = int(datetime.datetime.now().timestamp() - exam_page.start_time.timestamp())
    a = {}
    a["result"] = str(int(diff/60))+'分钟'+str(diff%60)+'秒'  ##"post_success"
    return HttpResponse(json.dumps(a), content_type='application/json')

@csrf_exempt
def api_handle_choice_answer(request, exampage_id, choice_question_id, choice_id):

    try:
        exam_page = ExamPaper.objects.get(id=exampage_id)
    except ExamPaper.DoesNotExist:
        a = {"result":"null"}
        return HttpResponse(json.dumps(a), content_type='application/json')
    old_answers = exam_page.choice_question_answers.split(',')
    old_answers[choice_question_id-1] = str(choice_id)
    exam_page.choice_question_answers = ','.join(old_answers)
    exam_page.save()
    a = {}
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


@csrf_exempt
def api_download_coding_zipfile(request, exampage_id, coding_question_id):

    try:
        exam_page = ExamPaper.objects.get(id=exampage_id)
    except ExamPaper.DoesNotExist:
        a = {"result":"null"}
        return HttpResponse(json.dumps(a), content_type='application/json')
    
    coding_question_database_id = int(exam_page.coding_questions.split(',')[coding_question_id-1])
    coding_question = CodingQuestion.objects.get(pk=coding_question_database_id)

    file_path = coding_question.zip_path_()
    if file_path:
        response = FileResponse(open(file_path, 'rb'))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="coding{}.zip"'.format(coding_question_id)
        return response
    else:
        a = {"result":"null"}
        return HttpResponse(json.dumps(a), content_type='application/json')