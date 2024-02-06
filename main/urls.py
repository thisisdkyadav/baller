from django.urls import path
from .views import UsersProfileView, BooksView, AuthorView, LanguageView, PublisherView, CategoryView, TagView, RegisterView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/users/', UsersProfileView.as_view()),
    path('api/books/', BooksView.as_view()),
    path('api/authors/', AuthorView.as_view()),
    path('api/languages/', LanguageView.as_view()),
    path('api/publishers/', PublisherView.as_view()),
    path('api/categories/', CategoryView.as_view()),
    path('api/register/', RegisterView.as_view()),
    path('api/tags/', TagView.as_view(), name='index'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
