from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name="home"),

    path('', views.home, name=""),

    path('register', views.register, name='register'),

    path('my-login', views.my_login, name = "my-login"),

    path('user-agreement', views.user_agreement, name="user-agreement"),

    path('user-logut', views.user_logout, name="user-logout"),

    path('dashboard',views.dashboard ,name="dashboard"),

    path('questionnaire', views.questionnaire, name="questionnaire"),

    path('recommendation', views.recommendation, name="recommendation"),

    path('prediction/<str:symbol>', views.prediction, name="prediction"),
]