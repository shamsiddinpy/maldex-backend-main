from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.product.api.serializers import (
    CategoryListSerializers, MainCategorySerializer, CategoryProductsSerializer, SubCategorySerializer,
    TertiaryCategorySerializer, CategoryAutoUploaderSerializer, ExternalCategoryListSerializer, CategoryMoveSerializer,
    HomeCategorySerializer
)
from apps.product.filters import ProductCategoryFilter
from apps.product.models import ProductCategories, ExternalCategory, Products
from utils.pagination import StandardResultsSetPagination
from utils.responses import bad_request_response, success_response, success_created_response, success_deleted_response


# CACHE_TTL = 20


class CategoryListView(APIView):
    """
    API endpoint to list and create product categories.
    """
    pagination_class = StandardResultsSetPagination
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_description="Retrieve a list of categories",
        manual_parameters=[],
        tags=['Categories'],
        responses={200: CategoryListSerializers(many=True)}

    )
    def get(self, request):
        # cache_key = 'home_category'
        # cache_data = cache.get(cache_key)
        # if cache_data is not None:
        #     return success_response(cache_data)
        queryset = ProductCategories.objects.all().select_related('parent').prefetch_related('children__parent').filter(
            parent=None).order_by('order')

        filterset = ProductCategoryFilter(request.GET, queryset=queryset)
        if filterset.is_valid():
            queryset = filterset.qs
        is_popular = request.query_params.get('is_popular', None)
        if is_popular is True:
            queryset = queryset.order_by('order_top')
        serializers = MainCategorySerializer(queryset.order_by('-is_available', 'order', 'order_by_site'), many=True,
                                             context={'request': request})
        # cache.set(cache_key, serializers.data, CACHE_TTL)
        return success_response(serializers.data)

    @swagger_auto_schema(
        request_body=MainCategorySerializer,
        operation_description="Create a new product category",
        tags=['Categories'],
        responses={201: MainCategorySerializer(many=False)}
    )
    def post(self, request):
        """
        Create a new product category.
        """
        serializers = MainCategorySerializer(data=request.data, context={'request': request})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            # cache.delete('home_category')
            return success_created_response(serializers.data)
        return bad_request_response(serializers.errors)


class CategoryDetailView(APIView):
    """
    API endpoint to retrieve, update, and delete a specific product category.
    """
    pagination_class = StandardResultsSetPagination
    permission_classes = [AllowAny]

    # def get_cache_key(self, pk):
    #     return f'category_detail_{pk}'  # Todo

    @swagger_auto_schema(
        operation_description="Retrieve a specific product category",
        tags=['Categories'],
        responses={200: CategoryListSerializers(many=True)}
    )
    def get(self, request, pk):
        """
        Retrieve a specific product category.
        """
        # cache_key = self.get_cache_key(pk)
        # cache_data = cache.get(cache_key)
        # if cache_data is not None:
        #     return success_response(cache_data)
        queryset = get_object_or_404(ProductCategories, pk=pk)
        serializers = MainCategorySerializer(queryset, context={'request': request})
        # cache.set(cache_key, serializers.data, CACHE_TTL)
        return success_response(serializers.data)

    @swagger_auto_schema(
        request_body=CategoryListSerializers,
        operation_description="Update a specific product category",
        tags=['Categories'],
        responses={200: CategoryListSerializers(many=False)}
    )
    def put(self, request, pk):
        queryset = get_object_or_404(ProductCategories, pk=pk)
        data = request.data.copy()
        data.pop('logo', None)
        data.pop('icon', None)
        serializers = CategoryListSerializers(instance=queryset, data=data, context={
            'request': request,
            'logo': request.FILES.get('logo', None),
            'icon': request.FILES.get('icon', None)
        })
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            # cache.delete(self.get_cache_key(pk))
            return success_response(serializers.data)
        return bad_request_response(serializers.errors)

    @swagger_auto_schema(
        operation_description="Delete a specific product category",
        tags=['Categories'],
        responses={204: 'No content'}
    )
    def delete(self, request, pk):
        """
        Delete a specific product category.
        """
        queryset = get_object_or_404(ProductCategories, pk=pk)
        queryset.delete()
        # cache.delete(self.get_cache_key(pk))
        return success_deleted_response("Successfully deleted")


class HomeCategoryView(APIView):
    """
    API endpoint to handle the home category.
    """
    pagination_class = StandardResultsSetPagination
    permission_classes = [AllowAny, ]

    # @method_decorator(cache_page(600))
    @swagger_auto_schema(
        operation_description="Retrieve category or sub categories for home view",
        tags=['Categories'],
        responses={200: CategoryProductsSerializer()}
    )
    def get(self, request):
        """
        Retrieve category or sub categories for home view.
        """
        category = ProductCategories.objects.filter(parent=None, home=True).first()
        serializers = HomeCategorySerializer(category, context={'request': request})
        return success_response(serializers.data)

    @swagger_auto_schema(
        operation_description="Create category or sub categories for home view",
        tags=['Categories'],
        responses={200: CategoryProductsSerializer()}
    )
    def post(self, request):
        """
        Set a category as the home category.
        """
        serializers = HomeCategorySerializer(data=request.data, context={'request': request})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return success_created_response(serializers.data)
        return bad_request_response(serializers.errors)


category_id_param = openapi.Parameter('category_id', openapi.IN_QUERY,
                                      description="Main Category ID",
                                      type=openapi.TYPE_STRING)
subcategory_id_param = openapi.Parameter('subcategory_id', openapi.IN_QUERY,
                                         description="Sub Category ID",
                                         type=openapi.TYPE_STRING)


@swagger_auto_schema(tags=['Categories'],
                     responses={200: SubCategorySerializer(many=True)},
                     operation_description='Get all sub categories',
                     method='GET')
@api_view(['GET'])
def get_main_categories(request):
    categories = list(ProductCategories.objects.filter(parent=None).values('id', 'name'))
    return success_response(categories)


@swagger_auto_schema(manual_parameters=[category_id_param], tags=['Categories'],
                     responses={200: SubCategorySerializer(many=True)},
                     operation_description='Get all sub categories',
                     method='GET')
@api_view(['GET'])
def get_subcategories(request, category_id):
    try:
        category_id = int(category_id)
        subcategories = list(ProductCategories.objects.filter(parent__id=category_id).values('id', 'name'))
        return success_response(subcategories)
    except ValueError:
        return success_response([])


@swagger_auto_schema(manual_parameters=[subcategory_id_param], tags=['Categories'],
                     responses={200: TertiaryCategorySerializer(many=True)},
                     operation_description='Get all tertiary categories',
                     method='GET')
@api_view(['GET'])
def get_tertiary_categories(request, subcategory_id):
    try:
        subcategory_id = int(subcategory_id)
        tertiary_categories = list(ProductCategories.objects.filter(parent_id=subcategory_id).values('id', 'name'))
        return success_response(tertiary_categories)
    except ValueError:
        return success_response([])


@api_view(['GET'])
def get_all_subcategories(request):
    search = request.GET.get('search')
    response = []
    subcategories = ProductCategories.objects.filter(parent__parent=None, parent__isnull=False,
                                                     parent__is_available=False).order_by('name')
    subcategories = subcategories.filter(name__icontains=search) if search else subcategories
    for cat in subcategories:
        ids = [cat.id]
        for sub in cat.children.all():
            ids.append(sub.id)
        count = Products.objects.filter(categoryId__id__in=ids).count()
        response.append({'name': cat.name, 'id': cat.id, 'site': cat.site, 'count': count})
    return Response(response)


class ExternalCategoryList(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Retrieve category or sub categories for home view",
        tags=['External Categories'],
        responses={200: CategoryProductsSerializer(many=True)}
    )
    def get(self, request):
        queryset = ExternalCategory.objects.all()
        serializer = ExternalCategoryListSerializer(queryset, many=True)
        return success_response(serializer.data)


class CategoryUploaderListView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=CategoryAutoUploaderSerializer,
        operation_description="Upload new product category",
        tags=['Uploader Categories'],
        responses={201: CategoryAutoUploaderSerializer(many=False), 400: 'Bad request'}
    )
    def post(self, request):
        serializer = CategoryAutoUploaderSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryMove(APIView):
    @swagger_auto_schema(
        tags=['Category'],
        responses={200: MainCategorySerializer()},
        request_body=CategoryMoveSerializer()
    )
    def post(self, request):
        categories_data = request.data.pop('categories_data')
        categories_data = [categories_data] if not isinstance(categories_data, list) else categories_data
        request.data['categories_data'] = categories_data
        serializer = CategoryMoveSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_200_OK)


class CategorySeenView(APIView):

    def post(self, request, pk):
        category = get_object_or_404(ProductCategories, pk=pk)
        category.products.update(added_recently=False)
        return success_response('OK')
