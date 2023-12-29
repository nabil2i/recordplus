from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator
from .validators import validate_file_size

User = settings.AUTH_USER_MODEL

# Create your models here.
class RecordedVideo(models.Model):
  title = models.CharField(max_length=255, null=True)
  description = models.TextField(null=True)
  video_file = models.FileField(upload_to='record/videos/',
                                validators=[
                                  # validate_file_size,
                                  FileExtensionValidator(allowed_extensions=['mp4', 'webm', 'avi'])
                                  ],
                                blank=True,
                                # null=True
                                )
  owner = models.ForeignKey(User, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return self.title

  def get_video_file_url(self):
    if (self.video_file):
      return settings.MEDIA_ROOT + '/' + self.video_file.name
    return None


class Transcription(models.Model):
  recorded_video = models.OneToOneField(RecordedVideo,
                                               on_delete=models.CASCADE,
                                               related_name='transcription')
  transcription_text = models.TextField(null=True)
  
  def __str__(self):
    return f"Transcription for video {self.recorded_video.title}"
  
  class Meta:
    ordering: ['-created_at']
