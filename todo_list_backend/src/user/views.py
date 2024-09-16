from django.contrib.auth.hashers import make_password
from rest_framework import generics, status
from rest_framework.response import Response

from user.models import CustomUser
from user.serializers import UserSerializer


class CreateUserAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        data = {
            'username': request.data.get('username'),
            'password': make_password(request.data.get('password')),
        }
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
