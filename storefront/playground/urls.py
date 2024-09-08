from django import urls
from . import views

urlpatterns = [
    # urls.path('',views.get_home),
    urls.path('restaurants/', views.get_restaurants, name='get_restaurants'),
]