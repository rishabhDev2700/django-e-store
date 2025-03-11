from operator import index
import os
from uuid import uuid4
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager
from accounts.models import User


# Category Model
class Category(models.Model):
    cover = models.ImageField(upload_to="covers/")
    name = models.CharField(max_length=80)
    description = models.TextField()
    slug = models.SlugField(blank=False, unique=True, max_length=30)
    objects = models.Manager()

    class Meta:
        verbose_name_plural = "Categories"
        indexes = [
            models.Index(fields=["slug"], name="category_slug_index"),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("store:show-category", args=[self.slug])


# Helper function to set the upload path for product images
def path_and_rename(instance, filename):
    upload_to = "products/"
    ext = filename.split(".")[-1]
    if instance.pk:
        filename = "{}.{}".format(instance.pk, ext)
    else:
        filename = "{}.{}".format(uuid4().hex, ext)
    return os.path.join(upload_to, filename)


# Product Model
class Product(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    slug = models.SlugField(blank=False, unique=True, max_length=30)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    is_free = models.BooleanField(default=False)  # New field to mark free products
    date_added = models.DateField(auto_now=True)
    is_available = models.BooleanField(default=True)
    cover = models.ImageField(upload_to=path_and_rename, null=True)
    thumbnail = models.ImageField(upload_to=path_and_rename, null=True)
    tags = TaggableManager()
    objects = models.Manager()

    class Meta:
        ordering = ["-date_added"]
        indexes = [
            models.Index(fields=["slug"], name="product_slug_index"),
            models.Index(fields=["category"], name="product_categories_index"),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("store:show-product", args=[self.slug])

    @property
    def effective_price(self):
        """
        Returns 0 if the product is free, otherwise its price.
        """
        return 0 if self.is_free else self.price


# ProductImage Model
class ProductImage(models.Model):
    name = models.CharField(max_length=40)
    image = models.ImageField(upload_to="media/")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    objects = models.Manager()

    def __str__(self):
        return self.name


# Discount Model
class Discount(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    percentage = models.FloatField()
    name = models.CharField(max_length=20, unique=True)
    valid_till = models.DateField()
    objects = models.Manager()


# Order Model
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    total = models.PositiveIntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return f"Order by: {self.user} created on: {self.created_on} total: {self.total} completed: {self.is_completed}"

    class Meta:
        ordering = ["-created_on"]


# OrderProduct Model
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    price = models.PositiveIntegerField()
    objects = models.Manager()

    def __str__(self):
        return f"Item: {self.product.name} quantity: {self.quantity}"

    class Meta:
        indexes = [
            models.Index(fields=["order", "product"], name="order_product_index"),
        ]


# Rating Model
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.SmallIntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(0)]
    )
    review = models.TextField()
    objects = models.Manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "product"], name="unique_rating")
        ]
        indexes = [
            models.Index(fields=["product"], name="product_rating_index"),
        ]


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ("RAZORPAY", "Razorpay"),
        ("STRIPE", "Stripe"),
        ("PAYPAL", "PayPal"),
        # add additional processors as needed
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payments")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    transaction_id = models.CharField(max_length=100, unique=True)
    amount = models.PositiveIntegerField()
    currency = models.CharField(max_length=10, default="USD")
    status = models.CharField(
        max_length=20, default="PENDING"
    )  # e.g. PENDING, COMPLETED, FAILED
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.payment_method} - {self.transaction_id}"

    class Meta:
        indexes = [
            models.Index(fields=["order"], name="payment_order_index"),
        ]
