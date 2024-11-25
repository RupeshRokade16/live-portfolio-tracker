from django.db import models
import uuid

# Create your models here.
class Portfolio(models.Model):
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    symbol = models.CharField(max_length=5,unique=True)
    purchase_date = models.DateField()
    volume = models.PositiveIntegerField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Portfolio"
        verbose_name_plural = "Portfolios"
        ordering = ['-symbol']

    def __str__(self):
        return f"{self.symbol} - {self.purchase_date} - {self.volume} @ {self.purchase_price}"
    
class StockData(models.Model):
    symbol = models.CharField(max_length=5, unique=True)  # Unique identifier for stock
    stock_name = models.CharField(max_length=100)        # Name of the stock
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Latest price
    current_time = models.DateTimeField()    
    

    class Meta:
        verbose_name = "Stock Data from Yahoo"
        verbose_name_plural = "Stock Data"
        ordering = ['-current_time']

    def __str__(self):
        return f"{self.symbol} - {self.stock_name} - ${self.price} @ {self.current_time}"