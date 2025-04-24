from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'urls', views.URLViewSet)

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('stats/', views.StatsView.as_view(), name='stats'),
    path('api/', include(router.urls)),
    path('api/shorten/', views.shorten_url_api, name='shorten_api'),
    path('s/<str:short_code>/', views.redirect_to_original, name='redirect'),
] 