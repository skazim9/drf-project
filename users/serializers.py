from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    product_type = serializers.ChoiceField(
        choices=[("course", "Course"), ("lesson", "Lesson")]
    )
    product_id = serializers.IntegerField()

    class Meta:
        model = Payment
        fields = ["product_type", "product_id", "amount", "session_id", "payment_link"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user
