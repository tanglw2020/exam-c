from django.contrib import admin
from .models import *
# Register your models here.


class ChoiceQuestionAdmin(admin.ModelAdmin):
        list_display = ('__str__', 'question_html_', 'answer_list_', 'problem_type')
        list_display_links = ('__str__',)


class CodingQuestionAdmin(admin.ModelAdmin):
        list_display = ('__str__', 'question_text', 'question_html_', 'code_html_','problem_type')
        list_display_links = ('question_text',)


class StudentAdmin(admin.ModelAdmin):
        list_display = ('class_name', 'student_name', 'student_id', )


class ExamAdmin(admin.ModelAdmin):
        list_display = ('id_', 'problem_type', 'info_text', 'out_link_')


class ExamPaperAdmin(admin.ModelAdmin):
        list_display = ('__str__', 'problem_type', 'student_id', 'exam_id', 'start_time_')


###########
# admin.site.register([ExamPaper])
admin.site.register(Exam, ExamAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(ExamPaper, ExamPaperAdmin)
admin.site.register(ChoiceQuestion, ChoiceQuestionAdmin)
admin.site.register(CodingQuestion, CodingQuestionAdmin)

