import requests
import json
from django.http import JsonResponse
from .models import Patron , Drink ,Drinks
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def create_patron(request):
    if request.method == "POST":
        # Get the data from the request
        data = json.loads(request.body)
        weight = data.get('weight','')

        if not weight :
            return JsonResponse({'error': 'weight, and email are required'}, status=400)
        
        new_patron = Patron.objects.create(
            weight=weight,
            consumption=0
        )
        return JsonResponse({'id_patron': new_patron.id_patron, 'weight': new_patron.weight, 'consumption': new_patron.consumption}, status=201)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405) 

@csrf_exempt
def update_patron_drinks(request, patron_id):
    if request.method == 'POST':
        # Retrieve the patron object by ID
        try:
            patron = Patron.objects.get(id_patron=patron_id)
        except Patron.DoesNotExist:
            return JsonResponse({'error': 'Patron not found'}, status=404)
        
        # Assuming the request data contains information about the drink
        drink_data = json.loads(request.body)
        patron.add_drink(drink_data)
        
        return JsonResponse({'message': 'Drink added to patron successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    
def get_patron(request, patron_id):
    if request.method == 'GET':
        try:
            patron = Patron.objects.get(id_patron=patron_id)
            drinks = patron.drinks.all()

            serialized_drinks = [{
                'id_drink': drink.id_drink,
                'drink_name': drink.drink_name,
                'drink_type': drink.drink_type,
                'quantity': drink.quantity,
                'alcohol_content': drink.alcohol_content,
                'time_consumed': drink.time_consumed
            } for drink in drinks]

            return JsonResponse({
                'id': patron.id_patron,
                'weight': patron.weight,
                'consumption': patron.consumption,
                'drinks': serialized_drinks
            })

        except Patron.DoesNotExist:
            return JsonResponse({'error': 'Patron not found'}, status=404)
    else:
            return JsonResponse({'error': 'Method not allowed'}, status=405)
     
@csrf_exempt
def delete_patron(request, patron_id):
    if request.method == 'DELETE':
        try:
            patron = Patron.objects.get(id_patron=patron_id)
            
            patron.delete()
            
            return JsonResponse({'message': 'Patron deleted successfully'}, status=204)
        
        except Patron.DoesNotExist:
    
            return JsonResponse({'error': 'Patron not found'}, status=404)
    
    else:
            return JsonResponse({'error': 'Method not allowed'}, status=405)

def get_all_patrons(request):
    queryset = Patron.objects.all()

    json_data = []
    for patron in queryset:
        drinks_info = [
            {'id_drink': drink.id_drink,
            'drink_name': drink.drink_name,
            'drink_type': drink.drink_type,
            'quantity': drink.quantity,
            'alcohol_content': drink.alcohol_content,
            'time_consumed': drink.time_consumed,} for drink in patron.drinks.all()
            ]
        patron_info = {
            'id_patron' : patron.id_patron,
            'weight' : patron.weight,
            'drinks' : drinks_info,
            'consumption' : patron.consumption,
        }
        json_data.append(patron_info)

    return JsonResponse(json_data, safe=False)
    
def get_all_drinks(request):
    drinks_instances = Drinks.objects.all()

    drinks_info = {
            'drinks': []
        }

    for drinks_instance in drinks_instances:

        for drink in drinks_instance.drinks.all():
            drink_info = {
                'id_drink': drink.id_drink,
                'drink_name': drink.drink_name,
                'drink_type': drink.drink_type,
                'quantity': drink.quantity,
                'alcohol_content': drink.alcohol_content,
                'time_consumed': drink.time_consumed,
            }
            drinks_info['drinks'].append(drink_info)

    return JsonResponse(drinks_info, safe=False)

    
def get(request):
    if request.method == 'GET':
        response = requests.get('https://www.thecocktaildb.com/api/json/v1/1/search.php?f=a')
        if response.status_code == 200:
            drink_data = response.json()
            drinks = drink_data['drinks']
            
            for drink in drinks:
                drink_instance, created = Drink.objects.get_or_create(
                    id_drink= drink['idDrink'],
                    drink_name=drink['strDrink'],
                    drink_type=drink['strCategory'],
                    alcohol_content= drink['strAlcoholic']
                )
                drinks_instance, created = Drinks.objects.get_or_create()
                drinks_instance.drinks.add(drink_instance)
                
            return JsonResponse({'message': 'Drink information retrieved and saved successfully'}, status=200)
        else:
            return JsonResponse({'error': 'Failed to retrieve drink information'}, status=response.status_code)

@csrf_exempt
def decrease_consumption(request):
    if request.method == "PATCH":
        patrons = Patron.objects.all()
        for patron in patrons:
                if patron.consumption > 0:
                    patron.consumption -= 2
                    patron.save()
        return get_all_patrons(request)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
