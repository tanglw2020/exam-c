from django.contrib import admin
from .models import *
# Register your models here.


class ChoiceQuestionAdmin(admin.ModelAdmin):
        list_display = ('__str__', 'question_html_', 'answer_list_', 'problem_type')
        list_display_links = ('__str__',)


class CodingQuestionAdmin(admin.ModelAdmin):
        list_display = ('__str__', 'question_text', 'question_html_', 'code_html_','problem_type', 'zip_path_')
        list_display_links = ('question_text',)


class StudentAdmin(admin.ModelAdmin):
        list_display = ('class_name', 'student_name', 'student_id', )


class ExamAdmin(admin.ModelAdmin):
        list_display = ('id_', 'problem_type', 'info_text','choice_question_num','choice_question_score', 'coding_question_num','coding_question_score','out_link_')


class ExamPaperAdmin(admin.ModelAdmin):
        list_display = ('__str__', 'problem_type', 'student', 'exam', 'start_time_')


###########
admin.site.register([StudentInfoImporter])
admin.site.register(Exam, ExamAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(ExamPaper, ExamPaperAdmin)
admin.site.register(ChoiceQuestion, ChoiceQuestionAdmin)
admin.site.register(CodingQuestion, CodingQuestionAdmin)

