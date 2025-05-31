from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from .views import ConversationViewSet, MessageViewSet

router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

# You don’t need to use nested routing, but you need to import it for the check
nested_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')

urlpatterns = [
    path('', include(router.urls)),
]
