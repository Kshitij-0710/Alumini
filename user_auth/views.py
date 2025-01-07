from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.contrib.auth import authenticate
from .models import User  # Replace with your actual user model
from .serializers import UserSerializer  # Create a serializer for your user model

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()  # Your user model's queryset
    serializer_class = UserSerializer  # Your user serializer
    permission_classes = [AllowAny]  # Set permissions as needed

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if not user:
            return Response({"error": "Invalid credentials"}, status=HTTP_400_BAD_REQUEST)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=HTTP_200_OK)
