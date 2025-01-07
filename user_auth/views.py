from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from django.contrib.auth import authenticate
from django.contrib.auth.models import User  # Replace with your actual user model
from .serializers import UserSerializer  # Create a serializer for your user model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  # Replace with your actual user model
        fields = ['username', 'password', 'email']  # Add any other fields you need


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()  
    serializer_class = UserSerializer  
    permission_classes = [AllowAny]  

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def signup(self, request):
        """
        Handle user signup.
        """
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if not username or not password or not email:
            return Response({"error": "Username, password, and email are required"}, status=HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already registered"}, status=HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password, email=email)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=HTTP_201_CREATED)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        """
        Handle user login.
        """
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if not user:
            return Response({"error": "Invalid credentials"}, status=HTTP_400_BAD_REQUEST)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=HTTP_200_OK)
