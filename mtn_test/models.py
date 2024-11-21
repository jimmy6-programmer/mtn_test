from django.db import models

class Route(models.Model):
    from_loc = models.CharField(max_length=100)
    to_loc = models.CharField(max_length=100)
    price = models.IntegerField()
    
    def __str__(self):
        return f"{self.from_loc} to {self.to_loc}"
    
class Payment(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="payments")
    phone_number = models.CharField(max_length=15)
    amount = models.IntegerField()
    transaction_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    status = models.CharField(max_length=20, default="pending")  # pending, success, failed
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for {self.route} - {self.status}"    