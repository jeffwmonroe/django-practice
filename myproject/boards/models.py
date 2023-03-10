from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return 'board: (' + str(self.pk) + ') ' + str(self.name)


def print_all_boards():
    print('print_all_boards')
    board_list = Board.objects.all()
    for board in board_list:
        print(f'    board = {board}')
        print(f'    board.pk = {board.pk}')


class Topic(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='topics')
    starter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topics')


class Post(models.Model):
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    # TODO Look into changing the related_name to be 'updated posts'
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='+')
