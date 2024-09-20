# Generated by Django 5.0.4 on 2024-09-16 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banner', '0003_alter_bannercarousel_media_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bannerproduct',
            options={'ordering': ('id',), 'verbose_name': 'Продукт Баннера', 'verbose_name_plural': 'Продукт Баннера'},
        ),
        migrations.AlterField(
            model_name='bannercarousel',
            name='media',
            field=models.FileField(default=1, upload_to='banner_carousel/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bannercarousel',
            name='media_type',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
