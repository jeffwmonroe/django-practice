from django.shortcuts import render, get_object_or_404, redirect
from .models import Board, Topic, Post
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound
from django.contrib.auth.models import User
from .forms import NewTopicForm

# Create your views here.

def home(request):
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards})


def board_by_pk(request, pk):
    try:
        board = Board.objects.get(pk=pk)
        return render(request, 'topics.html', {'board': board})
    except ObjectDoesNotExist:
        # ToDo need to handle this error better
        return HttpResponseNotFound("Unknown board")


def board(request, board_name):
    try:
        board = Board.objects.get(name=board_name)
        return render(request, 'topics.html', {'board': board})
    except ObjectDoesNotExist:
        return HttpResponseNotFound("Unknown Board")


def new_topic(request, board_name):
    board = get_object_or_404(Board, name=board_name)
    user = User.objects.first()  # TODO: get the currently logged in user

    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )

            return redirect('board', board_name=board.name)  # TODO: redirect to the created topic page
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'form': form,
                                              'board': board})
