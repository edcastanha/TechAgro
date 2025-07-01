from rest_framework import routers
from django.urls import path
from .views import (
    ProdutorViewSet,
    PropriedadeViewSet,
    SafraViewSet,
    AtividadeRuralViewSet
)
from .dashboard import DashboardView

router = routers.DefaultRouter()
router.register(r'produtores', ProdutorViewSet)
router.register(r'propriedades', PropriedadeViewSet)
router.register(r'safras', SafraViewSet)
router.register(r'atividades', AtividadeRuralViewSet)

urlpatterns = router.urls + [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]
