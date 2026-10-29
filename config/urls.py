from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Вбудована панель адміністратора Django
    path('admin/', admin.site.urls),

    # Ендпоінти для роботи з JWT-токенами:
    # 1. Отримання пари токенів (access + refresh) за username та password
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # 2. Оновлення access-токена за допомогою refresh-токена
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]