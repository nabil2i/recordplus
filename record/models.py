from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator
from .validators import validate_file_size

# Create your models here.
class RecordedVideo(models.Model):
  title = models.CharField(max_length=255)
  description = models.TextField()
  # cloudinary_url = models.URLField()
  video_file = models.FileField(upload_to='record/videos/',
                                validators=[
                                  validate_file_size,
                                  FileExtensionValidator(allowed_extensions=['mp4', 'webm', 'avi'])
                                  ],
                                blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return self.title

  # def get_video_url(self):
  #   if (self.video_file):
  #     return settings.BASE_URL + self.video_file.url
  #   return ''
