from rest_framework import serializers
from .models import Course, Lesson, Subscription
from .validators import validate_video_link


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(validators=[validate_video_link])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        user = self.context["request"].user
        return (
            Subscription.objects.filter(user=user, course=obj).exists()
            if user.is_authenticated
            else False
        )

    @staticmethod
    def get_lesson_count(obj):
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = "__all__"
