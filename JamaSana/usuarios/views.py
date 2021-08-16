from django.shortcuts import render
from rest_framework import viewsets, permissions

from .models import Cliente
from .models import Administrador
from .models import Vendedor
from seguridad.models import Tarjeta

from .serializers import ClienteSerializer
from .serializers import AdministradorSerializer
from .serializers import VendedorSerializer
from .serializers import UserSerializer

from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework import generics

from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from django.contrib.auth import authenticate, login
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Create your views here.

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ClienteSerializer

class AdministradorViewSet(viewsets.ModelViewSet):
    queryset = Administrador.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = AdministradorSerializer


class VendedorViewSet(viewsets.ModelViewSet):
    queryset = Vendedor.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = VendedorSerializer

##Funciones de Login

#Get if User have active Token
#Unique Token for User
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def isActiveToken(request,user):
    active=Token.objects.filter(user=user).exists()
    data = {'active': active}
    return Response(data, status=status.HTTP_200_OK)



@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def login(request):
    serializer = ObtainAuthToken.serializer_class(
        data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    
    try:    
        cliente = Cliente.objects.get(user=user)
        token, created = Token.objects.get_or_create(user=user) 
        data = {
            "id": cliente.id,
            "first_name": cliente.user.first_name,
            "last_name": cliente.user.last_name,
            "username": cliente.user.username,
            "email": cliente.user.email,
            "direccion": cliente.direccion,
            "fecha_nacimiento": cliente.fecha_nacimiento,
            'Auth-token': token.key,
        }
        return Response(data, status=HTTP_200_OK)
    except:
        return Response({'error': 'User not authorized'}, status=HTTP_404_NOT_FOUND)
    
    

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def login_admin(request):
    
    serializer = ObtainAuthToken.serializer_class(
        data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']

    try:
        admin = Administrador.objects.get(user=user)
        token, created = Token.objects.get_or_create(user=user)
        data = {
            "id": admin.id,
            "nombre": admin.user.first_name,
            "apellido": admin.user.last_name,
            "username": admin.user.username,
            "email": admin.user.email,
            'Auth-token': token.key,
        }
        return Response(data, status=HTTP_200_OK)
    except:
        return Response({'error': 'User not authorized'}, status=HTTP_404_NOT_FOUND)


    

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def login_vendedor(request):
    
    serializer = ObtainAuthToken.serializer_class(
        data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']

    try:
        vendedor = Vendedor.objects.get(user=user)
        token, created = Token.objects.get_or_create(user=user)
        data = {
            "id": vendedor.id,
            "nombre": vendedor.user.first_name,
            "apellido": vendedor.user.last_name,
            "username": vendedor.user.username,
            "email": vendedor.user.email,
            'Auth-token': token.key,
        }
        return Response(data, status=HTTP_200_OK)
    except:
        return Response({'error': 'User not authorized'}, status=HTTP_404_NOT_FOUND)
        

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication,TokenAuthentication])
@permission_classes([AllowAny])
def vendedorAll(request):
    if request.user.is_authenticated:
        data = Vendedor.objects.all()
        lista = []
        for vendedor in data:
            user = {}
            dataUser = User.objects.get(id=int(vendedor.user.id))
            user['id'] = vendedor.pk
            user['id_user'] = dataUser.id
            user['username'] = dataUser.username
            user['first_name'] = dataUser.first_name
            user['last_name'] = dataUser.last_name
            user['email'] = dataUser.email
            lista.append(user)
        return Response(lista,status=status.HTTP_200_OK)
    msg={
            'error':'Permission Denied!'
        }
    return Response(msg,status=status.HTTP_403_FORBIDDEN)

@api_view(['GET','PUT','DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication,TokenAuthentication])
@permission_classes([AllowAny])
def vendedor(request, pk):
    print(request.method)

    if(request.method=='GET' and request.user.is_authenticated):
        data = generics.get_object_or_404(Vendedor,id=pk)
        if data is not None:
            user = {}
            user['id'] = pk
            user['id_user'] = data.user.id
            user['username'] = data.user.username
            user['first_name'] = data.user.first_name
            user['last_name']= data.user.last_name
            user['email'] = data.user.email
            return Response(user,status=status.HTTP_200_OK)
        return Response({'message': 'Vendedor no existe'},status=status.HTTP_400_BAD_REQUEST) 

    elif(request.method=='PUT' and request.user.is_authenticated):
        data = generics.get_object_or_404(Vendedor,id=pk)
        if data is not None:
            id_user= request.data.get("id_user")
            username = request.data.get("username")
            first_name = request.data.get("first_name")
            last_name = request.data.get("last_name")
            email = request.data.get("email")

            if username is not None:
                data.user.username = username
            if first_name is not None:
                 data.user.first_name = first_name
            if last_name is not None:
                 data.user.last_name = last_name
            if email is not None:
                 data.user.email = email
            user = {}
            data.user.save()
            user['id']=pk
            user['id_user']= data.user.id
            user['username'] = data.user.username
            user['first_name'] = data.user.first_name
            user['last_name']= data.user.last_name
            user['email'] = data.user.email

            return Response(user,status=status.HTTP_200_OK)
        return Response({'message': 'Vendedor no existe'},status=status.HTTP_400_BAD_REQUEST)

    elif(request.method=='DELETE' and request.user.is_authenticated):
        data = generics.get_object_or_404(Vendedor,id=pk)
        if data is not None:
            data.user.delete()
            data.delete()
            msg={
                'message':'Vendedor eliminado exitosamente'
            }
            return Response(msg,status=status.HTTP_200_OK)
        return Response({'message': 'Vendedor no existe'},status=status.HTTP_400_BAD_REQUEST)

    else:
        msg={
            'error':'Permission Denied!'
        }
        return Response(msg,status=status.HTTP_403_FORBIDDEN)


##Funciones Para Registro de Usuarios
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def registrar(request):
    
    username = request.data.get("username")
    userExists=User.objects.filter(username=username).exists()
    if(userExists):
        msg={
            'error':"User already exists."
        }
        return Response(msg,status=status.HTTP_400_BAD_REQUEST)
    
    email = request.data.get("email")
    emailExists=User.objects.filter(email=email).exists()
    if(emailExists):
        msg={
            'error':"Email already exists."
        }
        return Response(msg,status=status.HTTP_400_BAD_REQUEST)
    
    password = make_password(request.data.get("password"))

    first_name = request.data.get("first_name")
    last_name = request.data.get("last_name")

    data = {
        "username": username,
        "email": email,
        "password": password,
        "first_name": first_name,
        "last_name": last_name
    }

    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        try:
            direccion = request.data.get("direccion")
            fecha_nacimiento = request.data.get("fecha_nacimiento")
            user = User.objects.get(username=username)
            tarjeta = Tarjeta.objects.get(pk=1)
            cliente = Cliente().crearCliente(user,direccion,fecha_nacimiento)
            if cliente is not None:
                data2 = {
                    "id": cliente.id,
                    "username": username,
                    "email": email,
                    "first_name": first_name,
                    "last_name": last_name
                }
                return Response(data2, status=status.HTTP_201_CREATED)
            else:
                msg={
                    'error':"Error creating user cliente in database"
                }
                return Response(msg,status=status.HTTP_400_BAD_REQUEST)
        except:
            msg={
                'error':"Error creating user cliente because of tarjeta or cliente"
            }
            return Response(msg,status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication,TokenAuthentication])
@permission_classes([AllowAny])
def registrar_vendedor(request):

    if request.user.is_authenticated:
        username = request.data.get("username")
        userExists=User.objects.filter(username=username).exists()
        if(userExists):
            msg={
                'error':"User already exists."
            }
            return Response(msg,status=status.HTTP_400_BAD_REQUEST)
        
        email = request.data.get("email")
        emailExists=User.objects.filter(email=email).exists()
        if(emailExists):
            msg={
                'error':"Email already exists."
            }
            return Response(msg,status=status.HTTP_400_BAD_REQUEST)
        
        password = make_password(request.data.get("password"))

        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")

        data = {
            "username": username,
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name
        }

        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            try:
                user = User.objects.get(username=username)
                vendedor = Vendedor().crearVendedor(user)
                if vendedor is not None:
                    data2 = {
                        "username": username,
                        "email": email,
                        "first_name": first_name,
                        "last_name": last_name
                    }
                    return Response(data2, status=status.HTTP_201_CREATED)
                else:
                    msg={
                        'error':"Error creating user vendedor in database"
                    }
                    return Response(msg,status=status.HTTP_400_BAD_REQUEST)
            except:
                msg={
                    'error':"Error creating user vendedor because of user account"
                }
                return Response(msg,status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    msg={
            'error':'Permission Denied!'
        }
    return Response(msg,status=status.HTTP_403_FORBIDDEN)



@api_view(['GET','PUT','DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication,TokenAuthentication])
@permission_classes([AllowAny])
def cliente(request, pk):
    print(request.method)

    if(request.method=='GET' and request.user.is_authenticated):
        data = generics.get_object_or_404(Cliente,id=pk)
        if data is not None:
            serializer = ClienteSerializer(data, many=False)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({'message': 'Cliente no existe'},status=status.HTTP_400_BAD_REQUEST) 

    elif(request.method=='PUT' and request.user.is_authenticated):
        data = generics.get_object_or_404(Cliente,id=pk)
        if data is not None:
            id_user= request.data.get("id_user")
            username = request.data.get("username")
            first_name = request.data.get("first_name")
            last_name = request.data.get("last_name")
            email = request.data.get("email")
            direccion= request.data.get("direccion")
            fecha_nacimiento=request.data.get("fecha_nacimiento")

            if username is not None:
                data.user.username = username
                # print("entre aqui")
            if first_name is not None:
                 data.user.first_name = first_name
            if last_name is not None:
                 data.user.last_name = last_name
            if email is not None:
                 data.user.email = email
            if direccion is not None:
                 data.direccion = direccion
            if fecha_nacimiento is not None:
                 data.fecha_nacimiento = fecha_nacimiento
            user = {}

            data.user.save()
            user['id']=pk
            user['id_user']= data.user.id
            user['username'] = data.user.username
            user['first_name'] = data.user.first_name
            user['last_name']= data.user.last_name
            user['email'] = data.user.email

            data.save()
            user['direccion'] = data.direccion
            user['fecha_nacimiento'] = data.fecha_nacimiento

            return Response(user,status=status.HTTP_200_OK)
        return Response({'message': 'Cliente no existe'},status=status.HTTP_400_BAD_REQUEST)

    elif(request.method=='DELETE' and request.user.is_authenticated):
        data = generics.get_object_or_404(Cliente,id=pk)
        if data is not None:
            data.user.delete()
            data.delete()
            msg={
                'message':'Cliente eliminado exitosamente'
            }
            return Response(msg,status=status.HTTP_200_OK)
        return Response({'message': 'Cliente no existe'},status=status.HTTP_400_BAD_REQUEST)

    else:
        msg={
            'error':'Permission Denied!'
        }
        return Response(msg,status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication,TokenAuthentication])
@permission_classes([AllowAny])
def clienteAll(request):
    if request.user.is_authenticated:
        data = Cliente.objects.all()
        lista = []
        for cliente in data:
            user = {}
            dataUser = User.objects.get(id=int(cliente.user.id))
            user['id'] = cliente.pk
            user['id_user'] = dataUser.id
            user['username'] = dataUser.username
            user['first_name'] = dataUser.first_name
            user['last_name'] = dataUser.last_name
            user['email'] = dataUser.email
            user['direccion'] = cliente.direccion
            user['fecha_nacimiento'] = cliente.fecha_nacimiento
            lista.append(user)
        return Response(lista,status=status.HTTP_200_OK)
    msg={
            'error':'Permission Denied!'
        }
    return Response(msg,status=status.HTTP_403_FORBIDDEN)
    




