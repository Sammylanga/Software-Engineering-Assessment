# urls.py

from django.urls import path
from .views import create_patron, get_patron, update_patron_drinks, get, delete_patron, get_all_drinks , get_all_patrons, decrease_consumption

urlpatterns = [
    path('patrons/create/', create_patron, name='create_patron'),
    path('patrons/<int:patron_id>/', get_patron, name='get_patron'),
    path('patrons/update_drinks/<int:patron_id>/', update_patron_drinks, name='update_patron_drinks'),
    path('update_all_drinks/', get, name='get'),
    path('delete_patron/<int:patron_id>/', delete_patron, name='delete_patron'),
    path('get_all_drinks/', get_all_drinks , name='get_all_drinks'),
    path('all_patrons/', get_all_patrons, name='patron-list'),
    path('decrease_consumption/', decrease_consumption, name='decrease_consumption')
    # Add other URL patterns as needed
]
