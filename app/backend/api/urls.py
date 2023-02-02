from django.urls import path

from . import views

app_name = "api"
urlpatterns = [
    # -----------------------------vending machine endpoints-----------------------------
    path("", views.get_all_machines, name="get_all_machines"),
    path("machine/add/", views.add_vending_machine, name="add_vending_machine"),
    path("machine/view/<int:vending_id>", views.get_machine, name="get_machine"),
    path("machine/delete/<int:vending_id>", views.delete_vending_machine, name="delete_vending_machine"),
    path("machine/update/<int:vending_id>", views.update_vending_machine, name="update_vending_machine"),
    # -----------------------------product endpoints-----------------------------
    path("product/view/", views.get_all_products, name="get_all_products"),
    path("product/add/", views.add_product, name="add_product"),
    path("product/view/<int:product_id>", views.get_product, name="get_product"),
    path("product/delete/<int:product_id>", views.delete_product, name="delete_product"),
    path("product/update/<int:product_id>", views.update_product, name="update_product"),
    # -----------------------------stock endpoints-----------------------------
    path("stock/view/", views.get_all_stock, name="get_all_stock"),
    path("stock/add/", views.add_stock, name="add_stock"),
    path("stock/view/<int:stock_id>", views.get_stock, name="stock"),
    path("stock/delete/<int:stock_id>", views.delete_stock, name="delete_stock"),
    path("stock/update/<int:stock_id>", views.update_stock, name="update_stock"),
]
