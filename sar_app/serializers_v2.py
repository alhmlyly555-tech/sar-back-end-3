from rest_framework import serializers
from shapely.wkt import loads as load_wkt
from shapely.errors import WKTReadingError
from .models import SARAnalysisResult

class SARAnalysisInputSerializer(serializers.Serializer):
    wkt = serializers.CharField(
        required=True,
        max_length=5000,
        help_text="مثال صيغة خماسية النقاط: POLYGON ((30.0 31.0, 30.1 31.0, 30.1 31.1, 30.0 31.1, 30.0 31.0))"
    )

    def validate_wkt(self, value):
        # 1. Protection against SQL / Script Injection
        clean_val = value.strip()
        if not clean_val.upper().startswith("POLYGON"):
            raise serializers.ValidationError("يجب أن تبدأ الإحداثيات بكلمة POLYGON.")

        try:
            geom = load_wkt(clean_val)
            
            # 2. Geometric Type Check
            if geom.geom_type != 'Polygon':
                raise serializers.ValidationError("يجب أن يكون الشكل الهندسي من نوع POLYGON حصراً.")

            # 3. Polygon Points & Bounds Check (5 points requirement as per dataset rules)
            coords = list(geom.exterior.coords)
            if len(coords) < 5:
                raise serializers.ValidationError("يجب أن يحتوي المضلع الجغرافي على 5 نقاط على الأقل مغلقة.")

            # 4. Limit Maximum Surface Area to prevent server overload
            if geom.area > 5.0: # Approx area restriction
                raise serializers.ValidationError("مساحة المضلع المطلوبة كبيرة جداً وتسبب ضغطاً على الخادم.")

            return clean_val

        except WKTReadingError:
            raise serializers.ValidationError("صيغة WKT النصية المرفقة غير صالحة برمجياً.")
        except Exception as e:
            raise serializers.ValidationError(f"خطأ في معالجة النطاق الجغرافي: {str(e)}")

class SARAnalysisResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SARAnalysisResult
        fields = '__all__'
        read_only_fields = ('task_id', 'created_at', 'updated_at', 'status')