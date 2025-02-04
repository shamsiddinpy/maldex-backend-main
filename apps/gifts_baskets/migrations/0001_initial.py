# Generated by Django 5.0.4 on 2024-09-23 16:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=150, null=True, verbose_name='Название')),
                ('file', models.FileField(blank=True, null=True, upload_to='files/', verbose_name='File')),
                ('created_at', models.DateField(auto_now_add=True, null=True)),
            ],
            options={
                'verbose_name': 'Административные файлы',
                'verbose_name_plural': 'Административные файлы',
                'db_table': 'admin_files',
            },
        ),
        migrations.CreateModel(
            name='SetCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Название')),
                ('is_available', models.BooleanField(default=False, verbose_name='Доступен на сайте?')),
                ('created_at', models.DateField(auto_now_add=True, null=True)),
                ('updated_at', models.DateField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name': 'Каталог наборов',
                'verbose_name_plural': 'Каталог наборов',
                'db_table': 'set_category',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название тэга')),
                ('order', models.IntegerField(blank=True)),
            ],
            options={
                'verbose_name': 'Теги',
                'verbose_name_plural': 'Теги',
            },
        ),
        migrations.CreateModel(
            name='TagCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Тег категории',
                'verbose_name_plural': 'Тег категории',
                'db_table': 'teg_category',
            },
        ),
        migrations.CreateModel(
            name='GiftsBasketCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=150, null=True, verbose_name='Название категории подарочной корзины')),
                ('is_available', models.BooleanField(default=False, verbose_name='Доступен на сайте?')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='gifts_baskets.giftsbasketcategory')),
            ],
            options={
                'verbose_name': 'Подарочные наборы Категория',
                'verbose_name_plural': 'Подарочные наборы Категория',
                'db_table': 'gifts_basket_category',
            },
        ),
        migrations.CreateModel(
            name='GiftsBaskets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Название подарочной корзины')),
                ('small_header', models.TextField(blank=True, null=True, verbose_name='Назовите небольшой заголовок подарочной корзины.')),
                ('article', models.CharField(blank=True, max_length=155, null=True, verbose_name='Артикул')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('other_sets', models.JSONField(blank=True, null=True, verbose_name='Другие наборы')),
                ('price', models.FloatField(blank=True, default=0, null=True, verbose_name='Цена')),
                ('price_type', models.CharField(blank=True, max_length=10, null=True, verbose_name='Цена валюта')),
                ('discount_price', models.FloatField(blank=True, default=0, null=True, verbose_name='Цена со скидкой')),
                ('created_at', models.DateField(auto_now_add=True, null=True, verbose_name='Дата публикации')),
                ('gift_basket_category', models.ManyToManyField(blank=True, related_name='cateGiftBasket', to='gifts_baskets.giftsbasketcategory')),
                ('tags', models.ManyToManyField(related_name='baskets', to='gifts_baskets.tag', verbose_name='Бирки для корзины подарков')),
            ],
            options={
                'verbose_name': 'Подарочные наборы',
                'verbose_name_plural': 'Подарочные наборы',
                'db_table': 'gifts_basket',
            },
        ),
        migrations.CreateModel(
            name='GiftsBasketProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, default=0, null=True, verbose_name='Количество')),
                ('product_sets', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.products', verbose_name='Наборы продуктов')),
                ('gift_basket', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='basket_products', to='gifts_baskets.giftsbaskets')),
            ],
            options={
                'verbose_name': 'Подарочные наборы товара',
                'verbose_name_plural': 'Подарочные наборы товара',
                'db_table': 'gifts_basket_product',
            },
        ),
        migrations.CreateModel(
            name='GiftsBasketImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.ImageField(blank=True, null=True, upload_to='gift_basket/', verbose_name='Изображений')),
                ('gift_basket', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='basket_images', to='gifts_baskets.giftsbaskets')),
            ],
            options={
                'verbose_name': 'Подарочные наборы изображения',
                'verbose_name_plural': 'Подарочные наборы изображения',
                'db_table': 'gifts_basket_image',
            },
        ),
        migrations.CreateModel(
            name='SetProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, default=0, null=True, verbose_name='Количество')),
                ('created_at', models.DateField(auto_now_add=True, null=True)),
                ('updated_at', models.DateField(auto_now=True, null=True)),
                ('product_sets', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.products', verbose_name='Наборы продуктов')),
                ('set_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='setProducts', to='gifts_baskets.setcategory')),
            ],
            options={
                'verbose_name': 'Наборы Каталог товаров',
                'verbose_name_plural': 'Наборы Каталог товаров',
                'db_table': 'set_product',
            },
        ),
        migrations.AddField(
            model_name='tag',
            name='tag_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='categoryTag', to='gifts_baskets.tagcategory'),
        ),
    ]
