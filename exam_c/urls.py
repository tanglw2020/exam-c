from django.urls import path

from . import views

app_name = 'c'
urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('exampage/<int:exampage_id>', views.exampage, name='exampage'),
    path('examroom/<int:exam_id>', views.exam_room, name='examroom'),
    path(r'handle/choiceanswer', views.handle_choice_ans_change,name='handle-choiceanswer'),
]