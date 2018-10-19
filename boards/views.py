from django.shortcuts import render
from .models import Board

def home(request):
	boards = Board.objects.all()
	board_names = [board.name for board in boards]

	return render(request, 'boards/home.html', {'boards': boards})