from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Course, Subscription, Lesson
from users.models import User


class CourseAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            username='testusername',
            password='password',
            is_staff=True
        )


        self.course_data = {
            'title': 'Test Course',
            'description': 'Test Description',
            'owner': self.user
        }
        self.course = Course.objects.create(**self.course_data)

        self.course_url = reverse('materials:course-detail', args=[self.course.id])
        self.subscription_url = reverse('materials:subscription')


    def test_course_creation(self):
        """ Тестирование создания курса """
        self.assertEqual(Course.objects.count(), 1)
        self.assertEqual(self.course.title, 'Test Course')


    def test_get_course_details(self):
        """ Тестирование получения деталей курса """
        self.client.login(email='testuser@example.com', password='password')
        response = self.client.get(self.course_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Course')
        self.assertEqual(response.data['owner'], self.user.id)


    def test_create_subscription(self):
        """ Тестирование создания подписки на курс """
        self.client.login(email='testuser@example.com', password='password')
        response = self.client.post(self.subscription_url, {
            'course_id': self.course.id,
            'username': 'testusername'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())
        self.assertEqual(response.data['message'], "Подписка добавлена")
class LessonAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            username='testusername',
            password='password',
            is_staff=True
        )

        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description',
            owner=self.user
        )

        self.lesson_data = {
            'title': 'Test Lesson',
            'description': 'Test Description',
            'course': self.course,
            'owner': self.user
        }
        self.lesson = Lesson.objects.create(**self.lesson_data)

        self.lesson_url = reverse('materials:lesson-detail', args=[self.lesson.id])
    def test_lesson_creation(self):
        """ Тестирование создания урока """
        self.assertEqual(Lesson.objects.count(), 1)
        self.assertEqual(self.lesson.title, 'Test Lesson')


    def test_get_lesson_details(self):
        """ Тестирование получения деталей урока """
        self.client.login(email='testuser@example.com', password='password')
        response = self.client.get(self.lesson_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Lesson')
        self.assertEqual(response.data['owner'], self.user.id)
