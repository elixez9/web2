from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('profile/<int:user_id>/', views.UserProfileView.as_view(), name='profile'),
    path('reset_password/', views.UserResetPasswordView.as_view(), name='reset_password'),
    path('reset/done/', views.UserResetPasswordDoneView.as_view(), name='password_reset_done'),
    path('confirm/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(), name='confirm'),
    path('complete/', views.UserPasswordResetCompleteView.as_view(), name='reset_complete'),
]
