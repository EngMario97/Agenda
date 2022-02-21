from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nome')
    lastname = models.CharField(max_length=255, blank=True, verbose_name='Sobrenome')
    telephone = models.CharField(max_length=255, verbose_name='Telefone')
    email = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Criado em')
    description = models.TextField(blank=True, verbose_name='Descrição')
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, verbose_name='Categoria')
    show = models.BooleanField(default=True, verbose_name='Mostrar')
    photo = models.ImageField(blank=True, upload_to='photos/%Y/%m/%d', verbose_name='Foto')

    def __str__(self):
        return self.name


