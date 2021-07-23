from django.urls import include, path
from rest_framework import routers
from . import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
   path('allconfiguraciones', views.configuracionAll),
    path('configuracion/<int:pk>', views.configuracion),
    path('allperfiles', views.perfilAll),
    path('perfil/<int:pk>', views.perfil),
    path('allperfilesE', views.perfilEAll),
    path('allpefilesP',views.perfilParametrizadoAll),
    path('perfilP/<int:pk>', views.perfilParametrizado),
    path('obtenerCategorias', views.get_categorias_perfil),
    path('crearcategorias/<int:pk>', views.create_categorias),
    path('categoriasPP/<int:pk>', views.categoriasPP),


]
router = routers.DefaultRouter()
router.register('configuraciones',views.ConfiguracionViewSet,'configuraciones')
router.register('perfiles',views.PerfilViewSet,'perfiles')
router.register('perfilesE', views.PerfilEViewSet,'perfilesE')
router.register('perfilesP', views.PerfilParametrizadoViewSet,'perfilesP')
router.register('categorias-perfilp', views.CategoriasPerfilParametrizadoViewSet,'categorias-perfilp')
urlpatterns = urlpatterns + router.urls

