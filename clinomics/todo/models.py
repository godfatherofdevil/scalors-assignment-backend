from django.db import models


class Board(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey("auth.User", related_name="board_owner", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}:{self.name}"

    def __unicode__(self):
        return self.name


class Todo(models.Model):
    title = models.CharField(max_length=100)
    done = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="todos")
    owner = models.ForeignKey("auth.User", related_name="todo_owner", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.board}:{self.title}"

    def __unicode__(self):
        return f"{self.title}: {self.created}"

    class Meta:
        ordering = ["created", ]
