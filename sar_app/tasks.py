from celery import shared_task
from .models import SARAnalysisResult
from .services.pipeline_manager import run_full_sar_pipeline

@shared_task(bind=True, max_retries=3)
def run_sar_analysis_task(self, task_id, wkt_geometry):
    try:
        SARAnalysisResult.objects.filter(task_id=task_id).update(
            status=SARAnalysisResult.Status.PROCESSING
        )
        
        # تنفيذ مراحل التحليل الموزعة
        result_payload = run_full_sar_pipeline(wkt_geometry)
        
        raw_url = result_payload.get("raw_scene_download_url")
        
        record = SARAnalysisResult.objects.get(task_id=task_id)
        record.status = SARAnalysisResult.Status.SUCCESS
        record.result_data = result_payload
        if raw_url:
            record.raw_scene_download_url = raw_url
        record.save()
        
    except Exception as exc:
        SARAnalysisResult.objects.filter(task_id=task_id).update(
            status=SARAnalysisResult.Status.FAILED
        )
        raise self.retry(exc=exc, countdown=10)