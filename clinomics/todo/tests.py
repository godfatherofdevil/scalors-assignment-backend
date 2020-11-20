from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Board, Todo


class BoardTest(APITestCase):

    def setUp(self) -> None:
        """
        setup test environment
        """
        self.test_user = User.objects.create_user(username="tempUser", password="temp@123")

    def test_create_board(self):
        self.client.force_login(self.test_user)
        url = reverse("boardList")
        data = {"name": "foo"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Board.objects.count(), 1)
        self.assertEqual(Board.objects.get().name, "foo")

        # list
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0].get("name"), "foo")
        self.assertEqual(response.data[0].get("todo_count"), 0)

    def test_list_one(self):
        self.client.force_login(self.test_user)
        url = reverse("boardList")
        items = [{"name": "foo"}, {"name": "bar"}]
        # create multiple
        for item in items:
            self.client.post(url, item, format="json")

        # get one
        response = self.client.get(f"{url}/1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("name"), "foo")

        response = self.client.get(f"{url}/2")
        self.assertEqual(response.data.get("name"), "bar")

    def test_board_change_title(self):
        self.client.force_login(self.test_user)
        url = reverse("boardList")
        data = {"name": "foo"}
        self.client.post(url, data, format="json")
        self.assertEqual(Board.objects.get().name, "foo")

        response = self.client.patch(f"{url}/1", data={"name": "bar"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Board.objects.get().name, "bar")

    def test_board_remove_one(self):
        self.client.force_login(self.test_user)
        url = reverse("boardList")
        data = {"name": "foo"}
        self.client.post(url, data, format="json")
        self.assertEqual(Board.objects.get().name, "foo")

        response = self.client.delete(f"{url}/1")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Board.objects.count(), 0)


class TodoTest(APITestCase):
    def setUp(self) -> None:
        """
        setup test environment
        """
        self.test_user = User.objects.create_user(username="tempUser", password="temp@123")
        self.client.force_login(self.test_user)
        url = reverse("boardList")
        items = [{"name": "foo"}, {"name": "bar"}]
        # create multiple
        for item in items:
            self.client.post(url, item, format="json")

    def test_todo_add(self):
        url = reverse("boardList")
        todo = {"title": "i am foo"}
        response = self.client.post(f"{url}/1/todo", data=todo, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Todo.objects.count(), 1)
        self.assertEqual(Todo.objects.get().title, "i am foo")

        # list
        another_todo = {"title": "i am bar"}
        self.client.post(f"{url}/1/todo", data=another_todo, format="json")
        self.assertEqual(Todo.objects.count(), 2)

        response = self.client.get(f"{url}/1/todo")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_todo_uncompleted(self):
        url = reverse("boardList")
        todos = [{"title": "i am foo"}, {"title": "i am bar"}, ]
        for todo in todos:
            self.client.post(f"{url}/2/todo", data=todo, format="json")

        # new has status not done by default
        response = self.client.get(f"{url}/2/todo?done={False}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        for d in response.data:
            self.assertEqual(d.get("done"), False)

        # change one's status to done
        self.client.patch(f"{url}/2/todo/1", data={"done": True}, format="json")
        response = self.client.get(f"{url}/2/todo?done={False}")
        self.assertEqual(len(response.data), 1)
        for d in response.data:
            self.assertEqual(d.get("done"), False)

    def test_todo_update(self):
        url = reverse("boardList")
        todo = {"title": "i am batman"}
        self.client.post(f"{url}/1/todo", data=todo, format="json")
        self.assertEqual(Todo.objects.get().title, "i am batman")
        self.assertEqual(Todo.objects.get().done, False)

        # change the title
        response = self.client.patch(f"{url}/1/todo/1",
                                     data={"title": "i am batman and i live in gotham city"},
                                     format="json"
                                     )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Todo.objects.get().title, "i am batman and i live in gotham city")
        self.assertEqual(Todo.objects.get().done, False)

        # change the status
        response = self.client.patch(f"{url}/1/todo/1", data={"done": True}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Todo.objects.get().title, "i am batman and i live in gotham city")
        self.assertEqual(Todo.objects.get().done, True)

    def test_todo_delete(self):
        url = reverse("boardList")
        todo = {"title": "i am batman"}
        self.client.post(f"{url}/1/todo", data=todo, format="json")
        self.assertEqual(Todo.objects.count(), 1)
        # delete
        response = self.client.delete(f"{url}/1/todo/1")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Todo.objects.count(), 0)
