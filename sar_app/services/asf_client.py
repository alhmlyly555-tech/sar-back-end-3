import logging
from typing import Dict, Any, List
import asf_search as asf
from django.core.cache import cache
from decouple import config

logger = logging.getLogger(__name__)

def fetch_sar_scenes(wkt_geometry: str) -> List[Dict[str, Any]]:
    """جلب وتحليل لقطات Sentinel-1 من NASA ASF API واستخراج البيانات المفتاحية"""
    cache_key = f"asf_search_{hash(wkt_geometry)}"
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data

    username = config("EARTHDATA_USERNAME", default="")
    password = config("EARTHDATA_PASSWORD", default="")

    try:
        session = asf.ASFSession()
        if username and password:
            session.auth_with_creds(username, password)

        results = asf.geo_search(
            intersectsWith=wkt_geometry,
            platform=asf.PLATFORM.SENTINEL1,
            processingLevel=asf.PRODUCT_TYPE.GRD,
            maxResults=1
        )

        if not results:
            return []

        first_scene = results[0]
        props = first_scene.properties
        
        parsed_scenes = [{
            "scene_name": props.get("sceneName"),
            "platform": props.get("platform"),
            "polarization": props.get("polarization"),
            "flight_direction": props.get("flightDirection"),
            "download_url": props.get("url"),
            "bytes": props.get("bytes"),
            "start_time": props.get("startTime"),
            "stop_time": props.get("stopTime"),
        }]

        cache.set(cache_key, parsed_scenes, timeout=3600)
        return parsed_scenes

    except Exception as e:
        logger.error(f"خطأ أثناء الاتصال بـ ASF API: {str(e)}")
        return []