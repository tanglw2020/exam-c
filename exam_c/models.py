
# -*- coding: utf-8 -*-
from django.db import models
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html, format_html_join
import re
# Create your models here.

EXAM_TYPE_CHOICES = [
    ('1','C语言'),
    ('2','C++'),
    ('3','Java'),
    ('4','Python'),
]

PERIOD_CHOICES = [
    ('1','120分钟'),
    ('2','90分钟'),
]

ANSWER_CHOICES = [
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
]


class Exam(models.Model):
    class Meta:
        verbose_name = '考试场次'
        verbose_name_plural = '考试场次'
    pub_date = models.DateTimeField('创建时间', 'date published', null=True)
    problem_type = models.CharField("试卷类型", max_length=20, choices=EXAM_TYPE_CHOICES, default='1')
    info_text = models.CharField('考试信息', max_length=200)
    period = models.CharField("考试时长", max_length=5, choices=PERIOD_CHOICES, default='1')

    def __str__(self):
        return str(self.id) + ' ' +self.info_text

    def id_(self):
        return str(self.id)
    id_.short_description = '考试编号'


class Student(models.Model):
    class Meta:
        verbose_name = '考生'
        verbose_name_plural = '考生'
    class_name = models.CharField('班级',max_length=20, default='')
    student_name = models.CharField('姓名', max_length=20, default='')
    student_id = models.CharField('学号', max_length=20, default='')
    pass_word = models.CharField('密码', max_length=20, default='', blank=True)

    # current_exam_id = models.CharField('当前考试编号', max_length=20, default='', blank=True)
    # current_paper_id = models.CharField('当前试卷编号', max_length=20, default='', blank=True)

    def __str__(self):
        return self.class_name+" "+self.student_name +" "+self.student_id


class ExamPaper(models.Model):
    class Meta:
        verbose_name = '试卷'
        verbose_name_plural = '试卷'

    def __str__(self):
        return '试卷'+str(self.id)

    problem_type = models.CharField("试卷类型", max_length=20, choices=EXAM_TYPE_CHOICES, default='1')
    student_id = models.ForeignKey(
        Student,
        on_delete=models.CASCADE, null=True,
        verbose_name='所属考生'
    ) 
    exam_id = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE, null=True,
        verbose_name='所属考试'
    ) 

    start_time = models.DateTimeField('开考时间', null=True, blank=True,)

    choice_questions = models.TextField("选择题列表", max_length=1000,  blank=True, default='')
    choice_question_answers = models.TextField("选择题答案列表", max_length=1000, blank=True,  default='')

    coding_questions = models.TextField("编程题列表", max_length=1000, blank=True, default='')
    coding_question_answers = models.TextField("编程题答案列表", max_length=1000, blank=True, default='')

    def start_time_(self):
        return str(self.start_time)
    start_time_.short_description = '开考时间'


class ChoiceQuestion(models.Model):
    class Meta:
        verbose_name = '选择题'
        verbose_name_plural = '选择题'

    def __str__(self):
        return '题'+str(self.id)

    problem_type = models.CharField("试卷类型", max_length=20, choices=EXAM_TYPE_CHOICES, default='1')

    question_text = models.TextField('题干')
    choice_1 = models.CharField('选项1', max_length=200,  default='')
    choice_2 = models.CharField('选项2', max_length=200,  default='')
    choice_3 = models.CharField('选项3', max_length=200,  default='')
    choice_4 = models.CharField('选项4', max_length=200,  default='')

    answer = models.CharField("正确选项", max_length=2, choices=ANSWER_CHOICES, default='1')

    def question_html_(self):
        question_text = [x for x in self.question_text.split('\n')]
        return format_html_join(
                '', '<p style="color:{};">{}</p>',
                (('black', x) for x in question_text)
                )
    question_html_.short_description = '题目'

    def answer_list_(self):
        choice_list = [
            ['white', 'A. '+ self.choice_1], 
            ['white', 'B. '+  self.choice_2], 
            ['white', 'C. '+  self.choice_3], 
            ['white', 'D. '+  self.choice_4], 
            ]
        choice_list[int(self.answer)-1][0] = 'Lime'

        return format_html("<ul>") + \
                format_html_join(
                '\n', '<li style="background-color:{};">{}</li>',
                ((x[0], x[1]) for x in choice_list)
                ) \
                + format_html("</ul>")
    answer_list_.short_description = '题目选项'


def validate_zipfile(value):
    extension = value.name.split('.')[-1]
    if extension not in ['zip',]:
        raise ValidationError(
            _(value.name+'不是zip压缩文件'),
            params={'value': value.name},
        )

def validate_txtfile(value):
    extension = value.name.split('.')[-1]
    if extension not in ['txt',]:
        raise ValidationError(
            _(value.name+'不是txt文件'),
            params={'value': value.name},
        )

def validate_cfile(value):
    extension = value.name.split('.')[-1]
    if extension not in ['c',]:
        raise ValidationError(
            _(value.name+'不是c文件'),
            params={'value': value.name},
        )

class CodingQuestion(models.Model):
    class Meta:
        verbose_name = '编程题'
        verbose_name_plural = '编程题'

    def __str__(self):
        return '题'+str(self.id)

    problem_type = models.CharField("试卷类型", max_length=20, choices=EXAM_TYPE_CHOICES, default='1')
    question_text = models.TextField('题目简介', )
    # upload_zipfile = models.FileField(upload_to='upload_zipfile/', null=True, blank=True, 
    # validators=[validate_zipfile], verbose_name='上传题目文件zip压缩包')

    upload_description_file = models.FileField(upload_to='upload_c_file/', null=True, blank=True, 
    validators=[validate_txtfile], verbose_name='上传题目描述[.txt文件]')

    upload_c_file = models.FileField(upload_to='upload_c_file/', null=True, blank=True, 
    validators=[validate_cfile], verbose_name='上传C文件[.c文件]')

    upload_input_file = models.FileField(upload_to='upload_answer_file/', null=True, blank=True, 
    validators=[validate_txtfile], verbose_name='上传题目输入[.txt文件]')

    upload_answer_file = models.FileField(upload_to='upload_answer_file/', null=True, blank=True, 
    validators=[validate_txtfile], verbose_name='上传题目输出[.txt文件]')

    def question_html_(self):
        # print(self.upload_description_file, type(self.upload_description_file))
        try:
        # if self.upload_description_file is not None:
            with open(self.upload_description_file.path,'r', encoding='utf-8') as f:
                lines = f.readlines()
                return format_html_join(
                        '', '<p style="color:{};">{}</p>',
                        (('black', x) for x in lines)
                        )
        except:
        # else:
            return ''
        # return ''
    question_html_.short_description = '题目'


    def code_html_(self):
        # if self.upload_c_file is not None:
        try:
            with open(self.upload_c_file.path,'r', encoding='utf-8') as f:
                lines = f.readlines()
                return format_html_join(
                        '', '<p style="color:{};">{}</p>',
                        (('black', x) for x in lines)
                        )
        # else:
        except:
            return ''
        # return ''
    code_html_.short_description = '代码'


# class CompletionQuestion(models.Model):
#     class Meta:
#         verbose_name = '填空题'
#         verbose_name_plural = '填空题'

#     def __str__(self):
#         return '题'+str(self.id)

#     problem_type = models.CharField("试卷类型", max_length=20, choices=EXAM_TYPE_CHOICES, default='1')
#     question_text = models.TextField('题目', help_text="题目填空处使用 ______[6个英文下划线] 的形式表示", )
#     answer_text = models.TextField('对应答案', help_text="题目中每个______对应的答案单独一行", default='')

#     def problem_type_(self):
#         return EXAM_TYPE_CHOICES[int(self.problem_type)-1][1]
#     problem_type_.short_description = '试卷类型'

#     def ansower_html_(self):
#         answer_text = [x for x in self.answer_text.split('\n')]
#         return format_html("<ol>") + \
#                 format_html_join(
#                 '\n', '<li style="color:{};">{}</li>',
#                 (('black', x) for x in answer_text)
#                 ) \
#                 + format_html("</ol>")
#     ansower_html_.short_description = '答案'

#     def question_html_(self):
#         question_text = [x for x in self.question_text.split('\n')]
#         return format_html_join(
#                 '', '<p style="color:{};">{}</p>',
#                 (('black', x) for x in question_text)
#                 )
#     question_html_.short_description = '题目'

#     def clean(self):
#         question_text = self.question_text.replace(' ','')

#         count_flags = question_text.count('______')  ## find all '______'
#         if count_flags==0:
#             raise ValidationError({'question_text': _('______ 缺失')})

#         answer_text_list = self.answer_text.split('\n')
#         answer_text_list = [x.strip() for x in answer_text_list if len(x.strip())>0]
#         if len(answer_text_list) != count_flags:
#             raise ValidationError({'question_text': _('______和答案数目不一致')})
