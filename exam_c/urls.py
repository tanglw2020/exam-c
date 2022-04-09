from django.urls import path

from . import views

app_name = 'c'
urlpatterns = [
    path('', views.login, name='login'),
    path('loginsecond/<exampage_id>', views.login_second, name='login-second'),
    path('exampage/<exampage_id>', views.exampage, name='exampage'),
    path('exampage/<exampage_id>/choicequestion/<int:choice_question_id>', views.exampage_choice_question, name='exampage-choicequestion'),
    path('exampage/<exampage_id>/codingquestion/<int:coding_question_id>', views.exampage_coding_question, name='exampage-codingquestion'),
    path('examroom/<int:exam_id>', views.exam_room, name='examroom'),
    path('api/sendchoiceanswer/<exampage_id>/<int:choice_question_id>/<int:choice_id>', views.api_handle_choice_answer,name='api-choiceanswer'),
    path('api/getchoicetext/<exampage_id>/<int:choice_question_id>', views.api_get_choice_text,name='api-choicetext'),
    path('api/getservertime/<exampage_id>', views.api_get_server_time,name='api-getservertime'),
    path('api/download/scorelist<int:exam_id>.txt', views.api_download_scorelist, name='api-download-scorelist'),
    path('api/download/codingzip/<exampage_id>/<int:coding_question_id>', views.api_download_coding_zipfile, name='api-download-coding-zipfile'),
    path('api/submitall/<exampage_id>', views.api_submit_all, name='api-submit-all'),
    path('api/addtime/<exampage_id>', views.add_time_enable, name='api-addtime'),
]