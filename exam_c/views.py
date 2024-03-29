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
from .forms import StudentForm, UploadOutputFileForm, StudentFormSecondLogin, CompleteForm
# Create your views here.

BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT  = BASE_DIR / 'media'

# def index(request):
#     exam_list = Exam.objects.all()
#     return render(request, 'exam_c/index.html')


def exampage(request, exampage_id):
    try:
        exam_page = ExamPaper.objects.get(unique_key=exampage_id)
    except ExamPaper.DoesNotExist:
        return HttpResponseRedirect(reverse('c:login'))

    question_links = []
    for a in exam_page.choice_question_answers_():
        if a=='+': question_links.append('btn btn-light')
        else: question_links.append('btn btn-success')
    context = {
        'exam': exam_page.exam,
        'student': exam_page.student,
        'question_links': question_links,
        'exam_page': exam_page,
        'choice_questions_answers': exam_page.choice_question_answers_(),
        'coding_questions_answers': exam_page.coding_question_answers_(),
        }
    return render(request, 'exam_c/exam_page.html', context)

def exampage_choice_question(request, exampage_id, choice_question_id):
    try:
        exam_page = ExamPaper.objects.get(unique_key=exampage_id)
    except ExamPaper.DoesNotExist:
        return HttpResponseRedirect(reverse('c:login'))

    choice_question_id = 1  # fix the id 
    question_links = []
    # for a in exam_page.choice_question_answers_():
    #     if a=='+': question_links.append('btn btn-light')
    #     else: question_links.append('btn btn-success')
    # question_links[choice_question_id-1] = 'btn btn-primary'
    current_choice = exam_page.choice_question_answers_()[choice_question_id-1]
    if current_choice=='+': current_choice=''
    context = {
        'exam': exam_page.exam,
        'student': exam_page.student,
        'exam_page': exam_page,
        'question_links': question_links,
        'current_choice': current_choice,
        'choice_question': exam_page.choice_questions_pk_(choice_question_id),
        'choice_question_id': choice_question_id,
        }
    return render(request, 'exam_c/exam_page_choice_question.html', context)


def exampage_complete_question(request, exampage_id, question_id):
    try:
        exam_page = ExamPaper.objects.get(unique_key=exampage_id)
    except ExamPaper.DoesNotExist:
        return HttpResponseRedirect(reverse('c:login'))
    
    uploadsucc = False
    question = exam_page.complete_questions_pk_(question_id)
    if request.method == 'POST':
        form = CompleteForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            answers = [cleaned_data['position1'], cleaned_data['position2'],cleaned_data['position3'] ]
            print("answers: ", answers)
            exam_page.update_complete_question_answer_result_(question_id, answers)
            uploadsucc = True
    else:
        answers = exam_page.complete_question_answers_()[question_id-1].split(',')
        if len(answers) == 3:
            data = {'position1': answers[0], 
                    'position2': answers[1], 
                    'position3': answers[2],
                    }
            form = CompleteForm(data)
        else:
            form = CompleteForm()

    if (not exam_page.enabled) or (not exam_page.choice_question_finished):
        form.fields['position1'].widget.attrs['disabled'] = True
        form.fields['position2'].widget.attrs['disabled'] = True
        form.fields['position3'].widget.attrs['disabled'] = True

    context = {
        'exam_page': exam_page,
        'question': question,
        'question_id': question_id,
        'uploadsucc': uploadsucc,
        'form': form,
        }
    return render(request, 'exam_c/exam_page_complete_question.html', context)


def handle_uploaded_file(f, output_save_path):
    # print(os.path.join(root_path,filename))
    with open(output_save_path, 'wb') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def exampage_coding_question(request, exampage_id, coding_question_id):
    try:
        exam_page = ExamPaper.objects.get(unique_key=exampage_id)
    except ExamPaper.DoesNotExist:
        return HttpResponseRedirect(reverse('c:login'))
    
    uploadsucc = False
    coding_question = exam_page.coding_questions_pk_(coding_question_id)
    if request.method == 'POST':
        form = UploadOutputFileForm(request.POST, request.FILES)
        if form.is_valid():
            output_save_path = exam_page.coding_output_path_(coding_question_id)
            handle_uploaded_file(request.FILES['file'], output_save_path)
            ## update coding answers
            # old_answers = exam_page.coding_question_answers.split(',')
            # old_answers[coding_question_id-1] = str(output_save_path)
            # exam_page.coding_question_answers = ','.join(old_answers)
            # exam_page.save()
            exam_page.update_coding_question_answer_result_(coding_question_id, output_save_path)
            uploadsucc = True
    else:
        form = UploadOutputFileForm()
    if (not exam_page.enabled) or (not exam_page.choice_question_finished):
        form.fields['file'].widget.attrs['disabled'] = True

    context = {
        'exam': exam_page.exam,
        'student': exam_page.student,
        'exam_page': exam_page,
        'coding_questions_answers': exam_page.coding_question_answers_(),
        'coding_question': exam_page.coding_questions_pk_(coding_question_id),
        'coding_question_id': coding_question_id,
        'uploadsucc': uploadsucc,
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
    
    exam_papers = exam.exampaper_set.order_by('student_id')
    # for exam_paper in exam_papers:
        # print(exam_paper.student, exam_paper.student.id)
    context = {
        'exam': exam,
        'exam_id': exam_id,
        'exam_papers': exam_papers,
        'login_url': 'http://'+get_host_ip()+':8000/c',
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
            unique_key = str(exam_id)+'-'+str(student_id)

            exam = Exam.objects.get(pk=exam_id)
            student = Student.objects.get(student_id=student_id)

            # 检查该考场和学号对应的试卷是否存在，不存在就创建新的试卷
            # 同时随机抽取题目
            choice_question_numb, coding_question_numb = exam.choice_question_num, exam.coding_question_num
            exam_paper, created = ExamPaper.objects.get_or_create(student=student, exam=exam, unique_key=unique_key)
            if created or exam_paper.is_empty_():
                exam_paper.problem_type = exam.problem_type
                exam_paper.start_time = datetime.datetime.now()

                exam_paper.student_id_local = student_id
                exam_paper.exam_id_local = exam_id

                #########
                choice_questions_ids = [str(x['id']) for x in ChoiceQuestion.objects.values('id')]
                choice_questions_ids = random.sample(choice_questions_ids, choice_question_numb)
                exam_paper.choice_questions = ','.join(choice_questions_ids)
                exam_paper.choice_question_answers = ','.join(['+' for i in range(len(choice_questions_ids))])
                exam_paper.choice_question_results = ','.join(['0' for i in range(len(choice_questions_ids))])

                #########
                complete_questions_ids = [str(x['id']) for x in CompleteQuestion.objects.values('id')]
                complete_questions_ids = random.sample(complete_questions_ids, exam.complete_question_num)
                exam_paper.complete_questions = ','.join(complete_questions_ids)
                exam_paper.complete_question_answers = '\n'.join(['#' for i in range(len(complete_questions_ids))])
                exam_paper.complete_question_results = ','.join(['0' for i in range(len(complete_questions_ids))])

                #########
                code_questions_ids = [str(x['id']) for x in CodingQuestion.objects.values('id')]
                code_questions_ids = random.sample(code_questions_ids, coding_question_numb)
                exam_paper.coding_questions = ','.join(code_questions_ids)
                exam_paper.coding_question_answers = ','.join(['+' for i in range(len(code_questions_ids))])
                exam_paper.coding_question_results = ','.join(['0' for i in range(len(code_questions_ids))])
                exam_paper.save()

            diff = int(timezone.now().timestamp() - exam_paper.start_time.timestamp())
            if diff<60: 
                return HttpResponseRedirect(reverse('c:exampage', args=(exam_paper.unique_key,)))
            else:
                return HttpResponseRedirect(reverse('c:login-second', args=(exam_paper.unique_key,)))
    else:
        form = StudentForm()

    context = {
        'form': form,
        }
    return render(request, 'exam_c/login.html', context)


def login_second(request, exampage_id):

    try:
        exam_page = ExamPaper.objects.get(unique_key=exampage_id)
    except ExamPaper.DoesNotExist:
        raise Http404("exampaper {} does not exist".format(exampage_id))

    if request.method == 'POST':
        form = StudentFormSecondLogin(request.POST)

        if form.is_valid():
            cleaned_data = form.cleaned_data

            # 查询用户是否在数据库中
            exam_id = cleaned_data['exam_id']
            student_id = cleaned_data['student_id']
            unique_key = str(exam_id)+'-'+str(student_id)
            return HttpResponseRedirect(reverse('c:exampage', args=(unique_key,)))
    else:
        data = {'exam_id': exam_page.exam_id_local, 
                'student_id': exam_page.student_id_local, 
                'password': '',
                'name': exam_page.student.student_name, 
                }
        form = StudentFormSecondLogin(data)

    context = {
        'form': form,
        }
    return render(request, 'exam_c/login_second.html', context)



@csrf_exempt
def api_get_server_time(request, exampage_id):

    try:
        exam_page = ExamPaper.objects.get(unique_key=exampage_id)
    except ExamPaper.DoesNotExist:
        a = {"result":"null"}
        return HttpResponse(json.dumps(a), content_type='application/json')

    # start_time = exam_page.start_time.replace(tzinfo=None)
    diff = int(timezone.now().timestamp() - exam_page.start_time.timestamp())
    if not exam_page.enabled:
        diff = 0
    elif exam_page.exam.period == '2':
        diff = (90+exam_page.add_time)*60 - diff
    elif exam_page.exam.period == '1':
        diff = (120+exam_page.add_time)*60 - diff

    a = {}
    a["refresh"] = 0
    a["color"] = 'black'
    if diff < 60*5: 
        a["color"] = 'red'
    if diff < 0:  
        diff = 0
        if exam_page.enabled:
            exam_page.disable_()
            a["refresh"] = 1  

    a["result"] = str(int(diff/60))+'分钟'+str(diff%60)+'秒'  ##"post_success"
    return HttpResponse(json.dumps(a), content_type='application/json')

@csrf_exempt
def api_handle_choice_answer(request, exampage_id, choice_question_id, choice_id):

    try:
        exam_page = ExamPaper.objects.get(unique_key=exampage_id)
    except ExamPaper.DoesNotExist:
        a = {"result":"null"}
        return HttpResponse(json.dumps(a), content_type='application/json')
    # old_answers = exam_page.choice_question_answers.split(',')
    # old_answers[choice_question_id-1] = str(choice_id)
    # exam_page.choice_question_answers = ','.join(old_answers)
    # exam_page.save()
    exam_page.update_choice_question_answer_result_(choice_question_id, choice_id)
    a = {}
    return HttpResponse(json.dumps(a), content_type='application/json')


@csrf_exempt
def api_get_choice_text(request, exampage_id, choice_question_id):

    try:
        exam_page = ExamPaper.objects.get(unique_key=exampage_id)
    except ExamPaper.DoesNotExist:
        a = {"result":"null"}
        return HttpResponse(json.dumps(a), content_type='application/json')
    question = exam_page.choice_questions_pk_(choice_question_id)
    question_text = question.question_text.replace('\n','<br>')
    answer = exam_page.choice_question_answers_()[choice_question_id-1]
    if answer == '+': answer = ''
    a = {"result": question_text, 
        "choice1":question.choice_1, 
        "choice2":question.choice_2, 
        "choice3":question.choice_3, 
        "choice4":question.choice_4, 
        "answer": answer
        }
    return HttpResponse(json.dumps(a), content_type='application/json')



@csrf_exempt
def api_get_choice_status(request, exampage_id):

    try:
        exam_page = ExamPaper.objects.get(unique_key=exampage_id)
    except ExamPaper.DoesNotExist:
        a = {"result":"null"}
        return HttpResponse(json.dumps(a), content_type='application/json')
    a = {"result": exam_page.choice_question_answers,}
    return HttpResponse(json.dumps(a), content_type='application/json')

@csrf_exempt
def api_set_choice_finished(request, exampage_id):

    try:
        exam_page = ExamPaper.objects.get(unique_key=exampage_id)
    except ExamPaper.DoesNotExist:
        a = {"result":"null"}
        return HttpResponse(json.dumps(a), content_type='application/json')
    exam_page.choice_question_finished = True
    exam_page.save()
    a = {"result": "ok"}
    return HttpResponse(json.dumps(a), content_type='application/json')


@csrf_exempt
def api_download_scorelist(request, exam_id):
    try:
        exam = Exam.objects.get(id=exam_id)
    except Exam.DoesNotExist:
        raise Http404("exam does not exist")

    exam_papers = exam.exampaper_set.all()
    line_head ="编号 班级 姓名 学号 选择题 填空题 编程题 总分"
    lines = [line_head]
    for i,exam_paper in enumerate(exam_papers):
        one_line = ' '.join([str(i), exam_paper.student.class_name, exam_paper.student.student_name, 
        exam_paper.student.student_id,
        str(exam_paper.choice_question_result_detail()).replace(' ',''),
        str(exam_paper.complete_question_result_detail()).replace(' ',''),
        str(exam_paper.coding_question_result_detail()).replace(' ',''),
        str(exam_paper.total_score()) ])
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
        exam_page = ExamPaper.objects.get(unique_key=exampage_id)
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



@csrf_exempt
def api_submit_all(request, exampage_id):

    try:
        exam_page = ExamPaper.objects.get(unique_key=exampage_id)
    except ExamPaper.DoesNotExist:
        a = {"result":"null"}
        return HttpResponse(json.dumps(a), content_type='application/json')
    
    if exam_page.enabled:
        exam_page.disable_()
    a = {"result":"null"}
    return HttpResponse(json.dumps(a), content_type='application/json')


@csrf_exempt
def add_time_enable(request, exampage_id):

    try:
        exam_page = ExamPaper.objects.get(unique_key=exampage_id)
    except ExamPaper.DoesNotExist:
        a = {"result":"null"}
        return HttpResponse(json.dumps(a), content_type='application/json')
    
    exam_page.add_time_enable_(3)
    a = {"result":"null"}
    return HttpResponse(json.dumps(a), content_type='application/json')