from django.urls import path,include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterUser,LogoutView,StyleConfigViewSet,StyleSuggestView,CommunityStyleView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'styles', StyleConfigViewSet, basename='style')
router.register(r'community/styles',CommunityStyleView, basename='CommunityStyle')

urlpatterns = [
    path('auth/register/', RegisterUser.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/',LogoutView.as_view(),name="logout"),
    path('chatbot/suggest/',StyleSuggestView.as_view(),name="suggest"),
    path('',include(router.urls))
]