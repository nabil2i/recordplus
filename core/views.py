from django.shortcuts import render
import jwt
from rest_framework.generics import GenericAPIView
from .serializers import EmailVerificationSerializer, RegisterSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site 
from django.urls import reverse
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.
class RegisterView(GenericAPIView):
  serializer_class = RegisterSerializer
  
  def post(self, request):
    user = request.data
    serializer = self.serializer_class(data=user)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    user_data = serializer.data
    
    user = User.objects.get(email=user_data['email'])
    # print("user: ", user)
    
    token = RefreshToken.for_user(user).access_token
    # print("token1:", token)
    
    current_domain = get_current_site(request).domain
    relativeLink = reverse('verify-email')
    
    absolute_url = 'http://' + current_domain + relativeLink + "?token=" + str(token)
    email_body = 'Hi ' + user.username + '! ' + 'Click this link to verify your email \n' + absolute_url
    data = {
      'email_body': email_body,
      'email_subject': 'Verify your email',
      'to_email': user.email,
    }
    Util.send_email(data)
    
    return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(APIView):
  serializer_class = EmailVerificationSerializer
  token_param_config = openapi.Parameter(
    "token",
    in_=openapi.IN_QUERY,
    description="Verification token",
    type=openapi.TYPE_STRING
  )
  responses = {
    200: openapi.Response(
      description="Verify email successful",
      examples={
        "application/json": {"email": "Email successfully activated."},
      }
    ),
    # 400: openapi.Response(
    #   description="Error when activation link is expired",
    #   examples={
    #     "application/json": {"error" : "Activation link expired."},
    #     # "application/json": {"error" : "Invalid token."},
    #   },  
    # ),
    400: openapi.Response(
      description="Error during email verification",
      examples={
          "application/json": {"error": "Activation link expired or Invalid token."},
      },
    ),
  }
  
  @swagger_auto_schema(
    operation_summary='Verify Email',
    operation_description='This endpoint verifies the email.',
    manual_parameters=[token_param_config],
    responses=responses
  )
  def get(self, request):
    token = request.GET.get('token')
    # print("token: ", token)
    try:
      payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
      # print("payload :", payload)
      user = User.objects.get(id=payload['user_id'])
      # print("user :", user)
      
      if not user.is_verified:
        user.is_verified = True
        user.save()
        return Response({ 'email': 'Email successfully activated.'}, status=status.HTTP_200_OK)
      else:
        return Response({'error': 'Email has already been verified.'}, status=status.HTTP_200_OK)
    except jwt.ExpiredSignatureError as identifier:
      return Response({ 'error' : 'Activation link expired.'}, status=status.HTTP_400_BAD_REQUEST)
    except jwt.exceptions.DecodeError as identifier:
      return Response({ 'error' : 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)
