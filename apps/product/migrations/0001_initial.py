# Generated by Django 5.0.4 on 2024-09-21 11:39

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Colors',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Уникальный идентификатор')),
                ('name', models.CharField(max_length=500, verbose_name='Название цвета')),
                ('hex', models.CharField(blank=True, max_length=16, null=True)),
            ],
            options={
                'verbose_name': 'Цвет',
                'verbose_name_plural': 'Цвет',
                'db_table': 'product_color',
            },
        ),
        migrations.CreateModel(
            name='ProductBanner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=512)),
                ('subtitle', models.CharField(max_length=1024)),
                ('image', models.ImageField(upload_to='product-banners/')),
                ('button_title', models.CharField(max_length=128)),
                ('button_url', models.URLField()),
            ],
            options={
                'verbose_name': 'product banner',
                'verbose_name_plural': 'product banners',
                'db_table': 'product_banners',
            },
        ),
        migrations.CreateModel(
            name='ProductFilterModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Уникальный идентификатор')),
                ('title', models.CharField(max_length=255)),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Дата публикации')),
            ],
            options={
                'verbose_name': 'фильтр для продукта',
                'verbose_name_plural': 'фильтры для продукта',
                'db_table': 'filter_for_product',
            },
        ),
        migrations.CreateModel(
            name='SiteLogo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site', models.CharField(max_length=256)),
                ('logo', models.ImageField(upload_to='site_logos/')),
            ],
            options={
                'verbose_name': 'Site Logo',
                'verbose_name_plural': 'Site Logos',
                'db_table': 'site_logos',
            },
        ),
        migrations.CreateModel(
            name='ProductCategories',
            fields=[
                ('id', models.IntegerField(editable=False, primary_key=True, serialize=False, unique=True, verbose_name='Уникальный идентификатор')),
                ('name', models.CharField(max_length=550, verbose_name='Название категории')),
                ('title', models.CharField(blank=True, max_length=500, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True, max_length=500, null=True)),
                ('is_popular', models.BooleanField(default=False, verbose_name='Популярен?')),
                ('is_hit', models.BooleanField(default=False, verbose_name='Хит?')),
                ('is_new', models.BooleanField(default=False, verbose_name='Новый?')),
                ('is_available', models.BooleanField(default=False, verbose_name='Доступен на сайте?')),
                ('icon', models.FileField(blank=True, null=True, upload_to='icon/', verbose_name='Категория значка')),
                ('logo', models.FileField(blank=True, null=True, upload_to='logo/', verbose_name='Категория логотипа')),
                ('site', models.CharField(blank=True, max_length=500, null=True)),
                ('seo_title', models.CharField(blank=True, max_length=500, null=True, verbose_name='SEO Заголовок')),
                ('seo_description', models.TextField(blank=True, null=True, verbose_name='SEO Описание')),
                ('order', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('order_top', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('order_by_site', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Порядок сайта')),
                ('home', models.BooleanField(default=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('products_count', models.IntegerField(default=0)),
                ('recently_products_count', models.IntegerField(default=0)),
                ('discounts', models.JSONField(blank=True, null=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='product.productcategories')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категория',
                'db_table': 'product_category',
                'ordering': ('-is_available', 'order', 'order_by_site'),
            },
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
            ],
            options={
                'verbose_name': 'Подкатегория',
                'verbose_name_plural': 'Подкатегории',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('product.productcategories',),
        ),
        migrations.CreateModel(
            name='TertiaryCategory',
            fields=[
            ],
            options={
                'verbose_name': 'Третичная категория',
                'verbose_name_plural': 'Третичные категории',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('product.productcategories',),
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigIntegerField(blank=True, primary_key=True, serialize=False, unique=True, verbose_name='Уникальный идентификатор')),
                ('name', models.CharField(blank=True, max_length=512, null=True, verbose_name='Название продукта')),
                ('code', models.IntegerField(blank=True, default=0, null=True)),
                ('article', models.CharField(blank=True, max_length=512, null=True, verbose_name='Артикул')),
                ('product_size', models.CharField(blank=True, max_length=256, null=True, verbose_name='Размер товара')),
                ('material', models.CharField(blank=True, default='S-XXL', max_length=512, null=True, verbose_name='Материал')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описания')),
                ('brand', models.CharField(blank=True, max_length=500, null=True, verbose_name='Бренд')),
                ('price', models.FloatField(blank=True, default=0, null=True, verbose_name='Цена')),
                ('price_type', models.CharField(blank=True, choices=[('RUB', 'RUB'), ('USD', 'USD')], default='RUB', max_length=10, null=True, verbose_name='Цена валюта')),
                ('discount_price', models.FloatField(blank=True, default=None, null=True, verbose_name='Цена со скидкой')),
                ('weight', models.CharField(blank=True, max_length=128, null=True, verbose_name='Масса')),
                ('barcode', models.CharField(blank=True, max_length=128, null=True, verbose_name='Штрих-код продукта')),
                ('ondemand', models.BooleanField(blank=True, default=True, null=True)),
                ('moq', models.CharField(blank=True, default='0', max_length=512, null=True)),
                ('days', models.IntegerField(blank=True, default=0, null=True)),
                ('pack', models.JSONField(blank=True, null=True)),
                ('prints', models.JSONField(blank=True, null=True)),
                ('warehouse', models.JSONField(blank=True, null=True)),
                ('sizes', models.JSONField(blank=True, null=True)),
                ('is_popular', models.BooleanField(blank=True, default=False, null=True, verbose_name='Популярен?')),
                ('is_hit', models.BooleanField(blank=True, default=False, null=True, verbose_name='Хит?')),
                ('is_new', models.BooleanField(blank=True, default=False, null=True, verbose_name='Новый?')),
                ('site', models.CharField(blank=True, max_length=500, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Данные опубликованы')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('home', models.BooleanField(default=False)),
                ('discounts', models.JSONField(blank=True, null=True)),
                ('common_name', models.CharField(blank=True, db_index=True, max_length=500, null=True)),
                ('added_recently', models.BooleanField(default=True)),
                ('categoryId', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='product.productcategories', verbose_name='Категория продукта')),
                ('colorID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='product.colors', verbose_name='Цвета')),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='product.products')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукт',
                'db_table': 'product',
                'ordering': ('-updated_at',),
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Уникальный идентификатор')),
                ('image', models.ImageField(blank=True, null=True, upload_to='media/product/', verbose_name='изображения')),
                ('image_url', models.URLField(blank=True, max_length=1024, null=True, verbose_name='URL изображения')),
                ('productID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images_set', to='product.products', verbose_name='Код товара')),
            ],
            options={
                'verbose_name': 'Изображения продукта',
                'verbose_name_plural': 'Изображения продукта',
                'db_table': 'product_images',
            },
        ),
        migrations.CreateModel(
            name='ProductFilterProducts',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Уникальный идентификатор')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Дата публикации')),
                ('filter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='product.productfiltermodel')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='filter_products', to='product.products')),
            ],
            options={
                'verbose_name': 'фильтрует продукты по продукту',
                'verbose_name_plural': 'фильтрует продукты по продукту',
                'db_table': 'filter_for_product_products',
            },
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='product.products')),
            ],
            options={
                'verbose_name': 'Like',
                'verbose_name_plural': 'Likes',
                'db_table': 'likes',
            },
        ),
        migrations.CreateModel(
            name='ExternalCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.CharField(max_length=500, verbose_name='внешний идентификатор')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='external_categories', to='product.productcategories', verbose_name='категория')),
            ],
            options={
                'verbose_name': 'Категория сайта',
                'verbose_name_plural': 'Категории сайта',
                'db_table': 'product_site_category',
                'unique_together': {('external_id', 'category')},
            },
        ),
    ]
