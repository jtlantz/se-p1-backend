from django.urls import path

from . import views
app_name = 'api'
urlpatterns = [
    #-----------------------------root url-----------------------------
    path('', views.index, name='index'),
    #-----------------------------vending machine endpoints-----------------------------
    path('vendingMachine/add/', views.addVendingMachine, name='addVendingMachine'),
    path('vendingMachine/view/<int:vending_id>', views.vendingMachine, name='vendingMachine'),
    path('vendingMachine/delete/<int:vending_id>', views.deleteVendingMachine, name='deleteVendingMachine'),
    path('vendingMachine/update/<int:vending_id>', views.updateVendingMachine, name='updateVendingMachine'),
    #-----------------------------product endpoints-----------------------------
    path('product/add/', views.addProduct, name='addProduct'),
    path('product/view/', views.allProducts, name='allProducts'),
    path('product/view/<int:product_id>', views.product, name='product'),
    path('product/delete/<int:product_id>', views.deleteProduct, name='deleteProduct'),
    path('product/update/<int:product_id>', views.updateProduct, name='updateProduct'),
    #-----------------------------stock endpoints-----------------------------
    path('stock/add/', views.addStock, name='addStock'),
    path('stock/view/', views.allStock, name='allStock'),
    path('stock/view/<int:stock_id>', views.stock, name='stock'),
    path('stock/delete/<int:stock_id>', views.deleteStock, name='deleteStock'),
    path('stock/update/<int:stock_id>', views.updateStock, name='updateStock'),
]