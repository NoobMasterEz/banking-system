from django.urls import path, re_path

from .authentication.views import LoginViewSet, LogoutViewSet, ResetPasswordViewSet, PasswordResetConfirmViewSet, PasswordResetCompleteViewSet
from .views import IndexDashboardViews

app_name = 'dashboard'
urlpatterns = [
    path("", IndexDashboardViews.as_view(), name="index"),
    path('login/', LoginViewSet.as_view(), name="login"),
    path('logout/', LogoutViewSet.as_view(), name="logout"),
    path('password_reset/', ResetPasswordViewSet.as_view(), name="password_reset"),
    path('password_reset_done/', PasswordResetCompleteViewSet.as_view(), name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/',
         PasswordResetConfirmViewSet.as_view(),
         name='password_reset_confirm'),
]
