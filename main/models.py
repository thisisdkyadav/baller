from django.db import models
from django.contrib.auth.models import User

# class UserProfile(User):
#     image = models.ImageField(upload_to='user_images/',default='default_profile.svg')
#     bio = models.TextField(blank=True)
#     phone = models.CharField(max_length=10)
#     address = models.ForeignKey('Address', on_delete=models.CASCADE, blank=True)
#     wishlist = models.ManyToManyField('Book', blank=True)
#     favorite_authors = models.ManyToManyField('Author', blank=True)
#     favorite_categories = models.ManyToManyField('Category', blank=True)
#     favorite_tags = models.ManyToManyField('Tag', blank=True)

#     # def getAllReviews(self):
#     #     return self.review_set.all()

#     def __str__(self):
#         return self.username


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user_images/',default='default_profile.svg')
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=10, blank=True)
    address = models.ForeignKey('Address', on_delete=models.CASCADE, blank=True,null=True)
    wishlist = models.ManyToManyField('Book', blank=True)
    favorite_authors = models.ManyToManyField('Author', blank=True)
    favorite_categories = models.ManyToManyField('Category', blank=True)
    favorite_tags = models.ManyToManyField('Tag', blank=True)

    def getAllReviews(self):
        return self.review_set.all()

    def __str__(self):
        return self.user.username
    

class Book(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='book_covers/')
    published_on = models.DateTimeField(auto_now_add=True)
    publisher = models.ForeignKey('Publisher', on_delete=models.CASCADE)
    language = models.ForeignKey('Language', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    author = models.ManyToManyField('Author')
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length = 50,primary_key=True)
    bio = models.TextField()
    image = models.ImageField(upload_to='author_images/')

    def getAllBooks(self):
        return self.book_set.all()

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def getAllBooks(self):
        return self.book_set.all()

    def __str__(self):
        return self.name
    

class Tag(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    description = models.TextField()

    def getAllBooks(self):
        return self.book_set.all()

    def __str__(self):
        return self.name
    

class Publisher(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length = 50,primary_key=True)
    description = models.TextField()
    website = models.URLField()

    def getAllBooks(self):
        return self.book_set.all()

    def __str__(self):
        return self.name
    

class Language(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def getAllBooks(self):
        return self.book_set.all()

    def __str__(self):
        return self.name


class Review(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.IntegerField()

    def __str__(self):
        return self.review
    

class Address(models.Model):
    pin_code = models.IntegerField()
    sub_address = models.TextField()
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    def getFullAddress(self):
        return f"{self.sub_address}, {self.city}, {self.district}, {self.state} - {self.pin_code}"

    def __str__(self):
        return self.sub_address

    
class CartItem(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total(self):
        return self.book.price * self.quantity
    
    def set_quantity(self, quantity):
        self.quantity = quantity
        self.save()

    def increase_quantity(self, quantity):
        self.quantity += quantity
        self.save()

    def __str__(self):
        return f"{self.quantity} x {self.book.title}"
    

class Cart(models.Model):
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    items = models.ManyToManyField('CartItem')
    total = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Cart for {self.user.username}"
    
    def get_total(self):
        total = 0
        for item in self.items.all():
            total += item.get_total()
        return total
    
    def add_item(self, book, quantity):
        try:
            item = self.items.get(book=book)
            item.increase_quantity(quantity)
        except CartItem.DoesNotExist:
            item = CartItem.objects.create(book=book, quantity=quantity)
            self.items.add(item)
        self.total = self.get_total()
        self.save()

    def remove_item(self, book):
        item = self.items.get(book=book)
        self.items.remove(item)
        self.total = self.get_total()
        self.save()

    def clear(self):
        self.items.clear()
        self.total = 0
        self.save()
        


