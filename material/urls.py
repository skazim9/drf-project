from django.urls import path, include
from rest_framework.routers import DefaultRouter

from material.apps import MaterialConfig
from material.views import (CourseViewSet, LessonCreteAPIView,
                           LessonUpdateAPIView, LessonListAPIView,
                           LessonDestroyAPIView, LessonRetrieveAPIView)
app_name = MaterialConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
    path('', include(router.urls)),
    path('lesson/crete/', LessonCreteAPIView.as_view(), name='lesson_crete'),
    path('lesson/list/', LessonListAPIView.as_view(), name='lesson_list'),
    path('lesson/retriv/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_retriv'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lesson/destroy/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson_destroy'),
]