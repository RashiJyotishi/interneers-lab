import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django_app.core.services.product_category_service import ProductCategoryService
from django_app.adapters.repositories.mongo_product_category_repository import MongoProductCategoryRepository
from dataclasses import asdict

category_repository = MongoProductCategoryRepository()
service = ProductCategoryService(category_repository)

@csrf_exempt
def categories(request):
    if request.method == 'GET':
        all_cats = service.get_all_categories()
        return JsonResponse([asdict(c) for c in all_cats], safe=False, status=200)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            category = service.create_category(data)
            return JsonResponse(asdict(category), status=201)
        except ValueError as e:
            return JsonResponse({'errors': e.args[0]}, status=400)

@csrf_exempt
def category_detail(request, category_id):
    if request.method == 'GET':
        category = service.get_category(category_id)
        if not category:
            return JsonResponse({'error': 'Category not found'}, status=404)
        return JsonResponse(asdict(category), status=200)

    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            category = service.update_category(category_id, data)
            if not category:
                return JsonResponse({'error': 'Category not found'}, status=404)
            return JsonResponse(asdict(category), status=200)
        except ValueError as e:
            return JsonResponse({'errors': e.args[0]}, status=400)

    elif request.method == 'DELETE':
        deleted = service.delete_category(category_id)
        if not deleted:
            return JsonResponse({'error': 'Category not found'}, status=404)
        return JsonResponse({}, status=204)