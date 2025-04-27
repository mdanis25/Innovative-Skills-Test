from django.db import models 
import uuid
from products.models import Product
from django.contrib.auth import get_user_model
User = get_user_model()
 
 
class Purchase(models.Model):  
    STATUS_CHOICES = ( 
        ('pending', 'Pending'), 
        ('completed', 'Completed'), 
        ('canceled', 'Canceled'), 
    )
    purchase_id  = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='purchases')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='purchases')  
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2) 
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    
    @property 
    def total_price(self):
        return self.product.price * self.quantity
   
    def __str__(self):
        return f'Purchase {self.purchase_id} by {self.user.username}'
    