from rest_framework import serializers
from .models import Book, Author, Category, Tag, Publisher, Language, UserProfile, Address
from django.contrib.auth.models import Group, User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(required = False)
    class Meta:
        model = Address
        fields = '__all__'

    

    def create(self , validated_data):
        print('****************',validated_data)
        user = User.objects.get(id=validated_data['user_id'])
        userprofile=UserProfile.objects.get(user=user)
        print(userprofile)
        if userprofile.address:
            address=userprofile.address
            address.pin_code = validated_data['pin_code']
            address.sub_address = validated_data['sub_address']
            address.city = validated_data['city']
            address.district = validated_data['district']
            address.state = validated_data['state']

        else:
            address = Address.objects.create(pin_code=validated_data['pin_code'], sub_address=validated_data['sub_address'], city=validated_data['city'], district=validated_data['district'], state=validated_data['state'])

        userprofile.address = address
        address.save()
        userprofile.save()
        
        return validated_data
    
    def validate_pin_code(self, pin_code):
        if not len(str(abs(pin_code))) == 6:
            raise serializers.ValidationError('Pin code must be 6 digits')
        return pin_code
    
    

    def get_fields(self, *args, **kwargs):
        fields = super(AddressSerializer, self).get_fields(*args, **kwargs)
        request = self.context.get('request', None)
        if request and request.method == 'POST':
            fields['user_id'].required = True
        return fields


class BookSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(many=True, queryset= Author.objects.all())
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset= Tag.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset= Category.objects.all())
    language = serializers.PrimaryKeyRelatedField(queryset= Language.objects.all())
    publisher = serializers.PrimaryKeyRelatedField(queryset= Publisher.objects.all())

    class Meta:
        model = Book
        fields = '__all__'


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['usrname'] = user.username
        # ...

        return token


class UserProfileSerializer(serializers.Serializer):
    user_id = serializers.CharField(required = True)
    
    address = serializers.PrimaryKeyRelatedField(queryset=Address.objects.all(), required = False)
    wishlist = serializers.PrimaryKeyRelatedField(many=True, queryset=Book.objects.all())
    favorite_authors = serializers.PrimaryKeyRelatedField(many=True, queryset=Author.objects.all())
    favorite_categories = serializers.PrimaryKeyRelatedField(many=True, queryset=Category.objects.all())
    favorite_tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())

    class Meta:
        model = UserProfile
        fields = '__all__'


    def create(self , validated_data):
        user = User.objects.get(id=validated_data['user_id'])
        userprofile=UserProfile.objects.get(user=user)
        print(userprofile)
        if 'address' in validated_data:
            address = Address.objects.create() if not userprofile.address else userprofile.address

        return validated_data


    def validate(self, data):

        return data


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    email = serializers.EmailField(required = True)
    first_name = serializers.CharField(required = True)
    last_name = serializers.CharField(required = True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'password2']

    def create(self, validated_data):
        user=User.objects.create_user(validated_data['username'].lower(), validated_data['email'].lower(), validated_data['password'], first_name=validated_data['first_name'], last_name=validated_data['last_name'])
        userprofile = UserProfile.objects.create(user=user)
        userprofile.save()

        return validated_data
    
    def validate_email(self, email):
        email = email.lower()
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('email is already used')

        return email
    
    def validate_username(self, username):
        allowed_charahteres = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9','.']

        if (not (i in allowed_charahteres for i in username)):
            raise serializers.ValidationError('Username can only contain a-z 0-9 and .')
        
        username=username.lower()
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('Username is taken')
        
        return username
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password':'Password must match'})
        return data