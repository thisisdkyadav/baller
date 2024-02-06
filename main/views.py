from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Book, Author, Category, Tag, Language, Publisher, UserProfile
from .serializers import UserProfileSerializer, BookSerializer, CategorySerializer, TagSerializer, LanguageSerializer,AuthorSerializer, PublisherSerializer, RegisterSerializer


class RegisterView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Data received', 'data': serializer.data})
        
        return Response({'message': 'No data received' , 'error': serializer.errors})

class BooksView(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [permissions.IsAdminUser]
    serializer_class = BookSerializer

    def get(self, request):
        """
        Return a list of all books.
        """
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        data = request.data
        serializer = BookSerializer(data=data)
        if serializer.is_valid():
            print(serializer.data)
            serializer.save()
            return Response({'message': 'Data received', 'data': serializer.data})
        
        return Response({'message': 'No data received' , 'error': serializer.errors})

class AuthorView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AuthorSerializer

    def get(self, request):
        """
        Return a list of all Author
        """
        author = Author.objects.all()
        serializer = AuthorSerializer(author, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        data = request.data
        serializer = AuthorSerializer(data=data)
        if serializer.is_valid():
            print(serializer.validated_data)
            serializer.save()
            return Response({'message': 'Data received', 'data': serializer.data})
        
        return Response({'message': 'No data received' , 'error': serializer.errors})

class LanguageView(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [permissions.IsAdminUser]
    serializer_class = LanguageSerializer

    def get(self, request):
        """
        Return a list of all Language
        """
        language = Language.objects.all()
        serializer = LanguageSerializer(language, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        data = request.data
        serializer = LanguageSerializer(data=data)
        if serializer.is_valid():
            print(serializer.validated_data)
            serializer.save()
            return Response({'message': 'Data received', 'data': serializer.data})
        
        return Response({'message': 'No data received' , 'error': serializer.errors})

class CategoryView(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [permissions.IsAdminUser]
    serializer_class = CategorySerializer

    def get(self, request):
        """
        Return a list of all Category
        """
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        data = request.data
        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            print(serializer.validated_data)
            serializer.save()
            return Response({'message': 'Data received', 'data': serializer.data})
        
        return Response({'message': 'No data received' , 'error': serializer.errors})

class TagView(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [permissions.IsAdminUser]
    serializer_class = TagSerializer

    def get(self, request):
        """
        Return a list of all Tag
        """
        tag = Tag.objects.all()
        serializer = TagSerializer(tag, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        data = request.data
        serializer = TagSerializer(data=data)
        if serializer.is_valid():
            print(serializer.validated_data)
            serializer.save()
            return Response({'message': 'Data received', 'data': serializer.data})
        
        return Response({'message': 'No data received' , 'error': serializer.errors})

class PublisherView(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [permissions.IsAdminUser]
    serializer_class = PublisherSerializer

    def get(self, request):
        """
        Return a list of all Publisher
        """
        publisher = Publisher.objects.all()
        serializer = PublisherSerializer(publisher, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        data = request.data
        serializer = PublisherSerializer(data=data)
        if serializer.is_valid():
            print(serializer.validated_data)
            serializer.save()
            return Response({'message': 'Data received', 'data': serializer.data})
        
        return Response({'message': 'No data received' , 'error': serializer.errors})

class UsersProfileView(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [permissions.IsAdminUser]
    serializer_class = UserProfileSerializer


    def get(self, request):
        profiles = UserProfile.objects.all()
        serializer = UserProfileSerializer(profiles, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        data = request.data
        # data['user'] = User.objects.filter(username=data['user'])
        # print(data['user'])
        serializer = UserProfileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Data received', 'data': serializer.data})
        
        return Response({'message': 'No data received' , 'error': serializer.errors})