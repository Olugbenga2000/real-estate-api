from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import exceptions
from .models import Property,Property_Image


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')
        
class Property_image_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Property_Image
        fields = ('id','images')
        
class PropertySerializer(serializers.ModelSerializer):
    media = Property_image_Serializer(many = True, required = False)
    class Meta:
        model = Property
        fields = '__all__'
        
    def create(self,validated_data):
        
        if 'media' in validated_data:
            media = validated_data.pop('media')
            prop_instance = Property.objects.create(**validated_data)
            for img in media:
                Property_Image.objects.create(**img, property = prop_instance)
            return prop_instance
        if 'media' not in validated_data:
             prop_instance = Property.objects.create(**validated_data)
             return prop_instance
        

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    def validate(self, data):
        username = data.get("username", "")
        password = data.get("password", "")
        
        if username and password:
            user = authenticate(username = username, password = password)
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    msg = "User is deactivated."
                    raise raise_exceptions.ValidationError(msg)
            else:
                msg = "Incorrect password or username."
                raise exceptions.ValidationError(msg)
        else:
            msg = "Must provide username and password both."
            raise exceptions.ValidationError(msg)
        return data
            