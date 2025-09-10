from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from game.views import home  # Импортируем новое представление

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # Главная страница
    path('accounts/', include('django.contrib.auth.urls')),  # Логин, логаут
    path('', include('game.urls')),  # Маршруты приложения game
]

# Для медиафайлов в разработке
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)