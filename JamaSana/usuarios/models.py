from django.db import models
from django.utils.dateparse import parse_date
from django.forms import ModelForm
from django.contrib.auth.models import User
# Create your models here.

import os
from django.dispatch import receiver

def get_upload_to_cliente(instance, filename):
    folder_name = 'cliente'
    #print(instance.hueca_id)
    return os.path.join(folder_name, filename)

class Cliente(models.Model):
    direccion = models.CharField(max_length=350)
    fecha_nacimiento = models.DateField()
    imagen = models.ImageField(null=True,blank=True,upload_to=get_upload_to_cliente)
    id_tarjeta = models.ForeignKey("seguridad.Tarjeta", on_delete=models.CASCADE,null=True,blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class ClienteForm(ModelForm):
        class Meta:
            # ordering = ["nombre","apellido"]
            ordering = ["user"]
            verbose_name = "Cliente"

    # def crearCliente(self,user,nombre,apellido,email,direccion,fecha_nacimiento):
    def crearCliente(self,user,direccion,fecha_nacimiento):
        try:
            cliente = Cliente()
            cliente.user = user
            cliente.direccion = direccion
            cliente.fecha_nacimiento = parse_date(fecha_nacimiento)
            cliente.id_tarjeta = None
            cliente.save()
            return cliente
        except Exception as e:
            print(str(e))
            return None


    def __str__(self):
        return self.user.first_name + ' - ' + self.user.last_name

@receiver(models.signals.post_delete, sender=Cliente)
def auto_delete_file_on_delete_Cliente(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.imagen:
        if os.path.isfile(instance.imagen.path):
            os.remove(instance.imagen.path)
    
class Administrador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class AdministradorForm(ModelForm):
        class Meta:
            ordering = ["user"]
            verbose_name = "Administrador"
  
 
    def __str__(self):
        return self.user.first_name + ' - ' + self.user.last_name

class Vendedor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class VendedorForm(ModelForm):
        class Meta:
            ordering = ["user"]
            verbose_name = "Vendedor"

    def crearVendedor(self,user):
        try:
            vendedor = Vendedor()
            vendedor.user = user
            vendedor.save()
            return vendedor
        except Exception as e:
            print(str(e))
            return None
        

    def __str__(self):
        return self.user.first_name + ' - ' + self.user.last_name
