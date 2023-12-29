from django.urls import path
from .views import LoginView, PasswordTokenCheck, RegisterView, RequestPasswordReset, SetNewPassword, TokenRefresh, VerifyEmail, logout_view

urlpatterns = [
  # path('', home, name="mylogin"),
  path('register/', RegisterView.as_view(), name="register"),
  path('verify-email/', VerifyEmail.as_view(), name="verify-email"),
  path('token/refresh/', TokenRefresh.as_view(), name="refresh-token"),
  path('password-reset-request', RequestPasswordReset.as_view(), name="request-password-reset"),
  path('password-reset/<uidb64>/<token>', PasswordTokenCheck.as_view(), name="confirm-password-reset"),
  path('password-reset-complete/', SetNewPassword.as_view(), name="set-new-password"),
  path('login/', LoginView.as_view(), name="login"),
  path('logout/', logout_view, name="logout"),
]
