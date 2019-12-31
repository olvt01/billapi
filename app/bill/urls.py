from django.urls import path, include
from rest_framework.routers import DefaultRouter

from bill import views


router = DefaultRouter()
router.register('committees', views.CommitteeViewSet)
router.register('bills', views.BillViewSet)
router.register('bills_detail', views.BillViewViewSet)
router.register('bills_cover', views.BillViewCoverViewSet)
router.register('subscribes', views.SubscribeViewSet)
router.register('bookmarks', views.BookmarkViewSet)

app_name = 'bill'

urlpatterns = [
    path('', include(router.urls))
]
