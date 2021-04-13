
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import datetime

from .models import Student, Exam

class StudentForm(forms.Form):
    exam_id = forms.IntegerField(label='考试编号')
    name = forms.CharField(label='姓名',  max_length=50)
    student_id = forms.IntegerField(label='学号')

    def clean(self):
        cleaned_data = super().clean()
        exam_id = cleaned_data['exam_id']
        student_id = str(cleaned_data['student_id'])

        if not Exam.objects.filter(id=exam_id).exists():
            self.add_error('exam_id', '考试编号不存在')
        if not Student.objects.filter(student_id=student_id).exists():
            self.add_error('student_id', '学号不存在')

            # if exam.pub_date < timezone.now() - datetime.timedelta(days=1):
            #     self.add_error('exam_id', '考试编号不是当天的')
        
