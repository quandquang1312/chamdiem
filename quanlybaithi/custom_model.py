from rest_framework import serializers
from .models import Bailam, Baithi

class BailamSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Bailam
        fields = '__all__'

    def get_photo_url(self, bailam):
        request = self.context.get('request')
        photo_url = bailam.bai.url
        return request.build_absolute_uri(photo_url)


