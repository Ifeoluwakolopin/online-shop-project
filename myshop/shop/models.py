from django.db import models
from django.urls import reverse
from parler.fields import TranslationsForeignKey
from parler.models import TranslatableModel, TranslatedFieldsModel


class Category(TranslatableModel):
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
            args=[self.slug])
    

class Product(TranslatableModel):
    category = models.ForeignKey(Category,
        related_name='products',
        on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/%Y/%m/%d',
        blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('shop:product_detail',
            args=[self.id, self.slug])


# Explicit models retain the tables and unique_together from 0002_translations.
class CategoryTranslation(TranslatedFieldsModel):
    master = TranslationsForeignKey(
        Category, related_name='translations', null=True,
        editable=False, on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        verbose_name = 'category Translation'
        db_table = 'shop_category_translation'
        db_tablespace = ''
        managed = True
        default_permissions = ()
        unique_together = (('language_code', 'master'),)


class ProductTranslation(TranslatedFieldsModel):
    master = TranslationsForeignKey(
        Product, related_name='translations', null=True,
        editable=False, on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'product Translation'
        db_table = 'shop_product_translation'
        db_tablespace = ''
        managed = True
        default_permissions = ()
        unique_together = (('language_code', 'master'),)