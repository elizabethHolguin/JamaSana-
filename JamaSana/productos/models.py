from django.db import models
from django.forms import ModelForm

import os
from django.dispatch import receiver

def get_upload_to_categoria(instance, filename):
    folder_name = 'categoria'
    #print(instance.hueca_id)
    return os.path.join(folder_name, filename)

def get_upload_to_comida(instance, filename):
    folder_name = 'comida'
    #print(instance.hueca_id)
    return os.path.join(folder_name, filename)

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=200)
    imagen = models.ImageField(null=True,blank=True,upload_to=get_upload_to_categoria)

    class CategoriaForm(ModelForm):
        class Meta:
            ordering = ["nombre"]
            verbose_name = "Categoria"

    def __str__(self):
        return self.nombre

@receiver(models.signals.post_delete, sender=Categoria)
def auto_delete_file_on_delete_Categoria(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.imagen:
        if os.path.isfile(instance.imagen.path):
            os.remove(instance.imagen.path)


@receiver(models.signals.pre_save, sender=Categoria)
def auto_delete_file_on_change_Categoria(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).imagen
    except sender.DoesNotExist:
        return False

    new_file = instance.imagen
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

class Comidas(models.Model):
    nombre =  models.CharField(max_length=200)
    descripcion = models.CharField(max_length=200)
    macronutrientes = models.CharField(max_length=1000)
    estado = models.BooleanField(default=True)
    precio = models.FloatField(default=0)
    calorias_totales = models.FloatField(default=0)
    imagen = models.ImageField(upload_to=get_upload_to_comida)
    id_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    id_vendedor = models.ForeignKey("usuarios.Vendedor", on_delete=models.CASCADE)

    class ComidasForm(ModelForm):
        class Meta:
            ordering = ["nombre","descripcion"]
            verbose_name = "Comidas"

    def __str__(self):
        return self.nombre + ' - ' + self.descripcion


@receiver(models.signals.post_delete, sender=Comidas)
def auto_delete_file_on_delete_Categoria(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.imagen:
        if os.path.isfile(instance.imagen.path):
            os.remove(instance.imagen.path)


@receiver(models.signals.pre_save, sender=Comidas)
def auto_delete_file_on_change_Categoria(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).imagen
    except sender.DoesNotExist:
        return False

    new_file = instance.imagen
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

class Pedido(models.Model):
    id_cliente = models.ForeignKey("usuarios.Cliente", on_delete=models.CASCADE)
    fecha_emitido = models.DateTimeField('Fecha de emisión')
    estado = models.IntegerField(default=0)
    
    
    class PedidoForm(ModelForm):    
        class Meta:
            ordering = ["id_cliente"]
            verbose_name = "Pedido"

    def __str__(self):
        return str(self.id)

class DetallePedido(models.Model):
    id_pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    fecha_emitido = models.DateTimeField('Fecha de emisión')
    id_comida = models.ForeignKey("productos.Comidas", on_delete=models.CASCADE)
    id_dias = models.ForeignKey("calendario.Dias", on_delete=models.CASCADE)
    hora_entrega = models.TimeField()
    estado_pedido = models.IntegerField(default=0)

    class DetallePedidoForm(ModelForm):
        class Meta:
            ordering = ["id_comida"]
            verbose_name = "Detalle Pedidos"
       
    def __str__(self):
        return self.id_comida


