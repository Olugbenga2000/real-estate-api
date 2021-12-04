from django.shortcuts import render
from django.http import HttpResponseRedirect
# Create your views here.
from rest_framework.views import APIView
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from rest_framework.authentication import TokenAuthentication,BasicAuthentication
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer, RegisterSerializer,LoginSerializer,PropertySerializer
from django.contrib.auth import login,logout

from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from .models import Property

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": Token.objects.create(user = user).key
        })
        

class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer
    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=200)
    
class LogoutView(APIView):
    authentication_classes = (TokenAuthentication, )
    
    def post(self, request):
        logout(request)
        return Response(status=200)
    
class PropertyView(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    