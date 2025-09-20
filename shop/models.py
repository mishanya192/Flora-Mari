from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class Product(models.Model):
    CATEGORY_CHOICES =[
        ('BOUQUET','Букеты'),
        ('POT','Комнактные расстения'),
        ('DRIED','Сухоцветы'),
        ('ACCESSORY','Аксессуары'),
    ]

    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Цена" 
    )

    image = models.ImageField(
        upload_to='products/',
        blank=True,
        verbose_name="Изображение",
        help_text="Формат: JPG, PNG. Максимальный размер: 2MB"
    )

    category = models.CharField(
        max_length=20,
        choices= CATEGORY_CHOICES,
        default='BOUQUET',
        verbose_name="Категория"
    )

    is_active = models.BooleanField(default=True, verbose_name="Активный")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.get_category_display()}"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.price < Decimal('0.01'):
            raise ValidationError({'price': 'Цена не может быть меньше 0.01'})