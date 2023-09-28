from django.db import models


# Create your models here.
class RecordedVideo(models.Model):
  title = models.CharField(max_length=255)
  description = models.TextField()
  # cloudinary_url = models.URLField()
  video_file = models.FileField(upload_to='record/videos',
                                blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return self.title

  def get_video_url(self):
    if (self.video_file):
      return 'http://127.0.0.1:8000' + self.video_file._url
    return ''
