from django.db import models

class Header(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.CharField(max_length=50)
    quantity = models.IntegerField()
    message = models.CharField(max_length=50)

    def __str__(self):
        return self.description

class Detail(models.Model):
    header = models.ForeignKey(Header, on_delete=models.CASCADE)
    dni = models.CharField(max_length=12)
    status = models.BooleanField()
    send_date = models.DateField()
    times = models.IntegerField()
    def __str__(self):
        
        return self.dni
