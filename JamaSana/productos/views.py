from usuarios.models import Cliente
from django.shortcuts import render
from rest_framework import viewsets, permissions

from .models import Categoria
from .models import Comidas
from .models import Pedido
from .models import DetallePedido

from .serializers import CategoriaSerializer
from .serializers import ComidasSerializer
from .serializers import PedidoSerializer
from .serializers import DetallePedidoSerializer

from django.http import JsonResponse
from rest_framework.response import Response

from rest_framework import status
from rest_framework import generics

from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
# Create your views here.

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = CategoriaSerializer

class ComidasViewSet(viewsets.ModelViewSet):
    queryset = Comidas.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ComidasSerializer


class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = PedidoSerializer

class DetallePedidoViewSet(viewsets.ModelViewSet):
    queryset = DetallePedido.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = DetallePedidoSerializer


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def categorias(request):
    data = Categoria.objects.all()
    serializer = CategoriaSerializer(data, many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)


@api_view(['GET','POST','PUT','DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication,TokenAuthentication])
@permission_classes([AllowAny])
def categoria(request, pk):

    if(request.method=='GET'):
        data = generics.get_object_or_404(Categoria,id=pk)
        if data is not None:
            serializer = CategoriaSerializer(data, many=False)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({'message': 'Categoría no existe'},status=status.HTTP_400_BAD_REQUEST)

    elif(request.method=='POST' and request.user.is_authenticated):
        serializer = CategoriaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)  

    elif(request.method=='PUT' and request.user.is_authenticated):
        data = generics.get_object_or_404(Categoria,id=pk)
        if data is not None:
            serializer = CategoriaSerializer(data, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Categoría no existe'},status=status.HTTP_400_BAD_REQUEST)

    elif(request.method=='DELETE' and request.user.is_authenticated):
        data = generics.get_object_or_404(Categoria,id=pk)
        if data is not None:
            data.delete()
            msg={
                'message':'Categoría eliminado exitosamente'
            }
            return Response(msg,status=status.HTTP_200_OK)
        return Response({'message': 'Categoría no existe'},status=status.HTTP_400_BAD_REQUEST)

    else:
        msg={
            'error':'Permission Denied!'
        }
        return Response(msg,status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def comidasAll(request):
    data = Comidas.objects.all()
    serializer = ComidasSerializer(data, many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)


@api_view(['GET','POST','PUT','DELETE', 'PATCH'])
@authentication_classes([SessionAuthentication, BasicAuthentication,TokenAuthentication])
@permission_classes([AllowAny])
def comida(request, pk):

    if(request.method=='GET'):
        data = generics.get_object_or_404(Comidas,id=pk)
        if data is not None:
            serializer = ComidasSerializer(data, many=False)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({'message': 'Comida no existe'},status=status.HTTP_400_BAD_REQUEST)

    elif(request.method=='POST' and request.user.is_authenticated):
        serializer = ComidasSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)  

    elif(request.method=='PUT' and request.user.is_authenticated):
        data = generics.get_object_or_404(Comidas,id=pk)
        if data is not None:
            serializer = ComidasSerializer(data, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Comida no existe'},status=status.HTTP_400_BAD_REQUEST)

    elif(request.method=='DELETE' and request.user.is_authenticated):
        data = generics.get_object_or_404(Comidas,id=pk)
        if data is not None:
            data.delete()
            msg={
                'message':'Comida eliminado exitosamente'
            }
            return Response(msg,status=status.HTTP_200_OK)
        return Response({'message': 'Comida no existe'},status=status.HTTP_400_BAD_REQUEST)

    else:
        msg={
            'error':'Permission Denied!'
        }
        return Response(msg,status=status.HTTP_403_FORBIDDEN)
    

@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication,TokenAuthentication])
@permission_classes([AllowAny])
def obtener_comidas(request,pk):

    if(request.method=='POST' and request.user.is_authenticated):
        categorias = request.data.get("categorias")
        if categorias is not None:
            comidas = Comidas.objects.filter(id_categoria__in=categorias)
            if len(comidas) == 0:
                return Response({'message': 'No se encontro ninguna comida anexada a las categorias enviadas'},status=status.HTTP_404_NOT_FOUND)
            serializer = ComidasSerializer(comidas, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)          
        return Response({'message': 'No se ha enviado lista de categorias'},status=status.HTTP_400_BAD_REQUEST)
     
    msg={
        'error':'Permission Denied!'
    }
    return Response(msg,status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def pedidosAll(request):
    data = Pedido.objects.all()
    serializer = PedidoSerializer(data, many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def pedidosCliente(request,pk):

    if(request.method=='GET' and request.user.is_authenticated):
        usuario = generics.get_object_or_404(Cliente,id=pk)
        data = Pedido.objects.filter(id_cliente=usuario)
        serializer = PedidoSerializer(data, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    msg={
        'error':'Permission Denied!'
    }
    return Response(msg,status=status.HTTP_403_FORBIDDEN)


@api_view(['GET','POST','PUT','DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication,TokenAuthentication])
@permission_classes([AllowAny])
def pedido(request, pk):

    if(request.method=='GET'):
        data = generics.get_object_or_404(Pedido,id=pk)
        if data is not None:
            serializer = PedidoSerializer(data, many=False)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({'message': 'Pedido no existe'},status=status.HTTP_400_BAD_REQUEST)

    elif(request.method=='POST' and request.user.is_authenticated):
        serializer = PedidoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)  

    elif(request.method=='PUT' and request.user.is_authenticated):
        data = generics.get_object_or_404(Pedido,id=pk)
        if data is not None:
            serializer = PedidoSerializer(data, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Pedido no existe'},status=status.HTTP_400_BAD_REQUEST)

    elif(request.method=='DELETE' and request.user.is_authenticated):
        data = generics.get_object_or_404(Pedido,id=pk)
        if data is not None:
            data.delete()
            msg={
                'message':'Pedido eliminado exitosamente'
            }
            return Response(msg,status=status.HTTP_200_OK)
        return Response({'message': 'Pedido no existe'},status=status.HTTP_400_BAD_REQUEST)

    else:
        msg={
            'error':'Permission Denied!'
        }
        return Response(msg,status=status.HTTP_403_FORBIDDEN)

@api_view(['GET','POST','PUT','DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication,TokenAuthentication])
@permission_classes([AllowAny])
def detalle_pedido(request, pk):

    if(request.method=='GET'):
        pedido = generics.get_object_or_404(Pedido,id=pk)
        data = generics.get_object_or_404(DetallePedido,id_pedido=pedido)
        if data is not None:
            serializer = DetallePedidoSerializer(data, many=False)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({'message': 'Pedido no existe'},status=status.HTTP_400_BAD_REQUEST)

    elif(request.method=='POST' and request.user.is_authenticated):
        serializer = DetallePedidoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)  

    elif(request.method=='PUT' and request.user.is_authenticated):
        data = generics.get_object_or_404(DetallePedido,id=pk)
        if data is not None:
            serializer = DetallePedidoSerializer(data, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Pedido no existe'},status=status.HTTP_400_BAD_REQUEST)

    elif(request.method=='DELETE' and request.user.is_authenticated):
        data = generics.get_object_or_404(DetallePedido,id=pk)
        if data is not None:
            data.delete()
            msg={
                'message':'Pedido eliminado exitosamente'
            }
            return Response(msg,status=status.HTTP_200_OK)
        return Response({'message': 'Pedido no existe'},status=status.HTTP_400_BAD_REQUEST)

    else:
        msg={
            'error':'Permission Denied!'
        }
        return Response(msg,status=status.HTTP_403_FORBIDDEN)
