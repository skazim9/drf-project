from rest_framework import viewsets, permissions
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from .permissions import IsModerator


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ["create", "destroy"]:
            return [permissions.IsAdminUser()]
        elif self.action in ["list", "retrieve", "update"]:
            return [IsModerator() | permissions.IsAuthenticated()]
        return super().get_permissions()

    def get_queryset(self):

        if (
            self.request.user.groups.filter(name="moderators").exists()
            or self.request.user.is_staff
        ):
            return Course.objects.all()
        return Course.objects.filter(owner=self.request.user)


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.action in ["create", "destroy"]:
            return [permissions.IsAdminUser()]
        elif self.action in ["list", "retrieve", "update"]:
            return [IsModerator() | permissions.IsAuthenticated()]
        return super().get_permissions()

    def get_queryset(self):
        if (
            self.request.user.groups.filter(name="moderators").exists()
            or self.request.user.is_staff
        ):
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)