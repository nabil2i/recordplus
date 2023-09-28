from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from .serializers import RecordedVideoSerializer
from .models import RecordedVideo
from rest_framework.viewsets import ModelViewSet
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

# Create your views here.
class VideoViewSet(ModelViewSet):
  http_method_names = ['get', 'post']
  
  queryset = RecordedVideo.objects.all()
  serializer_class = RecordedVideoSerializer
  parser_classes = (MultiPartParser, FormParser)
  
  @action(detail=True, methods=['GET'])
  def stream_video(self, request, pk):
    video = get_object_or_404(RecordedVideo, pk=pk)
    
    video_file_path = video.video_file.path
    print(video_file_path)
    
    try:
      with open(video_file_path, 'rb') as video_file:
        response = HttpResponse(video_file.read(), content_type='video/mp4')
        response['Content-Disposition'] = f'inline; filename="{video_file_path}"'
        return response
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
