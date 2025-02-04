from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView

from apps.banner.api.serializers import (
    BannerListSerializer,
    BannerCarouselListSerializer, BannerProductListSerializer
)
# logger = logging.getLogger(__name__)
from apps.banner.models import *
from utils.expected_fields import check_required_key
from utils.pagination import StandardResultsSetPagination
from utils.responses import (
    bad_request_response,
    success_response,
    success_created_response,
    success_deleted_response,
)


class BannerListView(APIView):
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination

    """ Banner Get View """

    @swagger_auto_schema(operation_description="Retrieve a list of banners",
                         tags=['Banners'],
                         responses={200: BannerListSerializer(many=True)})
    def get(self, request):
        queryset = Banner.objects.all().order_by('order_by_id')
        serializer = BannerListSerializer(queryset, many=True, context={'request': request})
        return success_response(serializer.data)

    @swagger_auto_schema(request_body=BannerListSerializer,
                         operation_description="Banner create",
                         tags=['Banners'],
                         responses={201: BannerListSerializer(many=False)})
    def post(self, request):
        valid_fields = {'name', 'product_data'}
        unexpected_fields = check_required_key(request, valid_fields)
        if unexpected_fields:
            return bad_request_response(f"Unexpected fields: {', '.join(unexpected_fields)}")

        serializer = BannerListSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return success_created_response(serializer.data)
        return bad_request_response(serializer.errors)


class BannerDetailView(APIView):
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination

    @swagger_auto_schema(operation_description="Retrieve Banners",
                         tags=['Banners'],
                         responses={200: BannerListSerializer(many=True)})
    def get(self, request, pk):
        queryset = get_object_or_404(Banner, pk=pk)
        serializer = BannerListSerializer(queryset, context={'request': request, })
        return success_response(serializer.data)

    @swagger_auto_schema(request_body=BannerListSerializer,
                         operation_description="Banners update",
                         tags=['Banners'],
                         responses={200: BannerListSerializer(many=False)})
    def put(self, request, pk):
        queryset = get_object_or_404(Banner, pk=pk)
        serializer = BannerListSerializer(instance=queryset, data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return success_response(serializer.data)
        return bad_request_response(serializer.errors)

    @swagger_auto_schema(operation_description="Delete a Banners",
                         tags=['Banners'],
                         responses={204: 'No content'})
    def delete(self, request, pk):
        queryset = get_object_or_404(Banner, pk=pk)
        queryset.delete()
        return success_deleted_response("Successfully deleted")


class BannerProductDetailView(APIView):
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination

    @swagger_auto_schema(request_body=BannerProductListSerializer,
                         operation_description="Banners product update",
                         tags=['Banner Product'],
                         responses={200: BannerProductListSerializer(many=False)}, )
    def put(self, request, pk):
        valid_fields = {'product_id'}
        unexpected_fields = check_required_key(request, valid_fields)
        if unexpected_fields:
            return bad_request_response(f"Unexpected fields: {', '.join(unexpected_fields)}")

        queryset = get_object_or_404(BannerProduct, pk=pk)
        serializer = BannerProductListSerializer(instance=queryset, data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return success_response(serializer.data)
        return bad_request_response(serializer.errors)

    @swagger_auto_schema(operation_description="Delete a Banners product",
                         tags=['Banner Product'],
                         responses={204: 'No content'})
    def delete(self, request, pk):
        queryset = get_object_or_404(BannerProduct, pk=pk)
        queryset.delete()
        return success_deleted_response("Successfully deleted")


class BannerCarouselListView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser]

    """ Banner Carousel Get View """

    @swagger_auto_schema(operation_description="Retrieve a list of banner carousel",
                         tags=['Banner Carousel'],
                         responses={200: BannerCarouselListSerializer(many=True)},
                         pagination_class=StandardResultsSetPagination)
    def get(self, request):
        queryset = BannerCarousel.objects.all().order_by('-created_at')
        serializer = BannerCarouselListSerializer(queryset, many=True, context={'request': request})
        return success_response(serializer.data)

    @swagger_auto_schema(request_body=BannerCarouselListSerializer,
                         operation_description="Banner create",
                         tags=['Banner Carousel'],
                         responses={201: BannerCarouselListSerializer(many=False)})
    def post(self, request):
        valid_fields = {'name', 'product', 'product_id', 'video', 'title1', 'url1', 'title2', 'url2', 'media'}
        unexpected_fields = check_required_key(request, valid_fields)
        if unexpected_fields:
            return bad_request_response(f"Unexpected fields: {', '.join(unexpected_fields)}")
        serializer = BannerCarouselListSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return success_created_response(serializer.data)
        return bad_request_response(serializer.errors)
    # @swagger_auto_schema(request_body=BannerCarouselListSerializer,
    #                      operation_description="Banner create",
    #                      tags=['Banner Carousel'],
    #                      responses={201: BannerCarouselListSerializer(many=False)})
    # def post(self, request):
    #     valid_fields = {'name', 'product', 'product_id', 'video', 'title1', 'url1', 'title2', 'url2', 'media'}
    #     unexpected_fields = check_required_key(request, valid_fields)
    #     if unexpected_fields:
    #         return bad_request_response(f"Unexpected fields: {', '.join(unexpected_fields)}")
    #
    #     try:
    #         serializer = BannerCarouselListSerializer(data=request.data, context={'request': request})
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #         return success_created_response(serializer.data)
    #     except ValidationError as e:
    #         return bad_request_response(str(e))
    #     except Exception as e:
    #         return bad_request_response(f"An unexpected error occurred: {str(e)}")


class BannerCarouselDetailView(APIView):
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(operation_description="Retrieve Banners",
                         tags=['Banner Carousel'],
                         responses={200: BannerCarouselListSerializer(many=True)})
    def get(self, request, pk):
        queryset = get_object_or_404(BannerCarousel, pk=pk)
        serializer = BannerCarouselListSerializer(queryset, context={'request': request, })
        return success_response(serializer.data)

    # @swagger_auto_schema(request_body=BannerCarouselListSerializer,
    #                      operation_description="Banners update",
    #                      tags=['Banner Carousel'],
    #                      responses={200: BannerCarouselListSerializer(many=False)})
    # def put(self, request, pk):
    #     valid_fields = {'name'}
    #     unexpected_fields = check_required_key(request, valid_fields)
    #     if unexpected_fields:
    #         return bad_request_response(f"Unexpected fields: {', '.join(unexpected_fields)}")
    #
    #     queryset = get_object_or_404(BannerCarousel, pk=pk)
    #     serializer = BannerListSerializer(instance=queryset, data=request.data, context={'request': request})
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.save()
    #         return success_response(serializer.data)
    #     return bad_request_response(serializer.errors)

    @swagger_auto_schema(
        request_body=BannerCarouselListSerializer,
        operation_description="Update Banner Carousel",
        tags=['Banner Carousel'],
        responses={200: BannerCarouselListSerializer(many=False)}
    )
    def put(self, request, pk):
        banner_carousel = get_object_or_404(BannerCarousel, pk=pk)
        serializer = BannerCarouselListSerializer(instance=banner_carousel, data=request.data, partial=True,
                                                  context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_description="Delete a Banners",
                         tags=['Banner Carousel'],
                         responses={204: 'No content'})
    def delete(self, request, pk):
        queryset = get_object_or_404(BannerCarousel, pk=pk)
        queryset.delete()
        return success_deleted_response("Successfully deleted")
