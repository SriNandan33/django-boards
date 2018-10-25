from django.urls import path
from . import views


urlpatterns = [
	path('', views.home, name='home'),
	path('boards/<int:pk>/', views.board_topics, name='board_topics'),
	path('boards/<int:pk>/new/', views.new_topic, name='new_topic'),
	path('boards/<int:pk>/topics/<int:topic_pk>/', views.topic_posts, name='topic_posts'),
	path('boards/<int:pk>/topics/<int:topic_pk>/reply/', views.reply_topic, name='reply_topic')

]