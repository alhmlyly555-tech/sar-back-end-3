from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SARAnalysisInputSerializer, SARAnalysisResultSerializer
from .tasks import run_sar_analysis_task
from .models import SARAnalysisResult

class SARAnalysisView(APIView):
    def post(self, request):
        serializer = SARAnalysisInputSerializer(data=request.data)
        if serializer.is_valid():
            wkt = serializer.validated_data['wkt']
            task = run_sar_analysis_task.delay(wkt)
            return Response({"task_id": task.id, "status": "PROCESSING"}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SARResultView(APIView):
    def get(self, request, task_id):
        try:
            result_obj = SARAnalysisResult.objects.get(task_id=task_id)
            serializer = SARAnalysisResultSerializer(result_obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except SARAnalysisResult.DoesNotExist:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)