from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from task.models import Category, Task
from task.serializers import CategorySerializer, TaskSerializer


class CategoryAPIView(APIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        categories = Category.objects.filter(user=request.user.id)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {'name': request.data.get('name')}
        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, category_id, *args, **kwargs):
        category = self.get(category_id, request.user.id)
        if not category:
            return Response(
                {'res': 'Object does not exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {'name': request.data.get('name')}
        serializer = CategorySerializer(instance=category, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, category_id, *args, **kwargs):
        category = self.get(category_id, request.user.id)
        if not category:
            return Response(
                {"res": "Object does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        category.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )


class CategoryAllAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        categories = Category.objects.filter(user=request.user.id)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TaskAPIView(APIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get(self, request, *args, **kwargs):
        tasks = Task.objects.select_related('category').filter(user=request.user.id)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'title': request.data.get('title'),
            'content': request.data.get('content'),
            'due_date': request.data.get('due_date'),
            'category': request.data.get('category'),
            'user': request.data.get('category')
        }
        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, task_id, *args, **kwargs):
        task = self.get(task_id, request.user.id)
        if not task:
            return Response(
                {'res': 'Object does not exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'title': request.data.get('title'),
            'content': request.data.get('content'),
            'due_date': request.data.get('due_date'),
            'category': request.data.get('category'),
            'user': request.data.get('category')
        }
        serializer = CategorySerializer(instance=task, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, category_id, *args, **kwargs):
        task = self.get(category_id, request.user.id)
        if not task:
            return Response(
                {"res": "Object does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        task.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )


class TaskAllAPIView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get(self, request, *args, **kwargs):
        tasks = Task.objects.select_related('category').filter(user=request.user.id)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TaskAllByCategoryAPIView(APIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get(self, request, category_id, *args, **kwargs):
        tasks = Task.objects.select_related('category').filter(
            user=request.user.id,
            category=category_id
        )
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
