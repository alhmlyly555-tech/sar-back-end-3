from django.urls import path
from .views import SARAnalysisView, SARResultView

urlpatterns = [
    path('analyze/', SARAnalysisView.as_view(), name='sar-analyze'),
    path('result/<str:task_id>/', SARResultView.as_view(), name='sar-result'),
]