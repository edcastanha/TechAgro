from rest_framework import routers
from .views import (
    ProdutorViewSet,
    PropriedadeViewSet,
    SafraViewSet,
    AtividadeRuralViewSet
)

router = routers.DefaultRouter()
router.register(r'produtores', ProdutorViewSet)
router.register(r'propriedades', PropriedadeViewSet)
router.register(r'safras', SafraViewSet)
router.register(r'atividades', AtividadeRuralViewSet)

urlpatterns = router.urls
