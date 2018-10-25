from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Board, Topic, Post
from .forms import NewTopicForm, PostForm

def home(request):
	boards = Board.objects.all()
	board_names = [board.name for board in boards]

	return render(request, 'boards/home.html', {'boards': boards})


def board_topics(request, pk):
	board = get_object_or_404(Board, pk=pk)
	return render(request, 'boards/topics.html', {'board': board})


@login_required
def new_topic(request, pk):
	board = get_object_or_404(Board, pk=pk)

	if request.method == 'POST':
		form = NewTopicForm(request.POST)
		if form.is_valid():
			topic = form.save(commit=False)
			topic.board = board
			topic.starter = request.user
			topic.save()
			post = Post.objects.create(
				message = form.cleaned_data.get('message'),
				topic = topic,
				created_by=request.user
			)
			return redirect('topic_posts', pk=pk, topic_pk=topic.pk)
	else:
		form = NewTopicForm()

	context = {
		'form':form,
		'board': board
	}
	return render(request, 'boards/new_topic.html', context)


def topic_posts(request, pk, topic_pk):
	topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
	return render(request, 'boards/topic_posts.html', {'topic': topic})



@login_required
def reply_topic(request, pk, topic_pk):
	topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
	if request.method == 'POST':
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.topic = topic
			post.created_by = request.user
			post.save()
			return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
	else:
		form = PostForm()

	return render(request, 'boards/reply_topic.html', {'topic': topic, 'form': form})