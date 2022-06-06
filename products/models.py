from account.models import User
from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django_countries.fields import CountryField
from django.utils.text import slugify
from ecommerce.utils import BaseModel, path_and_rename



ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)






class Category(BaseModel):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    slug = models.SlugField(unique=True, editable=False)
    image = models.ImageField(upload_to=path_and_rename)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class SubCategory(BaseModel):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True,editable=False)
    image = models.ImageField(upload_to=path_and_rename)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'SubCategory'
        verbose_name_plural = 'SubCategories'


class Item(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory,on_delete=models.CASCADE)
    slug = models.SlugField()
    description = models.TextField()
    image_thumbnail = models.ImageField(upload_to=path_and_rename)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Item, self).save(*args, **kwargs)
    # def get_absolute_url(self):
    #     return reverse("core:product", kwargs={
    #         'slug': self.slug
    #     })

    # def get_add_to_cart_url(self):
    #     return reverse("core:add-to-cart", kwargs={
    #         'slug': self.slug
    #     })

    # def get_remove_from_cart_url(self):
    #     return reverse("core:remove-from-cart", kwargs={
    #         'slug': self.slug
    #     })




class OrderItem(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    # def get_total_item_price(self):
    #     return self.quantity * self.item.price

    # def get_total_discount_item_price(self):
    #     return self.quantity * self.item.discount_price

    # def get_amount_saved(self):
    #     return self.get_total_item_price() - self.get_total_discount_item_price()

    # def get_final_price(self):
    #     if self.item.discount_price:
    #         return self.get_total_discount_item_price()
    #     return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)

    '''
    1. Item added to cart
    2. Adding a billing address
    (Failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    6. Refunds
    '''

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total


class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'


# class Payment(models.Model):
#     stripe_charge_id = models.CharField(max_length=50)
#     user = models.ForeignKey(User,on_delete=models.SET_NULL, blank=True, null=True)
#     amount = models.FloatField()
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.user.username


class Coupon(models.Model):
    code = models.CharField(max_length=15,db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    expiry_date = models.DateTimeField(blank=True,null=True)
    discount_amount = models.FloatField()

    def __str__(self):
        return self.code

