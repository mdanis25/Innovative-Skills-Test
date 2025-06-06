from django.db import models 
 

class Product(models.Model):  
    name = models.CharField(max_length=255) 
    description = models.TextField() 
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    stock = models.PositiveIntegerField()  
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 
   
    class Meta: 
        unique_together = ('name', 'price', 'description')
    
    def __str__(self): 
        return self.name 
    