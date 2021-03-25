from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('exam/<int:exam_id>', views.exam_detail, name='exam'),
]