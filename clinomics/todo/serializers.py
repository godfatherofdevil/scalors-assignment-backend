from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Board, Todo, Reminder


class BoardSerializer(serializers.ModelSerializer):
    todo_count = serializers.SerializerMethodField(read_only=True)
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Board
        fields = ["id", "name", "owner", "todo_count"]
        depth = 1

    def get_todo_count(self, board):
        return board.todos.count()


class TodoSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Todo
        fields = ["id", "title", "done", "created", "updated", "owner"]


class BoardDetailSerializer(serializers.ModelSerializer):
    todos = TodoSerializer(many=True, required=False)
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Board
        fields = ["id", "name", "owner", "todos"]


class UserSerializer(serializers.ModelSerializer):
    board_owner = serializers.PrimaryKeyRelatedField(many=True, queryset=Board.objects.all())
    todo_owner = serializers.PrimaryKeyRelatedField(many=True, queryset=Todo.objects.all())

    class Meta:
        model = User
        fields = ["id", "username", "board_owner", "todo_owner"]


class ReminderSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Reminder
        fields = ["id", "email", "text", "delay", "owner"]

