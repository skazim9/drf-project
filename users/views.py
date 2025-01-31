from rest_framework import generics, filters, viewsets, permissions, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from material.models import Course, Lesson
from .models import Payment
from .serializers import PaymentSerializer
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from .services import (
    create_product_course,
    create_price,
    create_checkout_session,
    create_product_lesson,
)

User = get_user_model()


class PaymentList(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = {
        "paid_course": ["exact"],
        "paid_lesson": ["exact"],
        "payment_method": ["exact"],
    }
    ordering_fields = ["payment_date"]
    ordering = ["payment_date"]


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        global price, product_price
        product_type = serializer.validated_data[
            "product_type"
        ]  # 'course' или 'lesson'
        product_id = serializer.validated_data["product_id"]  # ID курса или урока
        if product_type == "course":
            product = Course.objects.get(id=product_id)
            product_title = product.title
            product_price = product.price
            # Создаем продукт в Stripe для курса
            stripe_product = create_product_course(product_title)
            price = create_price(stripe_product.id, product_price)
            product.stripe_price_id = price.id
            product.save()
        elif product_type == "lesson":
            product = Lesson.objects.get(id=product_id)
            product_title = product.title
            product_price = product.price
            # Создаем продукт в Stripe для урока
            stripe_product = create_product_lesson(product_title)
            price = create_price(stripe_product.id, product_price)
            product.stripe_price_id = price.id
            product.save()
        session = create_checkout_session(price.id)
        payment = serializer.save(
            user=self.request.user,
            amount=product_price,
            session_id=session.id,
            payment_link=session.url,
        )
        return Response(
            {
                "checkout_url": session.url,
                "payment_id": payment.id,
            },
            status=status.HTTP_201_CREATED,
        )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ["create", "list"]:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save()
