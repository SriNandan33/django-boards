from django.urls import path
from . import views


urlpatterns = [
	path('', views.home, name='home'),
	path('boards/<int:pk>/', views.board_topics, name='board_topics'),
	path('boards/<int:pk>/new/', views.new_topic, name='new_topic'),

]