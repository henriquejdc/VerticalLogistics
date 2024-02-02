from rest_framework.routers import SimpleRouter

from logistics.views import OrderViewSet


router = SimpleRouter()
router.register(r'orders-by-user', OrderViewSet, basename='order_by_user')
urlpatterns = router.urls
