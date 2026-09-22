from rest_framework import serializers
from shapely.wkt import loads as load_wkt
from .models import SARAnalysisResult

class SARAnalysisInputSerializer(serializers.Serializer):
    wkt = serializers.CharField(
        required=True, 
        help_text="POLYGON((30.0 31.0, 30.1 31.0, 30.1 31.1, 30.0 31.1, 30.0 31.0))"
    )

    def validate_wkt(self, value):
        try:
            geom = load_wkt(value)
            if geom.geom_type != 'Polygon':
                raise serializers.ValidationError("المدخلات يجب أن تكون مضلعاً مكتملاً (Polygon).")
            return value
        except Exception as e:
            raise serializers.ValidationError(f"صيغة WKT غير صحيحة: {str(e)}")

class SARAnalysisResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SARAnalysisResult
        fields = '__all__'