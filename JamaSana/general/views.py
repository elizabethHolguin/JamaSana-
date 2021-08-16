from django.shortcuts import render
from rest_framework import viewsets, permissions

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
    HTTP_200_OK,
    HTTP_403_FORBIDDEN
)

from .utils import * 

from .models import Configuracion
from .models import Perfil
from .models import PerfilE
from .models import PerfilParametrizado
from .models import CategoriasPerfilParametrizado

from productos.models import Categoria

from .serializers import ConfiguracionSerializer
from .serializers import PerfilSerializer
from .serializers import PerfilESerializer
from .serializers import PerfilParametrizadoSerializer
from .serializers import CategoriasPerfilParametrizadoSerializer
# Create your views here.

class ConfiguracionViewSet(viewsets.ModelViewSet):
    queryset = Configuracion.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ConfiguracionSerializer

class PerfilViewSet(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = PerfilSerializer

class PerfilEViewSet(viewsets.ModelViewSet):
    queryset = PerfilE.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = PerfilESerializer

class PerfilParametrizadoViewSet(viewsets.ModelViewSet):
    queryset = PerfilParametrizado.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = PerfilParametrizadoSerializer

class CategoriasPerfilParametrizadoViewSet(viewsets.ModelViewSet):
    queryset = CategoriasPerfilParametrizado.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = CategoriasPerfilParametrizadoSerializer

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def configuracionAll(request):
    data = Configuracion.objects.all()
    serializer = ConfiguracionSerializer(data, many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)


@api_view(['GET','POST','PUT','DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication,TokenAuthentication])
@permission_classes([AllowAny])
def configuracion(request, pk):

    if(request.method=='GET'):
        data = generics.get_object_or_404(Configuracion,id=pk)
        if data is not None:
            serializer = ConfiguracionSerializer(data, many=False)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({'message': 'Configuracion no existe'},status=status.HTTP_400_BAD_REQUEST)

    elif(request.method=='POST' and request.user.is_authenticated):
        serializer = ConfiguracionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)  

    elif(request.method=='PUT' and request.user.is_authenticated):
        data = generics.get_object_or_404(Configuracion,id=pk)
        if data is not None:
            serializer = ConfiguracionSerializer(data, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Configuracion no existe'},status=status.HTTP_400_BAD_REQUEST)

    elif(request.method=='DELETE' and request.user.is_authenticated):
        data = generics.get_object_or_404(Configuracion,id=pk)
        if data is not None:
            data.delete()
            msg={
                'message':'Configuracion eliminado exitosamente'
            }
            return Response(msg,status=status.HTTP_200_OK)
        return Response({'message': 'Configuracion no existe'},status=status.HTTP_400_BAD_REQUEST)

    else:
        msg={
            'error':'Permission Denied!'
        }
        return Response(msg,status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def perfilAll(request):
    data = Perfil.objects.all()
    serializer = PerfilSerializer(data, many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)


@api_view(['GET','POST','PUT','DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication,TokenAuthentication])
@permission_classes([AllowAny])
def perfil(request, pk):

    if(request.method=='GET'):
        data = generics.get_object_or_404(Perfil,id=pk)
        if data is not None:
            serializer = PerfilSerializer(data, many=False)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({'message': 'Perfil no existe'},status=status.HTTP_400_BAD_REQUEST)

    elif(request.method=='POST' and request.user.is_authenticated):
        serializer = PerfilSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)  

    elif(request.method=='PUT' and request.user.is_authenticated):
        data = generics.get_object_or_404(Perfil,id=pk)
        if data is not None:
            serializer = PerfilSerializer(data, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Perfil no existe'},status=status.HTTP_400_BAD_REQUEST)

    elif(request.method=='DELETE' and request.user.is_authenticated):
        data = generics.get_object_or_404(Perfil,id=pk)
        if data is not None:
            data.delete()
            msg={
                'message':'Perfil eliminado exitosamente'
            }
            return Response(msg,status=status.HTTP_200_OK)
        return Response({'message': 'Perfil no existe'},status=status.HTTP_400_BAD_REQUEST)

    else:
        msg={
            'error':'Permission Denied!'
        }
        return Response(msg,status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def perfilEAll(request):
    data = PerfilE.objects.all()
    serializer = PerfilESerializer(data, many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def perfilParametrizadoAll(request):
    data = PerfilParametrizado.objects.all()
    serializer = PerfilParametrizadoSerializer(data, many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)


@api_view(['GET','POST','PUT','DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication,TokenAuthentication])
@permission_classes([AllowAny])
def perfilParametrizado(request, pk):

    if(request.method=='GET'):
        data = generics.get_object_or_404(PerfilParametrizado,id=pk)
        if data is not None:
            serializer = PerfilParametrizadoSerializer(data, many=False)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({'message': 'Perfil no existe'},status=status.HTTP_400_BAD_REQUEST)

    elif(request.method=='POST' and request.user.is_authenticated):
        serializer = PerfilParametrizadoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)  

    elif(request.method=='PUT' and request.user.is_authenticated):
        data = generics.get_object_or_404(PerfilParametrizado,id=pk)
        if data is not None:
            serializer = PerfilParametrizadoSerializer(data, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Perfil no existe'},status=status.HTTP_400_BAD_REQUEST)

    elif(request.method=='DELETE' and request.user.is_authenticated):
        data = generics.get_object_or_404(PerfilParametrizado,id=pk)
        if data is not None:
            data.delete()
            msg={
                'message':'Perfil eliminado exitosamente'
            }
            return Response(msg,status=status.HTTP_200_OK)
        return Response({'message': 'Perfil no existe'},status=status.HTTP_400_BAD_REQUEST)

    else:
        msg={
            'error':'Permission Denied!'
        }
        return Response(msg,status=status.HTTP_403_FORBIDDEN)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication,TokenAuthentication])
@permission_classes([AllowAny])
def create_categorias(request,pk):

    if(request.method=='POST' and request.user.is_authenticated):
        categorias = request.data.get("categorias")
        if categorias is not None:
            x = 0
            perfilPP = generics.get_object_or_404(PerfilParametrizado,id=pk)
            categoriasPP = Categoria.objects.filter(pk__in=categorias)
            if len(categoriasPP) == 0:
                return Response({'message': 'No se encontro ninguna categoria'},status=status.HTTP_404_NOT_FOUND)
            for categoria in categoriasPP:
                
                resultado = CategoriasPerfilParametrizado().create(perfil_parametrizado=perfilPP,categoria=categoria)
                
                if resultado is not None:
                    x += 1
            if (len(categoriasPP) - x) != 0:
                return Response({'message': 'Hubieron categorias que no pudieron ser creadas'},status=status.HTTP_400_BAD_REQUEST)
            return Response({'message': 'Categorias anexadas al perfil parametrizado'},status=status.HTTP_200_OK)
        return Response({'message': 'No se ha enviado lista de categorias'},status=status.HTTP_400_BAD_REQUEST)
            
        
    msg={
        'error':'Permission Denied!'
    }
    return Response(msg,status=status.HTTP_403_FORBIDDEN)


@api_view(['GET','POST','DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication,TokenAuthentication])
@permission_classes([AllowAny])
def categoriasPP(request,pk):

    if(request.method=='GET' and request.user.is_authenticated):
        perfil = generics.get_object_or_404(PerfilParametrizado,id=pk)
        registros = CategoriasPerfilParametrizado.objects.filter(perfil_parametrizado=perfil)

        if  len(registros) == 0:
            return Response({'message': 'No hay categorias anexadas a este perfil'},status=status.HTTP_404_NOT_FOUND)

        respuesta = []

        for registro in registros:
            respuesta.append({'id': registro.categoria.pk, 'nombre': registro.categoria.nombre })

        data = {
            'categorias': respuesta
        }

        return Response(data,status=status.HTTP_200_OK)

    elif(request.method=='POST' and request.user.is_authenticated):
        categoria = request.data.get("categoria")
        if categoria is not None:
            x = 0
            perfilPP = generics.get_object_or_404(PerfilParametrizado,id=pk)
            categoriaPP = generics.get_object_or_404(Categoria,id=categoria)
            if categoriaPP is not None:
                resultado = CategoriasPerfilParametrizado().create(perfil_parametrizado=perfilPP,categoria=categoriaPP)
                if resultado is None:
                    return Response({'message': 'No se pudo anexar la categoria con el perfil'},status=status.HTTP_400_BAD_REQUEST)
                return Response({'message': 'Categoria pudo ser anexada al perfil'},status=status.HTTP_200_OK)
            return Response({'message': 'Categoria enviada no existe en la base de datos'},status=status.HTTP_404_NOT_FOUND)
                
        return Response({'message': 'No se ha enviado categoria a anexar al perfil'},status=status.HTTP_400_BAD_REQUEST)

    elif(request.method=='DELETE' and request.user.is_authenticated):
        data = generics.get_object_or_404(CategoriasPerfilParametrizado,id=pk)
        if data is not None:
            data.delete()
            msg={
                'message':'Categoria eliminado exitosamente'
            }
            return Response(msg,status=status.HTTP_200_OK)
        return Response({'message': 'Categoria no existe'},status=status.HTTP_400_BAD_REQUEST)        
        
    msg={
        'error':'Permission Denied!'
    }
    return Response(msg,status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication,TokenAuthentication])
@permission_classes([AllowAny])
def get_categorias_perfil(request):

    if(request.method=='GET' and request.user.is_authenticated):
        peso_enviado=request.data.get("peso")
        altura_enviada=request.data.get("altura")
        imc_enviado=request.data.get("imc")

        perfiles = PerfilParametrizado.objects.all()

        controlador = 0

        if len(perfiles) == 0:
            return Response({'message': 'No hay perfiles para mostrar'},status=status.HTTP_404_NOT_FOUND)
            
        listado_resultante = search_in_pesos(perfiles, peso_enviado)

        if len(listado_resultante) == 0:
            listado_resultante = perfiles
            controlador += 1

        temp = listado_resultante

        listado_resultante = search_in_altura(listado_resultante, altura_enviada)

        if len(listado_resultante) == 0:
            listado_resultante = temp
            controlador += 1

        listado_resultante = search_in_imc(listado_resultante, imc_enviado)

        if len(listado_resultante) == 0:
            listado_resultante = temp
            controlador += 1

        if controlador == 3:
            return Response({'message': 'No existe un perfil que se ajuste a su informacion'},status=status.HTTP_404_NOT_FOUND)

        perfil_seleccionado = listado_resultante[0]

        categorias = CategoriasPerfilParametrizado.objects.filter(perfil_parametrizado=perfil_seleccionado.pk)

        categorias_obtenidas = []

        for categoria in categorias:
            categorias_obtenidas.append(categoria.pk)

        data = {
            'categorias': categorias_obtenidas
        }

        return Response(data,status=status.HTTP_200_OK)

    msg={
        'error':'Permission Denied!'
    }
    return Response(msg,status=status.HTTP_403_FORBIDDEN)


