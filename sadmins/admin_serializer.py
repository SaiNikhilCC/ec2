from rest_framework import serializers
from main import models
import random
import uuid




class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = "__all__"
    def create(self,validated_data):
        product = models.Product.objects.create(slug=validated_data['slug'],name=validated_data['name'], description=validated_data['description'],category = validated_data['category'],sub_category = validated_data['sub_category'], countInStock = validated_data['countInStock'], price = validated_data['price'],brand = validated_data['brand'],image=validated_data['image'])
        product.save()
        return product


class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductImages
        fields = "__all__"
    def create(self, validated_data):
        image_product = models.ProductImages.objects.create(product = validated_data['product'],image =validated_data['image'] )
        image_product.save()
        return image_product

# Product Reviews
class ProductReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reviews
        fields = "__all__"
    def create(self,validated_data):
        review = models.Reviews.objects.create(user=validated_data['user'],name=validated_data['name'],product=validated_data['product'],comment=validated_data['comment'],rating=validated_data['rating'])
        review.save()
        return review

class ProductSerializerWithImages(serializers.ModelSerializer):
    images = ProductImagesSerializer(many=True,read_only = True)
    reviews = ProductReviewsSerializer(many=True,read_only=True)
    class Meta:
        model = models.Product
        fields = "__all__"
        depth = 1










class CarouselSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Carousel
        fields = "__all__"

    def create(self,validated_data):
        carousel = models.Carousel.objects.create(carousel_image = validated_data['carousel_image'], navigation_link = validated_data['navigation_link'])
        carousel.save()
        return carousel



class ReplyToReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReplyReviews
        fields = "__all__"
    
    def create(self, validated_data):
        reply_review = models.ReplyReviews.objects.create(review = validated_data['review'],reply_text = validated_data['reply_text'])
        reply_review.save()
        return reply_review













