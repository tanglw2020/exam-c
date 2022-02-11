
# -*- coding: utf-8 -*-
from django.db import models
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html, format_html_join
from django.utils import timezone
import re
import os
import shutil
import zipfile
from pathlib import Path
# Create your models here.

BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT  = BASE_DIR / 'media'

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


class Student(models.Model):
    class Meta:
        verbose_name = '考试-考生'
        verbose_name_plural = '考试-考生'
    class_name = models.CharField('班级',max_length=100, default='')
    student_name = models.CharField('姓名', max_length=20, default='')
    student_id = models.CharField('学号', max_length=20,  unique = True, default='')
    pass_word = models.CharField('密码', max_length=20, default='', blank=True)

    def __str__(self):
        return self.class_name+" "+self.student_name +" "+self.student_id


class Exam(models.Model):
    class Meta:
        verbose_name = '考试-考场'
        verbose_name_plural = '考试-考场'

    pub_date = models.DateTimeField('创建时间', 'date published', null=True, default=timezone.now)
    problem_type = models.CharField("试卷类型", max_length=20, choices=EXAM_TYPE_CHOICES, default='1')
    creator = models.CharField('创建人', max_length=200, default='..老师')
    info_text = models.CharField('考试信息', max_length=200, default='C语言期末考试')
    period = models.CharField("考试时长", max_length=5, choices=PERIOD_CHOICES, default='1')

    passwd_second_login = models.CharField('二次登录密码', max_length=200, default='3333')
    opened = models.BooleanField("考场开放？", default=True)

    choice_question_num = models.IntegerField(verbose_name="选择题个数", default=20)
    choice_question_score = models.IntegerField(verbose_name="选择题分值", default=2)
    coding_question_num = models.IntegerField(verbose_name="编程题个数", default=4)
    coding_question_score = models.IntegerField(verbose_name="编程题分值", default=15)

    def __str__(self):
        return '考场-'+str(self.id)

    def id_(self):
        return '考场-'+str(self.id)
    id_.short_description = '考试编号'

    def clean(self):
        score = self.choice_question_num*self.choice_question_score + \
            self.coding_question_num * self.coding_question_score
        if score != 100:
            raise ValidationError(_('总分值不等于100'))

    def all_question_stat_(self):
        return '选择题'+str(self.choice_question_score)+'分X'+str(self.choice_question_num)+ \
            ' + '+'编程题'+str(self.coding_question_score)+'分X'+str(self.coding_question_num)
    all_question_stat_.short_description = '考题统计'

    def exam_type_(self):
        return str(EXAM_TYPE_CHOICES[int(self.problem_type)-1][1])
    exam_type_.short_description = '考试类型'

    def period_(self):
        return str(PERIOD_CHOICES[int(self.period)-1][1])
    period_.short_description = '考试时长'

    def out_link_(self):
        return format_html('<a href="/c/examroom/{}" target="_blank">点击查看</a>'.format(self.id))
    out_link_.short_description = '考场详情'




class ExamPaper(models.Model):
    class Meta:
        verbose_name = '考试-试卷'
        verbose_name_plural = '考试-试卷'

    def __str__(self):
        return '试卷-'+str(self.unique_key)

    problem_type = models.CharField("试卷类型", max_length=20, choices=EXAM_TYPE_CHOICES, default='1')
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE, null=True,
        verbose_name='所属考生'
    ) 
    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE, null=True,
        verbose_name='所属考场'
    ) 
    unique_key = models.CharField('unique-key', max_length=20, primary_key=True, default='xxx')  #  student_id_local+exam_id_local

    start_time = models.DateTimeField('开考时间', null=True, blank=True, default=timezone.now)
    end_time = models.DateTimeField('交卷时间', null=True, blank=True, default=timezone.now)
    add_time = models.IntegerField("附加延时[分]", default=0)
    enabled = models.BooleanField("是否可以作答?", default=True)

    student_id_local = models.CharField('学号', max_length=20, default='')
    exam_id_local = models.CharField('考场号', max_length=20, default='')

    choice_questions = models.TextField("选择题列表", max_length=1000,  blank=True, default='')
    choice_question_answers = models.TextField("选择题答案列表", max_length=1000, blank=True,  default='')
    choice_question_results = models.TextField("选择题评分", max_length=1000, blank=True,  default='')

    coding_questions = models.TextField("编程题列表", max_length=1000, blank=True, default='')
    coding_question_answers = models.TextField("编程题答案列表", max_length=1000, blank=True, default='')
    coding_question_results = models.TextField("编程题评分", max_length=1000, blank=True, default='')


    def is_empty_(self):
        if self.exam.choice_question_num:
            if len(self.choice_questions)<1: return True

        if self.exam.coding_question_num:
            if len(self.coding_questions)<1: return True
        return False


    def disable_(self):
        self.enabled = False
        self.end_time = datetime.datetime.now()
        self.save()

    def add_time_enable_(self, t=3):
        self.enabled = True
        self.add_time = self.add_time + t
        self.save()

    def start_time_(self):
        return (self.start_time.strftime("%Y-%m-%d %H:%M:%S"))
    start_time_.short_description = '开考时间'

    def end_time_(self):
        return (self.end_time.strftime("%Y-%m-%d %H:%M:%S"))
    end_time_.short_description = '结束时间'

    def coding_question_answers_(self):
        return self.coding_question_answers.split(',')
    coding_question_answers_.short_description = '编程题答案'

    def choice_question_answers_(self):
        return self.choice_question_answers.split(',')
    choice_question_answers_.short_description = '选择题答案'

    def choice_questions_all_(self):
        choice_question_ids = [int(x) for x in self.choice_questions.split(',') if len(x)]
        choice_questions_all = []
        for i in choice_question_ids:
            choice_questions_all.append(ChoiceQuestion.objects.get(pk=i))
        return choice_questions_all
    choice_questions_all_.short_description = '全部选择题'

    def coding_questions_all_(self):
        coding_question_ids = [int(x) for x in self.coding_questions.split(',') if len(x)]
        coding_questions_all = []
        for i in coding_question_ids:
            coding_questions_all.append(CodingQuestion.objects.get(pk=i))
        return coding_questions_all
    coding_questions_all_.short_description = '全部编程题'

    ## question_id start from 1 to n
    def choice_questions_pk_(self, question_id):
        question_database_id = int(self.choice_questions.split(',')[question_id-1])
        return ChoiceQuestion.objects.get(pk=question_database_id)
    choice_questions_pk_.short_description = 'pk选择题'

    def coding_questions_pk_(self, question_id):
        question_database_id = int(self.coding_questions.split(',')[question_id-1])
        return CodingQuestion.objects.get(pk=question_database_id)
    coding_questions_pk_.short_description = 'pk编程题'

    def coding_output_path_(self, question_id):
        output_save_path = os.path.join(MEDIA_ROOT, 'upload_output','coding_output_{}_{}.txt'.format(self.id, question_id))
        return output_save_path
    coding_output_path_.short_description = '上传结果保存目录'

    def update_choice_question_answer_result_(self, question_id, choice_id):
        old_answers = self.choice_question_answers.split(',')
        old_answers[question_id-1] = str(choice_id)
        self.choice_question_answers = ','.join(old_answers)

        choice_question = self.choice_questions_pk_(question_id)
        if choice_question.answer == str(choice_id):
            score = '1'
        else:
            score = '0'
        old_answers = self.choice_question_results.split(',')
        old_answers[question_id-1] = score
        self.choice_question_results = ','.join(old_answers)
        self.save()

    def choice_question_result_stat(self):
        answers = [x for x in self.choice_question_answers.split(',') if x!='+']
        results = [x for x in self.choice_question_results.split(',') if x=='1']
        return self.exam.choice_question_num, len(answers), len(results)

        # print(self.choice_question_results)

    def update_coding_question_answer_result_(self, coding_question_id, output_save_path):
        old_answers = self.coding_question_answers.split(',')
        old_answers[coding_question_id-1] = str(output_save_path)
        self.coding_question_answers = ','.join(old_answers)

        ## 
        coding_question = self.coding_questions_pk_(coding_question_id)
        answer_path = coding_question.upload_answer_file.path
        with open(answer_path, encoding='utf-8') as f:
            answers = [x.strip() for x in f.readlines()]
        with open(output_save_path, encoding='utf-8') as f:
            outputs = [x.strip() for x in f.readlines()]
        # print(outputs)
        min_len = min(len(answers), len(outputs))
        correct_cnt = 0
        for i in range(min_len):
            if answers[i] == outputs[i]: correct_cnt = correct_cnt + 1
        score = str(correct_cnt*1.0/len(answers))
        old_answers = self.coding_question_results.split(',')
        old_answers[coding_question_id-1] = score
        print(old_answers)
        self.coding_question_results = ','.join(old_answers)
        self.save()

    def coding_question_result_stat(self):
        answers = [x for x in self.coding_question_answers.split(',') if x!='+']
        results = [float(x) for x in self.coding_question_results.split(',')]
        sum = 0
        for i in range(len(results)):
            sum = sum + results[i]
        return self.exam.coding_question_num, len(answers), sum

    def coding_question_result_detail(self):
        answers = [x for x in self.coding_question_answers.split(',') if x!='+']
        results = [float(x) for x in self.coding_question_results.split(',')]
        return results

    def total_score(self):
        _,_, choice_question_correct_num = self.choice_question_result_stat()
        _,_, coding_question_correct_num = self.coding_question_result_stat()
        return choice_question_correct_num*self.exam.choice_question_score + coding_question_correct_num*self.exam.coding_question_score


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

def validate_csvfile(value):
    extension = value.name.split('.')[-1]
    if extension not in ['csv',]:
        raise ValidationError(
            _(value.name+'不是csv文件'),
            params={'value': value.name},
        )



class ChoiceQuestion(models.Model):
    class Meta:
        verbose_name = '题目-选择题'
        verbose_name_plural = '题目-选择题'

    def __str__(self):
        return '选择题-'+str(self.id)

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


class CodingQuestion(models.Model):
    class Meta:
        verbose_name = '题目-编程题'
        verbose_name_plural = '题目-编程题'

    def __str__(self):
        return '编程题-'+str(self.id)

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
        try:
            with open(self.upload_description_file.path,'r', encoding='utf-8') as f:
                lines = f.readlines()
                return format_html_join(
                        '', '<p style="color:{};">{}</p>',
                        (('black', x) for x in lines)
                        )
        except:
            return ''
    question_html_.short_description = '题目'

    def code_html_(self):
        try:
            with open(self.upload_c_file.path,'r', encoding='utf-8') as f:
                lines = f.readlines()
                return format_html_join(
                        '', '<p style="color:{};">{}</p>',
                        (('black', x) for x in lines)
                        )
        except:
            return ''
    code_html_.short_description = '代码'

    def zip_path_(self):
        try:
            c_path, input_path = self.upload_c_file.path, self.upload_input_file.path
            paths = os.path.split(input_path)
            return os.path.sep.join([paths[0], 'coding-'+str(self.id)+'.zip'])
        except:
            return ''
    zip_path_.short_description = '压缩文件'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  
        zip_path = self.zip_path_()
        if zip_path:
            if os.path.exists(zip_path): os.remove(zip_path)
            c_path, input_path = self.upload_c_file.path, self.upload_input_file.path
            print(zip_path)
            zf = zipfile.ZipFile(zip_path, 'w')
            zf.write(c_path,'{}/main.c'.format('coding'))
            zf.write(input_path,'{}/input.txt'.format('coding'))
            zf.close()



class StudentInfoImporter(models.Model):
    class Meta:
        verbose_name = '考试-批量导入考生'
        verbose_name_plural = '考试-批量导入考生'

    def __str__(self):
        return '导入考生-'+str(self.id)

    upload_description_file = models.FileField(upload_to='upload_student_list/', null=True, blank=True, 
    validators=[validate_txtfile], verbose_name='上传考生信息文件[.txt]')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the "real" save() method.
        print(self.upload_description_file, 'saved')
        with open(self.upload_description_file.path,'r', encoding='utf-8') as f:
            lines = [x.strip().replace('\t',' ').split(' ') for x in f.readlines()[:] if len(x)>0]
            class_name = ''
            for x in lines:
                if len(x)==1: 
                    class_name = x[0]
                    continue
                if len(x)>5 and (x[0] !='学号'):
                    # print(class_name, x[0], x[1])
                    Student.objects.get_or_create(class_name=class_name, student_id=x[0], student_name=x[1])
                    # p = Student(class_name=class_name, student_id=x[0], student_name=x[1])
                    # p.save()




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