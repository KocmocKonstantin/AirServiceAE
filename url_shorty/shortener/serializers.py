from rest_framework import serializers
from .models import URL


class URLSerializer(serializers.ModelSerializer):
    short_url = serializers.SerializerMethodField()
    
    class Meta:
        model = URL
        fields = ['id', 'original_url', 'short_code', 'short_url', 'created_at', 'access_count']
        read_only_fields = ['short_code', 'created_at', 'access_count']
    
    def get_short_url(self, obj):
        request = self.context.get('request')
        if request is not None:
            return f"{request.scheme}://{request.get_host()}/s/{obj.short_code}"
        return f"/s/{obj.short_code}"
    
    def create(self, validated_data):
        validated_data['short_code'] = URL.generate_short_code()
        return super().create(validated_data) 