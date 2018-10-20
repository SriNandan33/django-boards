from django.shortcuts import render, get_object_or_404
from .models import Board

def home(request):
	boards = Board.objects.all()
	board_names = [board.name for board in boards]

	return render(request, 'boards/home.html', {'boards': boards})


def board_topics(request, pk):
	board = get_object_or_404(Board, pk=pk)
	return render(request, 'boards/topics.html', {'board': board})