from django.http import JsonResponse
from django_app.core.services.hello_service import HelloService

service = HelloService()

def hello_world(request):
    name = request.GET.get('name')
    message = service.greet(name)
    return JsonResponse({"message": message})