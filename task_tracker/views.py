from django.db.models import Q, Count
from rest_framework.filters import SearchFilter
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)

from task_tracker.models import Employee, Task
from task_tracker.serializers import (
    EmployeeSerializer,
    TaskSerializer,
    ImportantTaskSerializer,
    EmployeeActiveTasksSerializer,
)
from task_tracker.custom_pagination import CustomPagination


class TaskCreateAPIView(CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        # Назначаем владельца задачи
        serializer.save(owner=self.request.user)


class TaskListAPIView(ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    pagination_class = CustomPagination


class ImportantTaskListAPIView(ListAPIView):
    serializer_class = ImportantTaskSerializer

    def get_queryset(self):
        # Фильтрация по статусу, важности и статусу родительской задачи
        return Task.objects.filter(
            status=Task.STATUS_NOT_STARTED,
            is_important=True,
            parent_task__status=Task.STATUS_IN_PROGRESS,
        )


class TaskRetrieveAPIView(RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskUpdateAPIView(UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskDestroyAPIView(DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class EmployeeCreateAPIView(CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeListAPIView(ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeActiveTasksListAPIView(ListAPIView):
    serializer_class = EmployeeActiveTasksSerializer
    filter_backends = [SearchFilter]
    search_fields = ["full_name"]

    def get_queryset(self):
        # Выбираем сотрудников и аннотируем количество задач
        return Employee.objects.annotate(tasks_count=Count("task")).order_by("-tasks_count")


class EmployeeRetrieveAPIView(RetrieveAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeActiveTasksSerializer


class EmployeeUpdateAPIView(UpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeDestroyAPIView(DestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
