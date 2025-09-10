from django.urls import path
from . import views

urlpatterns = [
    path('create-character/', views.create_character, name='create_character'),
    path('start/', views.start_scene, name='start_scene'),
    path('scene/<int:scene_id>/', views.scene_view, name='scene'),
    path('signup/', views.signup, name='signup'),
]