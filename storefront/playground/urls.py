from django import urls
from . import views

urlpatterns = [
    urls.path('hello/',views.print_hello),
]