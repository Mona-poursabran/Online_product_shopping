from re import U
from django.urls import  path
from .views import *

urlpatterns=[
    
    path('', store, name= 'store'),
    path('cart/', cart, name= 'cart'),
    path('checkout/', checkout, name= 'checkout'),

    path('success_login/', success_login, name='success_login'),
    # path('view_detail/<int:pk>/', ViewDetail.as_view(), name='view_detail'),
    path('panel_admin/', AdminPanel.as_view(), name='admin_panel'),
    path('panel_admin/product-list/', ProductsList.as_view(), name = 'product_list'),
    path('panel_admin/product-list/<int:pk>', ProductDetail.as_view(), name="product_detail"),
    path('panel_admin/product-list/new-product/', CreateProduct.as_view(), name='new_product'),
    path('panel_admin/product-list/update/<int:pk>/', UpdateProduct.as_view(), name="update_product"),
    path('ajax_delete_item/<int:pk>', DeleteProduct.as_view(), name="delete_product"),
    path('search/', search_result, name= 'search'),
    path('<int:pk>/', get_info_search, name='s_p'),

    path('updateitem/', updateitem, name='update_item'),
    path('processorder/', processOrder, name= 'process_order'),

]