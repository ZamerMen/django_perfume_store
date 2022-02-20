from time import time

from django.db import models
from django.contrib.auth import get_user_model

from django.utils.text import slugify

User = get_user_model()


def gen_slug(s):
    return slugify(s, allow_unicode=True)


def gen_slug_time(s):
    return f'{slugify(s, allow_unicode=True)}-{str(int(time()))}'


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name



class Perfume(models.Model):
    name = models.CharField(max_length=150, unique=True, db_index=True)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='photos/perfume/%Y/%m/%d', blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    available = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, db_index=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Аромат'
        verbose_name_plural = 'Ароматы'
        index_together = (('id', 'slug'),)


    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'perfume - {self.name}'



class Element(models.Model):
    title = models.CharField(max_length=150, unique=True, db_index=True)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='photos/perfume_element/%Y/%m/%d')
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'perfume element - {self.title}'



class Comment(models.Model):
    comment = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    perfume = models.ForeignKey(Perfume, on_delete=models.CASCADE)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, db_index=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug_time(self.perfume)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'user - {self.user} comment to {self.perfume} at {self.time_create}'