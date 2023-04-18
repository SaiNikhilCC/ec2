from jsonschema import ValidationError
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from ecommerce.customauth import CustomAuthentication
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from main import models
from . import enduser_serializers
from rest_framework.filters import SearchFilter
from rest_framework import generics
from sadmins import admin_serializer


# FAST2SMS API To Send OTP Code
url = "https://www.fast2sms.com/dev/bulkV2"

def sendsms(num, phone):
    payload = f"sender_id=FTWSMS&message=To Verify Your Mobile Number with Time2Time News is {num} &route=v3&numbers={phone}"
    print(payload)
    headers = {
        'authorization': "ulBGWHeNb4qJ9KmyA1fip0RdPYh6kXjwEscTSQ3ODFvC2rgnIZezvgnxpTBcjmlJZQAkY7LKVSHGMU4d",
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
    }
    response = "sent"
    response = requests.request("POST", url, data=payload, headers=headers)
    return True
# End of FAST2SMS API


# USER REGISTRATION AND REQUESTS FOR OTP
class RegisterUser(APIView):
    try:
        def post(self, request):
            serializer = enduser_serializers.EndUserSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({'status': 403, 'errors': serializer.errors, 'message': 'some error occurred'})
            serializer.save()
            otp = serializer.data['otp']
            phone = serializer.data['phone']
            # sendsms(otp,phone)
            print("OTP to Verify Your Number is : ",otp, " -----> sent to : ", phone)
            return Response({
                'status': 200,
                'data': serializer.data,
                'message': 'Success'
            })
    except Exception as e:
        raise ValidationError('Somthing Went Wrong')


# USER ENTERS OTP AND GETS VERIFIED BASED ON HIS UUID AND OTP
class VerifyOtp(APIView):
    try:
        def post(self, request):
            if models.EndUser.objects.filter(uid=request.data["uid"], otp=request.data["otp"]):
                user = models.EndUser.objects.get(uid=request.data['uid'])
                user.is_verified = True
                user.otp = ""
                user.save()
                refresh = AccessToken.for_user(user)
                updated_user = models.EndUser.objects.filter(uid=request.data["uid"])
                serializer = enduser_serializers.EndUserSerializer(updated_user, many=True)
                response = Response({
                    'status': 200,
                    'data': serializer.data,
                    'access': str(refresh),
                    'message': 'Success'
                })
                response.content_type = "application/json"
                return response
            else:
                return Response({
                    'status': 400,
                    'message': 'Incorrect otp'
                })
    except Exception as e:
        raise ValidationError('Something Went Wrong')


# Edit Users Profile
class EditUsersProfile(APIView):
    def post(self,request,user_id):
        user_details = models.EndUser.objects.get(pk=user_id)
        user_details.name = request.data['name']
        user_details.save()

        updated_user_details = models.EndUser.objects.filter(uid=user_id)
        updated_user_details_serializer = enduser_serializers.EndUserSerializer(updated_user_details,many=True)

        return Response({
            "status":200,
            "data":updated_user_details_serializer.data,
            "message":"Profile Updated Succesfully"
        })

#############################################################   User Cart Details   #####################################################################
# User Add To Cart 
class AddToCart(APIView):
    def post(self,request):
        serializer = enduser_serializers.CartItemsSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'status': 403,
                'errors': serializer.errors,
                'message': 'Some Error Occurred'
            })
        else:
            serializer.save()
            return Response({
                'status': 200,
                'errors': serializer.data,
                'message': 'Item added To Cart Succesfully'
            })


# Users Cart List 
class UsersCart(APIView):
    def get(self,request,user_id):
        user_cart = models.CartItems.objects.filter(user_id = user_id)
        user_cart_serializer = enduser_serializers.CartItemsSerializer(user_cart, many=True)
        return Response({
            'status': 200,
            'data': user_cart_serializer.data,
            'message': 'Users Cart Items Fetched Succesfully'
        })


#############################################################   Products   #####################################################################
# All Products List Without Token Authenticatio
class AllProducts(APIView):
    # authentication_classes = [CustomAuthentication]
    def get(self,request):
        products = models.Product.objects.all()
        serializer = admin_serializer.ProductSerializerWithImages(products,many=True)
        return Response({
            'status': 200,
            'data': serializer.data,
            'message': 'All Products Fetched Succesfully'
        })


# Particular Product Details Without Token Authentication
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

# Search Product
class SearchProduct(generics.ListAPIView):
    queryset = models.Product.objects.all()
    # serializer_class = admin_serializer.ProductSerializer
    serializer_class = admin_serializer.ProductSerializerWithImages
    filter_backends = [SearchFilter]
    search_fields = ['description','product_title']

#############################################################   Orders   #####################################################################

# Placing An Order By End User
class CreateOrders(APIView):
    def post(self,request):
        order_serializer = enduser_serializers.OrdersSerializer(data= request.data)
        if not order_serializer.is_valid():
            return Response({
                'status': 403,
                'errors': order_serializer.errors,
                'message': 'Some Error Occurred'
            })
        else:
            order_serializer.save()
            return Response({
                'status': 403,
                'data': order_serializer.data,
                'message': 'Order Placed Succesfully'
            })


# Order Cancel Request API by End User
class RequestOrderCancellation(APIView):
    def post(self,request,order_id):
        order = models.Orders.objects.get(pk = order_id)
        if order.order_status != "Requested for Cancellation":
            order.order_status = "Requested for Cancellation"
            order.save()
            updated_order_details = models.Orders.objects.filter(id = order_id)
            updated_order_serializer = enduser_serializers.OrdersSerializer(updated_order_details,many=True)
            return Response({
                'status': 200,
                'data': updated_order_serializer.data,
                'message': 'Cancel Request Sent Succesfully'
            })
        else:
            updated_order_details = models.Orders.objects.filter(id = order_id)
            updated_order_serializer = enduser_serializers.OrdersSerializer(updated_order_details,many=True)
            return Response({
                'status': 200,
                'data': updated_order_serializer.data,
                'message': 'Cancel Request Already Sent'
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

# Orders History
class OrdersHistory(APIView):
    def get(self,request,user_id):
        particular_users_orders = models.Orders.objects.filter(user_id = user_id)
        users_orders_serializer = enduser_serializers.OrdersSerializer(particular_users_orders,many=True)
        return Response({
            'status': 200,
            'data': users_orders_serializer.data,
            'message': 'Order History Fetched Succesfully'
        })


#############################################################   User Wishlist   #####################################################################

# Add Product To Wishlist
class AddToWishlist(APIView):
    def post(self,request):
        whislist_serializer = enduser_serializers.WishlistSerializer(data= request.data)
        if not whislist_serializer.is_valid():
            return Response({
                'status': 403,
                'errors': whislist_serializer.errors,
                'message': 'Some Error Occurred'
            })
        else:
            whislist_serializer.save()
            return Response({
                'status': 200,
                'data': whislist_serializer.data,
                'message': 'Item Added To Whishlist'
            })

# Particular Users Wishlist
class UsersWishList(APIView):
    def get(self,request,user_id):
        wishlist = models.Wishlist.objects.filter(user_id = user_id)
        whislist_serializer = enduser_serializers.WishlistSerializer(wishlist,many=True)
        return Response({
            'status': 200,
            'data': whislist_serializer.data,
            'message': 'Whishlist Fetched Succesfully'
        })

# Remove From Wishlist 
class RemoveFromWishlist(APIView):
    def delete(self,request,wishlist_id):
        if models.Wishlist.objects.filter(id = wishlist_id):
            wishlist = models.Wishlist.objects.get(pk = wishlist_id)
            wishlist.delete()
            return Response({
                'status': 200,
                'bool':True,
                'message': 'Item Removed From Whishlist Succesfully'
            })
        else:
            return Response({
                'status': 400,
                'bool':False,
                'message': 'Item Not Found In Wishlist'
            })
        
#############################################################   User Reviews   #####################################################################

# Post A Review
class PostReview(APIView):
    def post(self,request):
        review_serializer = enduser_serializers.ReviewSerializer(data = request.data)
        if not review_serializer.is_valid():
            return Response({
                'status': 403,
                'errors': review_serializer.errors,
                'message': 'Some Error Occurred'
            })
        else:
            review_serializer.save()
            return Response({
                'status': 200,
                'data': review_serializer.data,
                'message': 'Review Posted Succesfully'
            })

# Particular Products All Reviews
class ParticularProductReviews(APIView):
    def get(self,request,product_id):
        product_reviews = models.Reviews.objects.filter(product_id=product_id)
        product_reviews_serializer = enduser_serializers.ReviewSerializer(product_reviews,many=True)
        return Response({
            'status': 200,
            'data': product_reviews_serializer.data,
            'message': 'All Reviews Fetched Succesfully'
        })

# Edit A Particular Review
class DeleteReview(APIView):
    def delete(self,request,review_id):
        if models.Reviews.objects.filter(id = review_id):
            review = models.Reviews.objects.get(pk = review_id)
            review.delete()
            return Response({
                'status': 200,
                'bool':True,
                'message': 'Review Deleted Succesfully'
            })
        else:
            return Response({
                'status': 400,
                'bool':False,
                'message': 'Review With This Already Deleted'
            })

# Replies Received To a Particular Review
class ReceivedReviewsToAParticularReview(APIView):
    def get(self,request,review_id):
        replied_reviews = models.ReplyReviews.objects.filter(review = review_id)
        replied_review_serializer = admin_serializer.ReplyToReviewSerializer(replied_reviews,many=True)
        return Response({
            'status': 200,
            'data': replied_review_serializer.data,
            'message': 'All Reviews Fetched Succesfully'
        })









