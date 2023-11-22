from django.urls import path
from . import views


urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('tienda/', views.welcome, name='welcome'),
    path('tienda/login/', views.log_in, name='login'),
    path('tienda/singin/', views.sing_in, name='singin'),
    path('tienda/logout/', views.log_out, name='logout'),
    path('tienda/admin/producto/listado', views.listado_producto, name='producto_admin'),
    path('tienda/admin/producto/edicion/<int:pk>/', views.edit_producto, name='producto_editar'),
    path('tienda/admin/producto/nuevo/', views.nuevo_producto, name='producto_nuevo'),
    path('tienda/admin/producto/eliminar/<int:pk>/', views.admin_eliminar, name='producto_eliminar'),
    path('tienda/checkout/<int:pk>/', views.checkout, name='confimar_compra'),
    path('tienda/informe/marcas/', views.informe_marca, name='informe_marca'),
    path('tienda/informe/topProductos', views.top_productos, name='top_productos'),
    path('tienda/historial', views.historial_compras, name='historial'),
    path('tienda/informe/topClientes', views.top_clientes, name='top_clientes'),
]
