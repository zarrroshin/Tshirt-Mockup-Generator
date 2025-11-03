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
    """
    POST /api/mockups/generate/
    {
        "text": "Hello World",
        "font": "arial.ttf",          // optional
        "text_color": "#FFFFFF",      // optional
        "shirt_color": ["white", "black"] // optional
    }
    """
    text = request.data.get('text')
    font = request.data.get('font')
    text_color = request.data.get('text_color')
    shirt_colors = request.data.get('shirt_color')

    if not text:
        return Response({"error": "Field 'text' is required."}, status=400)

    task = generate_mockup.delay(text=text, font_name=font, text_color=text_color, shirt_colors=shirt_colors)
    return Response({
        "task_id": task.id,
        "status": "PENDING",
        "message": "Image generation started."
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