from rest_framework.decorators import api_view
from rest_framework.response import Response
from .tasks import generate_mockup
from celery.result import AsyncResult
from rest_framework import generics
from .models import Mockup
from .serializers import MockupSerializer


@api_view(['GET'])
def hello(request):
    return Response({"message": "سلام زهرا 👋 پروژه با موفقیت کار می‌کنه!"})

@api_view(['POST'])
def generate_mockup_view(request):
    text = request.data.get('text', '')
    if not text:
        return Response({"error": "متن اجباری است."}, status=400)

    task = generate_mockup.delay(text)
    return Response({
        "task_id": task.id,
        "status": "PENDING",
        "message": "در حال ساخت تصویر..."
    })


@api_view(['GET'])
def get_task_status(request, task_id):
    result = AsyncResult(task_id)
    return Response({
        "task_id": task_id,
        "status": result.status,
        "result": result.result if result.ready() else None
    })

class MockupListView(generics.ListAPIView):
    queryset = Mockup.objects.all().order_by('-created_at')
    serializer_class = MockupSerializer