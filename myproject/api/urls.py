from django.urls import path
from .views import RegisterView,LoginView,MessageView,UserView

urlpatterns = [ 
  
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('message', MessageView.as_view()),
    path('users', UserView.as_view())
 

]