from jsonschema import ValidationError
from rest_framework import serializers
from main import models
import random
import uuid


# End Users Signup Serializers
class EndUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EndUser
        fields = "__all__"
        
    def create(self, validated_data):
        otp_generated = random.randint(10000,99999)
        phone = validated_data['phone']
        if models.EndUser.objects.filter(phone=phone):
            user = models.EndUser.objects.get(phone=phone)
            user.otp=otp_generated
            user.save()
            return user
        else:
            user = models.EndUser.objects.create(dob = validated_data['dob'], gender = validated_data['gender'] ,name = validated_data['name'], phone = validated_data['phone'],uid = uuid.uuid4(), otp=otp_generated, email=validated_data['email'])
            user.save()
            return user


# End Users Cart Serializer
class CartItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CartItems
        fields = "__all__"

    def create(self,validated_data):
        product = models.Product.objects.get(pk=validated_data['product'].id)
        product.no_of_cart = product.no_of_cart+1
        product.save()
        cart_item = models.CartItems.objects.create(quantity = validated_data['quantity'],product = validated_data['product'], user = validated_data['user'])
        cart_item.save()
        return cart_item


# End User Orders Serializer
class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Orders
        fields = "__all__"

    def create(self, validated_data):
        product = models.Product.objects.get(pk=validated_data['product'].id)
        if product.no_of_products < validated_data['quantity']:
            raise serializers.ValidationError("Not Enough Products")
        else:
            orders = models.Orders.objects.create(landmark = validated_data['landmark'],colony = validated_data['colony'],street = validated_data['street'],hno=validated_data['hno'],mandal=validated_data['mandal'],disrtict=validated_data['disrtict'],state=validated_data['state'],user = validated_data['user'], product = validated_data['product'],quantity = validated_data['quantity'],purchased_price=validated_data['purchased_price'])
            product.no_of_products = product.no_of_products - validated_data['quantity']
            product.no_of_orders = product.no_of_orders+1
            product.save()
            orders.save()
            return orders


# End User Wishlist Serializer
class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Wishlist
        fields = "__all__"
    
    def create(self, validated_data):
        if models.Wishlist.objects.filter(user=validated_data['user'],product = validated_data['product']):
            raise serializers.ValidationError("Product Already Added to Wishlist")
        else:
            product = models.Product.objects.get(pk=validated_data['product'].id)
            product.no_of_wishlists = product.no_of_wishlists+1
            product.save()
            whislited = models.Wishlist.objects.create(user = validated_data['user'], product = validated_data['product'])
            whislited.save()
            return whislited


# End User Review Serializer
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reviews
        fields = "__all__"
    
    def create(self, validated_data):
        review = models.Reviews.objects.create(name=validated_data['name'],user = validated_data['user'], product = validated_data['product'], comment = validated_data['comment'],rating=validated_data['rating'])
        review.save()
        return review














