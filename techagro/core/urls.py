from rest_framework import routers
from django.urls import path, include
from .views import ProdutorRuralViewSet, EnderecoViewSet

router = routers.DefaultRouter()
router.register(r'produtores', ProdutorRuralViewSet)
router.register(r'enderecos', EnderecoViewSet)

urlpatterns = router.urls
