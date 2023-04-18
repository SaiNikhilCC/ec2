from jsonschema import ValidationError
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from ecommerce.customauth import CustomAuthentication
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from main import models
from . import admin_serializer
from rest_framework import generics


#############################################################   Super Admin   #####################################################################
# Super Admin Login View
class SuperAdminLoginView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        superadmin = models.SuperAdminAcc.objects.filter(username=username, password=password)
        serializer = admin_serializer.SuperAdminAccSerializer(superadmin, many=True)
        admin_acc = models.SuperAdminAcc.objects.get(username=username)
        access_token = AccessToken.for_user(admin_acc)
        if superadmin:
            return Response({
                "status": 200,
                "bool": True,
                "data": serializer.data,
                'token': str(access_token),
            })
        else:
            return Response({
                "bool": False,
                "message": "Invalid Credentials !!!"
            })


#############################################################   Products   #####################################################################
# Add Products View with token authentication
class AddProduct(APIView):
    # authentication_classes = [CustomAuthentication]
    def post(self, request):
        serializer = admin_serializer.ProductSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'status': 403,
                'errors': serializer.errors,
                'message': 'some error occurred'
            })
        else:
            serializer.save()
            serialized_product_id = serializer.data['id']
            #  Saving Images
            images = request.data.getlist('img')
            print(images)
            for i in images:
                img_serializer = admin_serializer.ProductImagesSerializer(data={'product': serialized_product_id, 'image': i})
                if img_serializer.is_valid():
                    img_serializer.save()
                else:
                    return Response({
                        'status': 403,
                        'errors': img_serializer.errors,
                        'message': 'some error occurred'
                    })
            all_images = models.ProductImages.objects.filter(product=serialized_product_id)
            all_images_serializer = admin_serializer.ProductImagesSerializer(all_images,many=True)
            return Response({
                'status': 200,
                'data': serializer.data,
                'images':all_images_serializer.data,
                'message': 'success'
            })


# All Products List With Token Authenticatio
class AllProducts(APIView):
    # authentication_classes = [CustomAuthentication]
    def get(self,request):
        products = models.Product.objects.all()
        for product in products:
            product.calculate_rating()
        serializer = admin_serializer.ProductSerializerWithImages(products,many=True)
        return Response({
            'status': 200,
            'data': serializer.data,
            'message': 'All Products Fetched Succesfully'
        })


# Particular Product Details With Token Authentication
class ParticularProductDetails(APIView):
    # authentication_classes = [CustomAuthentication]
    def get(self,request,product_id):
        product = models.Product.objects.filter(id=product_id)
        serializer = admin_serializer.ProductSerializerWithImages(product,many=True)
        return Response({
            'status': 200,
            'data': serializer.data,
            'message': 'Products Details Fetched Succesfully'
        })


# Edit Product Details For Title and Description
class EditProductDetails(APIView):
    # authentication_classes = [CustomAuthentication]
    def post(self,request,product_id):
        product = models.Product.objects.get(pk=product_id)
        if request.data['product_title']:
            product.product_title = request.data['product_title']
        if request.data['description']:
            product.description = request.data['description']
        product.save()
        updated_product = models.Product.objects.filter(id=product_id)
        serializer = admin_serializer.ProductSerializerWithImages(updated_product,many=True)
        return Response({
            'status': 200,
            'data': serializer.data,
            'message': 'Products Details Fetched Succesfully'
        })


# Delete Product
class DeleteProduct(APIView):
    # authentication_classes = [CustomAuthentication]
    def delete(self,request,product_id):
        product_details = models.Product.objects.filter(id=product_id)
        if product_details:
            product = models.Product.objects.get(pk=product_id)
            product.delete()
            return Response({
                'status': 200,
                'bool':True,
                'message': 'Product Deleted Succesfully'
            })
        else:
            return Response({
                'status': 200,
                'bool':False,
                'message': 'No Product Found'
            })


#############################################################   Carousels   #####################################################################

# API View To Add New Carousel
class AddNewCarousel(APIView):
    def post(self,request):
        carousel_serializer = admin_serializer.CarouselSerializer(data=request.data)
        if not carousel_serializer.is_valid():
            return Response({
                'status': 403,
                'errors': carousel_serializer.errors,
                'message': 'some error occurred'
            })
        else:
            carousel_serializer.save()
            return Response({
                'status': 200,
                'errors': carousel_serializer.data,
                'message': 'New Carousel Added Succesfully'
            })


# API View To Delete Carousel
class DeleteCarousel(APIView):
    def delete(self,request,carousel_id):
        carousel_details = models.Carousel.objects.filter(id=carousel_id)
        if carousel_details:
            carousel = models.Carousel.objects.get(pk=carousel_id)
            carousel.delete()
            return Response({
                'status': 200,
                'bool':True,
                'message': 'Carousel Deleted Succesfully'
            })
        else:
            return Response({
                'status': 400,
                'bool':False,
                'message': 'No Carousel Found'
            })





#############################################################   Customer Management   #####################################################################


from enduser import enduser_serializers

class ALLCustomers(APIView):
    def get(self,request):
        all_customers = models.EndUser.objects.all()
        all_customers_serializer = enduser_serializers.EndUserSerializer(all_customers,many=True)
        return Response({
            "status":200,
            "data":all_customers_serializer.data,
            "message":"All Customers Details Fetched"
        })




#############################################################   Detailed Sales Report   #####################################################################
# All Orders Status API 
class SalesReport(APIView):
    def get(self,request):
        orders_placed = models.Orders.objects.filter(order_status = "Order Placed")
        orders_delivered = models.Orders.objects.filter(order_status = "Delivered")
        orders_shipped = models.Orders.objects.filter(order_status = "Shipped")
        orders_canceled = models.Orders.objects.filter(order_status = "Canceled")
        orders_return_request = models.Orders.objects.filter(order_status = "Requested for Return")

        orders_placed_serializer = enduser_serializers.OrdersSerializer(orders_placed,many=True)
        orders_delivered_serializer = enduser_serializers.OrdersSerializer(orders_delivered,many=True)
        orders_shipped_serializer = enduser_serializers.OrdersSerializer(orders_shipped,many=True)
        orders_canceled_serializer = enduser_serializers.OrdersSerializer(orders_canceled,many=True)
        orders_return_request_serializer = enduser_serializers.OrdersSerializer(orders_return_request,many=True)

        return Response({
            "status":200,
            "placed_orders":orders_placed_serializer.data,
            "orders_shipped":orders_shipped_serializer.data,
            "orders_delivered":orders_delivered_serializer.data,
            "orders_canceled":orders_canceled_serializer.data,
            "orders_requested_for_return":orders_return_request_serializer.data,
            "message":"ALL Sales reports Fetched"
        })



# API for products out of stock
class ProductsOutOfStock(APIView):
    def get(self,request):
        products_out_of_stock  = models.Product.objects.filter(no_of_products = 0)
        products_out_of_stock_serializer = admin_serializer.ProductSerializer(products_out_of_stock,many=True)
        return Response({
            "status":200,
            "data":products_out_of_stock_serializer.data,
            "message":"Products out of stock fetched"
        })

# API for Products In Stock
class ProductsInStock(APIView):
    def get(self,request):
        products_in_stock  = models.Product.objects.exclude(no_of_products = 0)
        products_in_stock_serializer = admin_serializer.ProductSerializer(products_in_stock,many=True)
        return Response({
            "status":200,
            "data":products_in_stock_serializer.data,
            "message":"Products out of stock fetched"
        })

#############################################################   Orders   #####################################################################
# API View for All Orders
class AllOrders(APIView):
    def get(self,request):
        orders = models.Orders.objects.all()
        orders_serializer = enduser_serializers.OrdersSerializer(orders,many=True)
        return Response({
            "status":200,
            "data":orders_serializer.data,
            "message":"all orders fetched"
        })


# Order Details
class OrderDetails(APIView):
    def get(self,request,order_id):
        order_details = models.Orders.objects.filter(id = order_id)
        order_details_serializer = enduser_serializers.OrdersSerializer(order_details,many=True)
        return Response({
            'status': 200,
            'data': order_details_serializer.data,
            'message': 'Order Details Fetched Succesfully'
        })


# Change Order Status
class ChangeOrderStatus(APIView):
    def post(self,request,order_id):
        order_details = models.Orders.objects.get(pk = order_id)
        order_details.order_status = request.data['order_status']
        order_details.save()
        updated_order_details = models.Orders.objects.filter(id = order_id)
        updated_order_details_serializer = enduser_serializers.OrdersSerializer(updated_order_details,many=True)
        return Response({
            'status': 200,
            'data': updated_order_details_serializer.data,
            'message': 'Order Details Fetched Succesfully'
        })

