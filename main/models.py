from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=60)
    roll_no = models.IntegerField(unique=True)
    accounting = models.IntegerField(default=0)
    decision_support = models.IntegerField(default=0)
    information_security = models.IntegerField(default=0)
    english_accounting = models.IntegerField(default=0)
    personnel_management = models.IntegerField(default=0) 
    total = models.IntegerField(default=0)
    percent = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name
