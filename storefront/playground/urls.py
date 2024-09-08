from django import urls
from . import views

urlpatterns = [
    urls.path('restaurant/',views.get_restaurant),
]