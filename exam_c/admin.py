from django.contrib import admin
from .models import *
# Register your models here.

class ChoiceQuestionAdmin(admin.ModelAdmin):
        list_display = ('__str__', 'question_html_', 'answer_list_', 'problem_type_')
        list_display_links = ('__str__',)

# class CompletionQuestionAdmin(admin.ModelAdmin):
#         list_display = ('__str__', 'question_html_', 'ansower_html_', 'problem_type_')
#         list_display_links = ('__str__',)

class CodingQuestionAdmin(admin.ModelAdmin):
        list_display = ('__str__', 'question_text', 'question_html_', 'code_html_','problem_type_')
        list_display_links = ('question_text',)

class StudentAdmin(admin.ModelAdmin):
        list_display = ('class_name', 'student_name', 'student_id', )

admin.site.register([Exam, ExamPaper])
admin.site.register(Student, StudentAdmin)
admin.site.register(ChoiceQuestion, ChoiceQuestionAdmin)
admin.site.register(CodingQuestion, CodingQuestionAdmin)

