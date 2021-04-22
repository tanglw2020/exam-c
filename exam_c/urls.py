from django.urls import path

from . import views

app_name = 'c'
urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('exampage/<int:exampage_id>', views.exampage, name='exampage'),
    path('exampage/<int:exampage_id>/choicequestion/<int:choice_question_id>', views.exampage_choice_question, name='exampage-choicequestion'),
    path('exampage/<int:exampage_id>/codingquestion/<int:coding_question_id>', views.exampage_coding_question, name='exampage-codingquestion'),
    path('examroom/<int:exam_id>', views.exam_room, name='examroom'),
    path('api/choiceanswer', views.api_choiceanswer,name='api-choiceanswer'),
    path('api/getservertime/<int:exampage_id>', views.api_get_server_time,name='api-getservertime'),
    path('api/download/scorelist<int:exam_id>.txt', views.api_download_scorelist, name='api-download-scorelist'),
]