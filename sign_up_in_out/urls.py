from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('blog/', views.blog, name='blog'),
    path('blog/newpost/', views.newpost, name='newpost'),
    path('blog/myposts/', views.myposts, name='myposts'),
    path('blog/signout/', views.signout)
]