from rest_framework import serializers
from .models import Cliente
from .models import Administrador
from .models import Vendedor

from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id','username', 'password','first_name', 'last_name', 'email')

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ('id','nombre','apellido', 'imagen','email','usuario','contraseña','direccion','fecha_nacimiento','id_tarjeta')

class AdministradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrador
        fields = ('id','user')

class VendedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendedor
        fields = ('id','user')
