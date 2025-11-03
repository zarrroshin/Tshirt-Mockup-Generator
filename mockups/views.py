from rest_framework.decorators import api_view
from rest_framework.response import Response
from .tasks import generate_mockup
from celery.result import AsyncResult
from rest_framework import generics,filters
from .models import Mockup
from .serializers import MockupSerializer
from rest_framework.pagination import PageNumberPagination

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
def task_status_view(request, task_id):
    """
    Returns the status and results of a given Celery task.
    """
    task_result = AsyncResult(task_id)

    if task_result.status == "SUCCESS":
        # task_result.result شامل URLهای عکس‌هاست
        results = []
        for image_url in task_result.result:
            mockup = Mockup.objects.filter(image__icontains=os.path.basename(image_url)).first()
            if mockup:
                results.append({
                    "image_url": request.build_absolute_uri(mockup.image.url),
                    "created_at": mockup.created_at.isoformat()
                })

        return Response({
            "task_id": task_id,
            "status": task_result.status,
            "results": results
        })

    return Response({
        "task_id": task_id,
        "status": task_result.status,
        "results": None
    })


class MockupPagination(PageNumberPagination):
    page_size = 5  # تعداد آیتم در هر صفحه
    page_size_query_param = 'page_size'


class MockupListView(generics.ListAPIView):
    """
    GET /api/v1/mockups/
    Supports ?search=<text> and pagination.
    """
    queryset = Mockup.objects.all().order_by('-created_at')
    serializer_class = MockupSerializer
    pagination_class = MockupPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['text']
