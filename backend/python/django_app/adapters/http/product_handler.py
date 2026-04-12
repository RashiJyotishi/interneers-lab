import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django_app.core.services.product_service import ProductService
from django_app.adapters.repositories.in_memory_product_repository import InMemoryProductRepository
from dataclasses import asdict

# Wire up once (in real apps this is done via dependency injection)
repository = InMemoryProductRepository()
service = ProductService(repository)

@csrf_exempt
def products(request):
    if request.method == 'GET':
        all_products = service.get_all_products()
        return JsonResponse([asdict(p) for p in all_products], safe=False, status=200)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            product = service.create_product(data)
            return JsonResponse(asdict(product), status=201)
        except ValueError as e:
            return JsonResponse({'errors': e.args[0]}, status=400)

@csrf_exempt
def product_detail(request, product_id):
    if request.method == 'GET':
        product = service.get_product(product_id)
        if not product:
            return JsonResponse({'error': 'Product not found'}, status=404)
        return JsonResponse(asdict(product), status=200)

    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            product = service.update_product(product_id, data)
            if not product:
                return JsonResponse({'error': 'Product not found'}, status=404)
            return JsonResponse(asdict(product), status=200)
        except ValueError as e:
            return JsonResponse({'errors': e.args[0]}, status=400)

    elif request.method == 'DELETE':
        deleted = service.delete_product(product_id)
        if not deleted:
            return JsonResponse({'error': 'Product not found'}, status=404)
        return JsonResponse({}, status=204)