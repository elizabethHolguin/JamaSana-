
from django.db import models
from django.forms import ModelForm

import os
from django.dispatch import receiver

# Create your models here.
class Configuracion(models.Model):
    dolares_por_kilometros = models.FloatField()
    valor_comida = models.FloatField()
    direccion_fija = models.CharField(max_length=500)
    no_comidas_por_semana = models.IntegerField(default=0)
    no_de_comida_por_dia = models.IntegerField(default=0)
    perfil_defecto = models.ForeignKey("PerfilParametrizado", on_delete = models.CASCADE, null=True, default=None)

    class ConfiguracionForm(ModelForm):
        class Meta:
            ordering = ["direccion_fija"]
            verbose_name = "Configuracion"

    def __str__(self):
        return self.direccion_fija 


class Perfil(models.Model):
    nombre = models.CharField(max_length=200)
    peso_inicio = models.FloatField()
    peso_meta = models.FloatField()
    id_cliente = models.ForeignKey("usuarios.Cliente", on_delete = models.CASCADE)

    class PerfilForm(ModelForm):
        class Meta:
            ordering = ["nombre"]
            verbose_name = "Perfil"

    def __str__(self):
        return self.nombre

def get_upload_to_perfil_e(instance, filename):
    folder_name = 'perfilE'
    #print(instance.hueca_id)
    return os.path.join(folder_name, filename)

class PerfilE(models.Model):
    nombre = models.CharField(max_length=200)
    imagen = models.ImageField(null=True,blank=True,upload_to=get_upload_to_perfil_e)

    class Meta:
        verbose_name = "Perfil_E"

    def __str__(self):
        return self.nombre

@receiver(models.signals.post_delete, sender=PerfilE)
def auto_delete_file_on_delete_PerfilE(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.imagen:
        if os.path.isfile(instance.imagen.path):
            os.remove(instance.imagen.path)


class PerfilParametrizado(models.Model):
    nombre=models.CharField(max_length=200)
    peso_mode_comparator=models.IntegerField(default=1)
    peso_minimo=models.FloatField(blank=True, null=True)
    peso_maximo=models.FloatField(blank=True, null=True)
    altura_mode_comparator=models.IntegerField(default=1)
    altura_minimo=models.FloatField(blank=True, null=True)
    altura_maximo=models.FloatField(blank=True, null=True)
    imc_mode_comparator=models.IntegerField(default=1)
    imc_minimo=models.FloatField(blank=True, null=True)
    imc_maximo=models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name = "PerfilParametrizado"

    def __str__(self):
        return self.nombre

class CategoriasPerfilParametrizado(models.Model):

    perfil_parametrizado=models.ForeignKey("PerfilParametrizado", on_delete = models.CASCADE)
    categoria=models.ForeignKey("productos.Categoria", on_delete = models.CASCADE)

    class Meta:
        verbose_name = "CategoriasPerfilParametrizado"
        unique_together = ('perfil_parametrizado', 'categoria')

    def create(self, perfil_parametrizado, categoria):
        try:
            categoriaPP = CategoriasPerfilParametrizado()
            categoriaPP.perfil_parametrizado = perfil_parametrizado
            categoriaPP.categoria = categoria
            categoriaPP.save()
            return categoriaPP
        except Exception as e:
            return None

    
    def __str__(self):
        return self.perfil_parametrizado.nombre + ' - ' + self.categoria.nombre
