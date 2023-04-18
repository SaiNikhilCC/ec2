from django.db import models
import uuid

# UserBase Model
class UserBaseModel(models.Model):
    id = models.CharField(default ="", max_length=100)
    uid = models.UUIDField(primary_key=True, editable=False,default = uuid.uuid4())
    created_date = models.DateField(auto_now_add=True)
    created_time= models.TimeField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    updated_time = models.TimeField(auto_now=True)
    class Meta:
        abstract = True

#############################################################   Super Admin Models   #####################################################################
# Super Admin Account
class SuperAdminAcc(models.Model):
    username = models.CharField(max_length=250)
    password = models.CharField(max_length=200)
    def __str__(self):
        return self.username

# {
#     "_id": "642aec43fa858319a15a47bc",
#     "name": "Nike Slim shirt", (chatField)
#     "slug": "nike-slim-shirt", (chatField)
#     "image": "/images/p1.jpg", (FileField)
#     "brand": "Nike", (chatField)
#     "category": "Shirts", (chatField)
#     "description": "high quality shirt", (TextField)
#     "price": 10, (IntegerField)
#     "countInStock": 10, (IntegerField)
#     "rating": 3,      (Calculate Dynamically)
#     "numReviews": 1,  (Calculate Dynamically)
#     "__v": 1,
#     "createdAt": "2023-04-03T15:09:55.412Z",  (DateTimeField ,auto_now_add)
#     "updatedAt": "2023-04-05T17:54:10.622Z",  (DateTimeField, auto_now)
#     "images": [

#     ],
#     "reviews": [
#       {
#         "name": "Muzeef",                    (CharField)
#         "comment": "nice product",              (CharField)
#         "rating": 3,                      (IntegerField)
#         "_id": "642db5c2961a166dfab54076",
#         "createdAt": "2023-04-05T17:54:10.621Z", (DateTimeField ,auto_now_add)
#         "updatedAt": "2023-04-05T17:54:10.621Z"  (DateTimeField, auto_now)
#       }
#     ]
#   }



from django.db.models import Avg

# Products
class Product(models.Model):
    name = models.CharField(max_length=250)
    slug = models.CharField(max_length=250)
    image = models.FileField(upload_to="product_thumbnails")
    brand = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=200)
    price = models.IntegerField()
    countInStock = models.IntegerField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    sub_category = models.CharField(max_length=200,null=True)
    rating = models.IntegerField(default=0)
    numReviews = models.IntegerField(default=0)

    def calculate_rating(self):
        ratings = Reviews.objects.filter(product=self)
        if ratings.count() > 0:
            self.rating = ratings.aggregate(Avg('rating'))['rating__avg']
            self.numReviews = ratings.count()
        else:
            self.rating = 0
            self.numReviews = 0
        self.save()
  
# Product Images
class ProductImages(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='images')
    image = models.ImageField(upload_to="product_images/")

# Class Carousels
class Carousel(models.Model):
    carousel_image = models.ImageField(upload_to="carousel_images/")
    navigation_link = models.CharField(max_length=500,null=True)
    created_date = models.DateField(auto_now_add=True)
    created_time = models.TimeField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    updated_time = models.TimeField(auto_now=True)

#############################################################   End User Models   #####################################################################

# End User 
class EndUser(UserBaseModel):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=250)
    phone = models.CharField(max_length=200)
    gender = models.CharField(max_length=200)
    profile_pic = models.ImageField(upload_to="user_profiles/",null=True)
    otp = models.CharField(max_length=100,null=True)
    is_verified  = models.BooleanField(default=False)
    dob = models.DateField(max_length=8,null=True)
    def __str__(self):
        return self.name


# Cart Items
class CartItems(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(EndUser,on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)


# State
class State(models.Model):
    state_name = models.CharField(max_length=200)
    state_representing_image = models.ImageField(upload_to="state_images/",null=True)


# District 
class Disrtict(models.Model):
    state = models.ForeignKey(State,on_delete=models.CASCADE)
    district_name = models.CharField(max_length=200)


# Mandal
class Mandal(models.Model):
    district = models.ForeignKey(Disrtict,on_delete=models.CASCADE)
    mandal_name = models.CharField(max_length=200)


# End Users Orders
class Orders(models.Model):
    user = models.ForeignKey(EndUser,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    purchased_price = models.IntegerField()
    state = models.ForeignKey(State,on_delete=models.CASCADE)
    disrtict = models.ForeignKey(Disrtict,on_delete=models.CASCADE)
    mandal = models.ForeignKey(Mandal,on_delete=models.CASCADE)
    hno = models.CharField(max_length=200)
    street = models.CharField(max_length=200)
    colony = models.CharField(max_length=500)
    landmark = models.CharField(max_length=200,null=True)
    order_status = models.CharField(max_length=200,default="Order Placed")
    mode_of_payment = models.CharField(max_length=200)
    order_placed_date = models.DateField(auto_now_add=True)
    order_placed_time = models.TimeField(auto_now_add=True)
    order_updated_date = models.DateField(auto_now=True)
    order_updated_time = models.TimeField(auto_now=True)

    


# End User Wishlist
class Wishlist(models.Model):
    user = models.ForeignKey(EndUser,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    created_time = models.TimeField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    updated_time = models.TimeField(auto_now=True)


# Reviews
class Reviews(models.Model):
    user = models.ForeignKey(EndUser,on_delete=models.CASCADE)
    name=models.CharField(max_length=250)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="reviews")
    comment = models.TextField()
    rating = models.IntegerField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

# Reply Reviews
class ReplyReviews(models.Model):
    review = models.ForeignKey(Reviews,on_delete=models.CASCADE)
    reply_text = models.TextField()
    created_date = models.DateField(auto_now_add=True)
    created_time = models.TimeField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    updated_time = models.TimeField(auto_now=True)




 






