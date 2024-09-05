from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import User
from .serializers import UserSerializer


@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = get_object_or_404(User, username=username)
    print("login test")
    if check_password(password, user.password):

        django_login(request, user)
        return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['PUT'])
def update_user(request, key):
    user = get_object_or_404(User, pk=key)  # 获取指定的用户对象
    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_user(request, key):
    user = get_object_or_404(User, pk=key)
    # 检查用户是否为超级用户（可根据需要添加更多逻辑）
    if user.is_superuser:
        return Response({"message": "Cannot delete a superuser"}, status=status.HTTP_403_FORBIDDEN)

    # 执行删除操作前的额外逻辑，例如日志记录、发送通知等
    # logging.info(f"User {user.username} is being deleted by {request.user.username}")
    # 删除用户
    user.delete()
    # 返回自定义的响应消息
    return Response({"message": f"User {user.username} deleted successfully"}, status=status.HTTP_200_OK)