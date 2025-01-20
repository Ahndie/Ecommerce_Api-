from django.urls import path, include
from .import views
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, UserCreateView, UserLoginView
from rest_framework_simplejwt import views as jwt_views

router = DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('product/', views.product, name='product'),
    path('auth/register/', UserCreateView.as_view(), name='register'),
    path('auth/login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
