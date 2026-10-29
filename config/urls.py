from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from core.views import AssetViewSet

# Створюємо роутер і реєструємо наш ViewSet
router = DefaultRouter()
router.register(r'assets', AssetViewSet, basename='asset')

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT токени
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Підключаємо всі маршрути для assets: /api/assets/
    path('api/', include(router.urls)),
]