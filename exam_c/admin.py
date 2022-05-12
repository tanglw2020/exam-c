from django.contrib import admin
from .models import *
# Register your models here.


class ChoiceQuestionAdmin(admin.ModelAdmin):
        list_display = ('__str__', 'question_html_', 'answer_list_', 'problem_type')
        list_display_links = ('__str__',)
        search_fields = ('question_text',)

class CompleteQuestionAdmin(admin.ModelAdmin):
        list_display = ('__str__', 'question_html_', 'answers_html_', 'problem_type')


class CodingQuestionAdmin(admin.ModelAdmin):
        list_display = ('__str__', 'question_html_', 'code_html_','problem_type',)
        # list_display = ('__str__', 'question_html_', 'problem_type',)


class StudentAdmin(admin.ModelAdmin):
        list_display = ('class_name', 'student_name', 'student_id', )
        search_fields = ('student_name', 'student_id',)


class ExamAdmin(admin.ModelAdmin):
        list_display = ('id_', 'opened','problem_type', 'info_text','all_question_stat_','out_link_',)
        list_editable = ( 'opened',)

class ExamPaperAdmin(admin.ModelAdmin):
        list_display = ('__str__', 'problem_type', 'student', 'exam', 'start_time_')


###########
admin.site.register([StudentInfoImporter, ChoiceQuestionImporter])
admin.site.register(Exam, ExamAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(ExamPaper, ExamPaperAdmin)
admin.site.register(ChoiceQuestion, ChoiceQuestionAdmin)
admin.site.register(CompleteQuestion, CompleteQuestionAdmin)
admin.site.register(CodingQuestion, CodingQuestionAdmin)

admin.site.site_title = "C语言期末考试后台管理系统"
admin.site.site_header = "C语言期末考试后台管理系统"