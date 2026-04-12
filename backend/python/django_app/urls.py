from django.contrib import admin
from django.urls import path
# from adapters.http.hello_handler import hello_world
# from django.http import HttpResponse
# from django.http import JsonResponse
# from django.conf import settings

from django_app.adapters.http.hello_handler import hello_world

# def test_mongo(request):
#     try:
#         db = settings.CLIENT["test_db"]
#         db.command("ping")
#         return JsonResponse({"status": "MongoDB Connected"})
#     except Exception as e:
#         return JsonResponse({"errorrrrr": str(e)})


# def hello_world(request):
#     # Get 'name' from the query string, default to 'World' if missing
#     name = request.GET.get("name", "World")
#     return JsonResponse({"message": f"Hello, {name}!"})

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('hello/', hello_world),
    # path('test-mongo/', test_mongo),
    path('hello-world/', hello_world),
]
