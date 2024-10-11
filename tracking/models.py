from django.db import models

class Violation(models.Model):
    date = models.DateField()
    violation_type = models.CharField(max_length=100)
    fine_collected = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    vehicle_number = models.CharField(max_length=20)
    officer_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.violation_type} - {self.vehicle_number}"

class ViolationType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name