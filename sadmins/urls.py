from django.urls import path
from . import views


urlpatterns = [

    # Products
    path("add-product/",views.AddProduct.as_view()),
    path("all-products/",views.AllProducts.as_view()),
    path("product-details/<int:product_id>/",views.ParticularProductDetails.as_view()),
    path("edit-product-details/<int:product_id>/",views.EditProductDetails.as_view()),
    path("delete-product/<int:product_id>/",views.DeleteProduct.as_view()),

    # Carousels
    path("add-carousel/",views.AddNewCarousel.as_view()),
    path("delete-carousel/<int:carousel_id>/",views.DeleteCarousel.as_view()),
    # Customer Management
    path("all-customers/",views.ALLCustomers.as_view()),
    # Sales Report
    path("all-orders-report/",views.SalesReport.as_view()),
    path("products-out-of-stock/",views.ProductsOutOfStock.as_view()),
    path("products-in-stock/",views.ProductsInStock.as_view()),

    # Orders
    path("all-orders/",views.AllOrders.as_view()),
    path("order-details/<int:order_id>/",views.OrderDetails.as_view()),
    path("change-order-status/<int:order_id>/",views.ChangeOrderStatus.as_view()),
]








