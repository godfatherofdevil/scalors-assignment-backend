from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Board, Todo, Reminder
from .permissions import IsOwnerOrReadOnly
from .serializers import BoardDetailSerializer, BoardSerializer, TodoSerializer, UserSerializer, \
    ReminderSerializer
from .tasks import send_email


class BoardList(generics.ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BoardDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, ]


class TodoList(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]

    def get_queryset(self):
        queryset = Todo.objects.all()
        if self.request.method == "POST":
            return queryset
        done = self.request.query_params.get("done")
        board_id = self.kwargs.get(self.lookup_field)
        if done is not None:
            queryset = queryset.filter(board_id=board_id, done=done)
        else:
            queryset = queryset.filter(board_id=board_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(board_id=self.kwargs.get(self.lookup_field), owner=self.request.user)


class TodoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    lookup_field = "id"
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, ]


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ReminderList(generics.ListCreateAPIView):
    queryset = Reminder.objects.all()
    serializer_class = ReminderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        send_email.apply_async(
            (self.request.data.get("email"), self.request.data.get("text")),
            countdown=self.request.data.get("delay") * 60
        )


class ReminderDetail(generics.DestroyAPIView):
    queryset = Reminder.objects.all()
    serializer_class = ReminderSerializer
    permission_classes = [IsOwnerOrReadOnly, ]


@api_view(["POST", ])
def email_callback(request):
    email = request.data.get("email")
    text = request.data.get("text")
    success = f"email sent to {email}"
    content = {
        "email": email, "text": text, "message": success
    }

    return Response(content, status=200)
