from django.contrib import admin
from .models import Book, Author, Category, Tag, Language, Publisher, UserProfile, Cart, CartItem, Address, Review

# Register your models here.
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Language)
admin.site.register(Publisher)
admin.site.register(UserProfile)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Address)
admin.site.register(Review)

