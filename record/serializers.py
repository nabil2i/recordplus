from rest_framework import serializers

from .models import RecordedVideo


class RecordedVideoSerializer(serializers.ModelSerializer):
  class Meta:
    model = RecordedVideo
    fields = ['id', 'title', 'description', 'get_video_url']
