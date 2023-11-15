from rest_framework import serializers

from .models import RecordedVideo, Transcription


class TranscriptionSerializer(serializers.ModelSerializer):
  class Meta:
    model = Transcription
    fields = ['id', 'transcription_text']
    

class RecordedVideoSerializer(serializers.ModelSerializer):
  video_file = serializers.FileField(required=False)
  transcription = TranscriptionSerializer()
  class Meta:
    model = RecordedVideo
    fields = [
              'id',
              'title',
              'description',
              'video_file',
              'created_at',
              'transcription'
            ]
    
  def validate(self, data):
    title = data.get('title', '')
    video_file = data.get('video_file')
    
    if not video_file:
      raise serializers.ValidationError('Upload a video in format .avi, .webm, or .mp4')
    
    ## file should be max 100MB
    # max_size = 1024 * 1024 * 100  
    # if video_file.size > max_size:
    #   raise serializers.ValidationError(f'File size exceeds the limit of {max_size}MB.')
    
    ## title must be at least 5 characters long
    # if len(title) < 5:
    #   raise serializers.ValidationError('Title must be at least 5 characters long.')
    
    return data
