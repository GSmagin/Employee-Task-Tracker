from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from task_tracker.models import Task, Employee
from users.models import User


class TaskTestCase(APITestCase):

    def setUp(self):
        # Создаем пользователя
        self.user = User.objects.create(email="testuser@example.com")

        # Создаем сотрудника
        self.employee = Employee.objects.create(
            full_name="Сергей Сергеевич Куропаткин",
            position="Инженер"
        )

        # Создаем задачу
        self.task = Task.objects.create(
            title="Test1",
            start_date="2024-09-10",
            end_date="2024-09-10",
            is_important=True,
            employee=self.employee,
        )

    def test_should_retrieve_task_successfully(self):
        url = reverse("task_tracker:task_retrieve", args=(self.task.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["title"], self.task.title)
        self.assertEqual(data["employee"], self.employee.id)

    def test_should_create_task_successfully(self):
        url = reverse("task_tracker:task_create")
        data = {
            "title": "Test2",
            "start_date": "2024-09-10",
            "end_date": "2024-09-10",
            "employee": self.employee.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)

        created_task = Task.objects.get(title="Test2")
        self.assertEqual(created_task.employee, self.employee)

    def test_should_update_task_successfully(self):
        url = reverse("task_tracker:task_update", args=(self.task.pk,))
        data = {
            "title": "Updated Task Title",
            "start_date": "2024-09-10",
            "end_date": "2024-09-20",
        }
        response = self.client.patch(url, data)
        updated_task = Task.objects.get(pk=self.task.pk)  # Получаем обновленную задачу
        data = response.json()
        print(data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["title"], updated_task.title)
        self.assertEqual(data["start_date"], updated_task.start_date.isoformat())  # Приводим к строке
        self.assertEqual(data["end_date"], updated_task.end_date.isoformat())  # Приводим к строке

    def test_should_delete_task_successfully(self):
        url = reverse("task_tracker:task_delete", args=(self.task.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

    def test_should_list_tasks_successfully(self):
        url = reverse("task_tracker:task_list")
        response = self.client.get(url)
        data = response.json()

        expected_result = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    "id": self.task.pk,
                    "term_days": 0,
                    "title": "Test1",
                    "start_date": "2024-09-10",
                    "end_date": "2024-09-10",
                    "status": "Не приступал к выполнению",
                    "comments": None,
                    "owner": None,
                    "is_active": True,
                    "is_important": True,
                    "parent_task": None,
                    "employee": self.task.employee.id,
                }
            ]
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, expected_result)

    def test_should_not_create_task_with_invalid_dates(self):
        url = reverse("task_tracker:task_create")
        data = {
            "title": "InvalidTask",
            "start_date": "invalid-date",
            "end_date": "2024-09-10",
            "employee": self.employee.id,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("start_date", response.data)

    def test_should_not_update_task_with_invalid_dates(self):
        url = reverse("task_tracker:task_update", args=(self.task.pk,))
        data = {"start_date": "invalid-date"}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("start_date", response.data)

    def test_task_list_pagination(self):
        url = reverse("task_tracker:task_list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertLessEqual(len(response.data['results']), 10)
        self.assertIn('count', response.data)

    def test_should_return_404_for_non_existent_task(self):
        non_existent_task_id = 999
        url = reverse("task_tracker:task_retrieve", args=(non_existent_task_id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_should_not_create_task_with_start_date_after_end_date(self):
        url = reverse("task_tracker:task_create")
        data = {
            "title": "TestInvalidDates",
            "start_date": "2024-09-11",  # Дата начала позже даты окончания
            "end_date": "2024-09-10",
            "employee": self.employee.id,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
        self.assertIn("Дата начала не может быть позже даты окончания.", response.data['non_field_errors'])

    def test_should_not_allow_duplicate_task(self):
        url = reverse("task_tracker:task_create")
        data = {
            "title": "Test1",
            "start_date": "2024-09-10",
            "end_date": "2024-09-10",
            "employee": self.employee.id,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
        self.assertIn('Поля title должны производить массив с уникальными значениями.', response.data['non_field_errors'])



