from django.db import models

class Drink(models.Model):
    id_drink =  models.CharField(max_length=50,primary_key=True) 
    drink_name = models.CharField(max_length=50)
    drink_type = models.CharField(max_length=50,blank=True)  
    quantity = models.IntegerField(default=1)
    alcohol_content = models.CharField(max_length=50, blank=True)
    time_consumed = models.DateTimeField(auto_now_add=True)

class Patron(models.Model):
    id_patron = models.AutoField(primary_key=True)    
    age = models.CharField(max_length=3)
    weight = models.CharField(max_length=3)
    drinks = models.ManyToManyField(Drink,null=True)
    consumption = models.FloatField(max_length=3)
    
    def add_drink(self, drink_data):
            if self.consumption < 100:
                drink, created = Drink.objects.get_or_create(id_drink=drink_data.get('id_drink'), defaults=drink_data)
                if drink.alcohol_content == 'Alcoholic':
                    self.consumption =  float(self.consumption) + float(self.weight)/10
                    self.save() 
                    
                if drink in self.drinks.all():
                    existing_drink = self.drinks.get(id_drink=drink.id_drink)
                    existing_drink.quantity += drink_data.get('quantity', 0) 
                    existing_drink.save()
                else:
                    self.drinks.add(drink)

class Drinks(models.Model):
    drinks = models.ManyToManyField(Drink)