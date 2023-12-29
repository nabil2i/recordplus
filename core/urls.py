from django.urls import path
from .views import LoginView, RegisterView, VerifyEmail, logout_view

urlpatterns = [
  # path('', home, name="mylogin"),
  path('register/', RegisterView.as_view(), name="register"),
  path('verify-email/', VerifyEmail.as_view(), name="verify-email"),
  path('login/', LoginView.as_view(), name="login"),
  path('logout/', logout_view, name="logout"),
]
