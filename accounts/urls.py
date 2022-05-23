from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.SignUpView.as_view(template_name='registration/sign-up.html'), name='signup'),
    path('profile/<str:pk>/', views.CustomerView.as_view(), name='profile'),
    path('profile/edit/<str:pk>/', views.CustomerUpdateView.as_view(), name='profile-edit'),

]
