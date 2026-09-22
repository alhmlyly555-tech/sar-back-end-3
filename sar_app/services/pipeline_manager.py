import logging
from typing import Dict, Any
from .asf_client import fetch_sar_scenes
from .surface_extractor import extract_surface_features
from .predictive_analytics import analyze_predictive_risks

logger = logging.getLogger(__name__)

def run_full_sar_pipeline(wkt_geometry: str) -> Dict[str, Any]:
    """المدير الرئيسي لربط وتمرير البيانات بين خدمات التحليل الثلاث"""
    # 1. جلب بيانات المشهد الراداري الخام من ASF
    scenes = fetch_sar_scenes(wkt_geometry)
    raw_scene = scenes[0] if scenes else {}

    # 2. استخراج المعاملات ورطوبة السطح
    surface_results = extract_surface_features(wkt_geometry, raw_scene)

    # 3. التحليل التنبؤي ومخاطر الكوارث
    predictive_results = analyze_predictive_risks(surface_results)

    # تجميع الهيكل النهائي المكتمل لـ DB والـ Frontend
    return {
        "asf_raw_metadata": raw_scene,
        "raw_scene_download_url": raw_scene.get("download_url"),
        "surface_analysis": surface_results,
        "predictive_analytics": predictive_results,
        "pipeline_status": "SUCCESS"
    }