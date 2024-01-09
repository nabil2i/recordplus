from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (LoginView, LogoutView, PasswordTokenCheckView,
                    RegisterView, RequestPasswordResetView, SetNewPasswordView,
                    VerifyEmailView, GoogleView)

urlpatterns = [
  # path('', home, name="mylogin"),
  path('google/callback/', GoogleView.as_view(), name="google"),
  path('register/', RegisterView.as_view(), name="register"),
  path('verify-email/', VerifyEmailView.as_view(), name="verify-email"),
  path('token/refresh/', TokenRefreshView.as_view(), name="refresh-token"),
  path('password-reset-request', RequestPasswordResetView.as_view(), name="request-password-reset"),
  path('password-reset/<uidb64>/<token>', PasswordTokenCheckView.as_view(), name="confirm-password-reset"),
  path('password-reset-complete/', SetNewPasswordView.as_view(), name="set-new-password"),
  path('login/', LoginView.as_view(), name="login"),
  path('logout/', LogoutView.as_view(), name="logout"),
]


handler404 = 'utils.views.error_404'
handler500 = 'utils.views.error_500'
