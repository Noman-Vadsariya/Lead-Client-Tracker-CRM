from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'leads', views.LeadViewSet)
router.register(r'clients', views.ClientViewSet)
router.register(r'notes', views.NoteViewSet)
router.register(r'followups', views.FollowUpViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
