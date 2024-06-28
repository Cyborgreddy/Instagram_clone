from django.urls import path,include
from . import views

urlpatterns = [
    path('sign_in/', views.sign_in, name='sign_in'),
    path('signout/', views.signout, name='signout'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('home/',views.home,name='home'),
    path('web/',views.web,name='web'),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('post/<int:id>/', views.post_detail, name='post_detail'),
    path('post/<int:id>/like/', views.like_post, name='like_post'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('posts/', views.post_list, name='post_list'),
    path('reels/', views.reel_list, name='reel_list'),
    path('posts/add/', views.add_post, name='add_post'),
    path('reels/add/', views.add_reel, name='add_reel'),
    path('user_search/', views.user_search, name='user_search'),

]