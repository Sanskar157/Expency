from django.db import models

# Create your models here.
class Transaction(models.Model):
  amount = models.DecimalField(max_digits=10,decimal_places=2)
  date = models.DateField()
  description= models.CharField(max_length=255)

  def __str__(self):
    return f"{self.date} - {self.description} - {self.amount}"
