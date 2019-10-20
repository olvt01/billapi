from django.urls import path, include
from rest_framework.routers import DefaultRouter

from bill import views


router = DefaultRouter()
router.register('bills', views.BillViewSet)
router.register('bills_detail', views.BillDetailViewSet)
router.register('subscribes', views.SubscribeViewSet)

app_name = 'bill'

urlpatterns = [
    path('', include(router.urls))
]
