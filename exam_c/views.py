from django.shortcuts import render
from django.http import HttpResponse

from .models import *
# Create your views here.

def index(request):
    exam_list = Exam.objects.all()
    
    return render(request, 'exam_c/index.html')


def exam_detail(request, exam_id):
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
    return render(request, 'exam_c/exam_detail.html', context)


from django.views.decorators.csrf import csrf_exempt
import json
import datetime

@csrf_exempt
def handle_choice_ans_change(request):

  time = datetime.datetime.now()
  a = {}
  a["result"] = str(time) ##"post_success"
  return HttpResponse(json.dumps(a), content_type='application/json')