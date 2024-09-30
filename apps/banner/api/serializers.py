import logging

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from apps.banner.models import *
from apps.banner.utils import create_banner_products, update_banner_products, \
    create_banner_buttons
from apps.product.api.serializers import ProductDetailSerializers


class BannerProductSerializers(ProductDetailSerializers):
    class Meta:
        model = Products
        fields = ['id', 'name', 'images_set', 'site']


class BannerProductListSerializer(serializers.ModelSerializer):
    productID = serializers.SerializerMethodField()
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = BannerProduct
        fields = ['id', 'productID', 'product_id']

    def update(self, instance, validated_data):
        product = get_object_or_404(Products, id=validated_data.pop('product_id'))
        instance.productID = product
        instance.save()
        return instance

    def get_productID(self, obj):
        data = BannerProductSerializers(obj.productID, context=self.context)
        return data.data


class ButtonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Button
        fields = ['title', 'url']


class BannerListSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    product_set = serializers.SerializerMethodField()
    product_data = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )

    class Meta:
        model = Banner
        fields = ['id', 'name', 'product_set', 'product_data', 'order_by_id']

    def create(self, validated_data):
        product_data = validated_data.pop('product_data', [])
        create_banner = Banner.objects.create(**validated_data)
        create_banner_products(product_data, create_banner)
        return create_banner

    def update(self, instance, validated_data):
        product_data = validated_data.pop('product_data', [])
        update_banner_products(instance, product_data)
        return super().update(instance, validated_data)

    def get_product_set(self, obj):
        data = BannerProductListSerializer(obj.bannerID.all(), many=True, context=self.context)
        return data.data


logger = logging.getLogger(__name__)


class BannerCarouselListSerializer(serializers.ModelSerializer):
    product = ProductDetailSerializers(read_only=True)
    product_id = serializers.CharField(write_only=True, required=False)
    media_type = serializers.CharField(read_only=True)
    buttons = ButtonSerializer(many=True, read_only=True)
    title1 = serializers.CharField(write_only=True, required=False)
    url1 = serializers.CharField(write_only=True, required=False)
    title2 = serializers.CharField(write_only=True, required=False)
    url2 = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = BannerCarousel
        fields = ['id', 'name', 'media', 'media_type', 'product', 'product_id', 'buttons', 'title1', 'url1', 'title2',
                  'url2']

    def create(self, validated_data):
        product_id = validated_data.pop('product_id', None)
        product = get_object_or_404(Products, id=product_id) if product_id else None
        media = validated_data.pop('media', None)
        if media:
            media_type = media.content_type.split('/')[0]
            validated_data['media_type'] = media_type
        else:
            validated_data['media'] = None
        buttons_data = []
        title1 = validated_data.pop('title1', None)
        url1 = validated_data.pop('url1', None)
        title2 = validated_data.pop('title2', None)
        url2 = validated_data.pop('url2', None)
        buttons_data.append({'title': title1, 'url': url1}) if title1 and url1 else None
        buttons_data.append({'title': title2, 'url': url2}) if title2 and url2 else None
        create_banner_carousel = BannerCarousel.objects.create(**validated_data, product=product)
        create_banner_buttons(buttons_data, create_banner_carousel)
        return create_banner_carousel

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    # def update(self, instance, validated_data):
    #     product_id = validated_data.pop('product_id', None)
    #     product = get_object_or_404(Products, id=product_id) if product_id else None
    #
    #     media = validated_data.pop('media', None)
    #     if media:
    #         instance.media = media
    #         instance.media_type = media.content_type.split('/')[0]
    #     elif media is None and 'media' in validated_data:
    #         instance.media = None
    #         instance.media_type = None
    #
    #     buttons_data = []
    #     title1 = validated_data.pop('title1', None)
    #     url1 = validated_data.pop('url1', None)
    #     title2 = validated_data.pop('title2', None)
    #     url2 = validated_data.pop('url2', None)
    #
    #     if title1 and url1:
    #         buttons_data.append({'title': title1, 'url': url1})
    #     if title2 and url2:
    #         buttons_data.append({'title': title2, 'url': url2})
    #
    #     # Update all other fields
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
    #
    #     instance.product = product
    #     instance.save()
    #
    #     # Update or create buttons
    #     instance.buttons.all().delete()  # Remove existing buttons
    #     create_banner_buttons(buttons_data, instance)
    #
    #     return instance #Todt

    def validate_media(self, media):
        media_type = media.content_type.split('/')[0]
        if media_type not in ['image', 'video']:
            raise serializers.ValidationError('Invalid media type')
        return media
