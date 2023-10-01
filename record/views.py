import os
import tempfile

from django.core.exceptions import SuspiciousFileOperation
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import SuspiciousFileOperation

from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import RecordedVideo
from .serializers import RecordedVideoSerializer
from .tasks import transcribe_video


class VideoViewSet(ModelViewSet):
  http_method_names = ['get', 'post', 'patch']
  queryset = RecordedVideo.objects.prefetch_related('transcription').all()
  serializer_class = RecordedVideoSerializer
  parser_classes = (MultiPartParser, FormParser, JSONParser)
  
  def create(self, request, *args, **kwargs):
    title = request.data.get('title')
    description = request.data.get('description')
    video_file = request.FILES.get('video_file')
    
    if not title:
      return Response({'error': "supply a title"})
    if not video_file:
      return Response({'error': "supply a video file"})
    
    video_instance = RecordedVideo.objects.create(
      title=title,
      description=description,
      video_file=video_file
    )
        
    # serializer = self.get_serializer(data=request.data)
    # serializer.is_valid(raise_exception=True)
    # video_instance = serializer.save()
    
    return Response({'video_id': video_instance.id}, status=status.HTTP_201_CREATED)
  
  @action(detail=True, methods=['PATCH'])
  def update_video_file(self, request, pk):
    video_chunk = request.FILES.get('video_chunk')
    
    if not pk or not video_chunk:
      return Response({'message': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
    
    video_instance = get_object_or_404(RecordedVideo, pk=pk)

    video_file_path = video_instance.get_video_file_url()
    
    try:
      with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        for chunk in video_chunk.chunks():
          temp_file.write(chunk)
                          
      existing_clip = VideoFileClip(video_file_path)
      new_clip = VideoFileClip(temp_file.name)
      final_clip = concatenate_videoclips([existing_clip, new_clip])
      final_clip.write_videofile(video_file_path,
                                #  method="compose",
                                #  codec="libx264"
                                  )
      # video_instance.video_file.save(video_chunk.name, video_chunk)
      return Response({'message': 'Chunk uploaded successfully'}, status=status.HTTP_200_OK)
    
    except SuspiciousFileOperation:
      return Response({'message': 'Invalid file operation'}, status=status.HTTP_400_BAD_REQUEST)
    
    finally:
      temp_file.close()
      if temp_file.name:
        os.remove(temp_file.name)

  @action(detail=True, methods=['POST'])
  def finalize_video_upload(self, request, pk):  
    if not pk:
      return Response({'message': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
    
    transcribe_video.delay(pk)
    
    return Response({'message': 'Transcription task initiated'}, status=status.HTTP_200_OK)
    
    # serializer = self.get_serializer(data=request.data)
    # serializer.is_valid(raise_exception=True)
    # video_instance = serializer.save()
    # transcribe_video.delay(video_instance.id)
    # return Response(serializer.data, status=status.HTTP_201_CREATED)
  
  @action(detail=True, methods=['GET'])
  def stream_video(self, request, pk):
    video = get_object_or_404(RecordedVideo, pk=pk)
    
    video_file_path = video.video_file.path
    
    file_extension = video.video_file.name.split('.')[-1].lower()
    
    content_types = {
            'mp4': 'video/mp4',
            'webm': 'video/webm',
            'avi': 'video/x-msvideo',
        }
    content_type = content_types.get(file_extension, 'video/mp4')
    
    try:
      def file_iterator(file_path, chunk_size=8192):
        with open(file_path, 'rb') as video_file:
            while True:
                chunk = video_file.read(chunk_size)
                if not chunk:
                    break
                yield chunk

      response = StreamingHttpResponse(file_iterator(video_file_path), content_type=content_type)
      response['Content-Disposition'] = f'inline; filename="{video_file_path}"'
      return response

      # with open(video_file_path, 'rb') as video_file:
      #   response = HttpResponse(video_file.read(), content_type=content_type)
      #   response['Content-Disposition'] = f'inline; filename="{video_file_path}"'
      #   return response
    except FileNotFoundError:
      return response({ 'message': 'Video not found'}, status=status.HTTP_404_NOT_FOUND)

      
      
# class VideoDetail(APIView):  
#   parser_classes = (MultiPartParser, FormParser)
  
#   def get(self, request, pk):
#     # retrieve video from database
#     video = get_object_or_404(RecordedVideo, pk=pk)
#     serializer = RecordedVideoSerializer(video)
    
#     video_file_path = video.video_file.path
    
#     response = HttpResponse(content_type='video/webm')
#     # inline: browser should try to display video directly if possible
#     response['Content-Disposition'] = f'inline; filename="{video_file_path}"'
    
#     # streaming the file
#     with open(video_file_path, 'rb') as video_file:
#       response.write(video_file.read())
    
#     return response
    
    # return Response(serializer.data)
    
    
# class VideoList(APIView):
#   def post(self, request):
#     # process recorded video, save video and return response
#     serializer = RecordedVideoSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
    
#     return Response({'message': 'Video saved successfully'}, status=status.HTTP_201_CREATED)
  
#   def get(self, request):
#     # get all videos
#     videos = RecordedVideo.objects.all()
#     serializer = RecordedVideoSerializer(videos, many=True)
#     # video_data = [{'title': video.title, 'description': video.description, 'video_file': video.video_file.url} for video in videos]
#     return Response(serializer.data)

# class VideoDetail(APIView):  
#   parser_classes = (MultiPartParser, FormParser)
  
#   def get(self, request, pk):
#     # retrieve video from database
#     video = get_object_or_404(RecordedVideo, pk=pk)
#     serializer = RecordedVideoSerializer(video)
    
#     video_file_path = video.video_file.path
    
#     response = HttpResponse(content_type='video/webm')
#     # inline: browser should try to display video directly if possible
#     response['Content-Disposition'] = f'inline; filename="{video_file_path}"'
    
#     # streaming the file
#     with open(video_file_path, 'rb') as video_file:
#       response.write(video_file.read())
    
#     return response
    
#     # return Response(serializer.data)
