from django.db import models

# Create your models here.


class County(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=200)
    county = models.ForeignKey(County, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Street(models.Model):
    name = models.CharField(max_length=200)
    county = models.ForeignKey(County, null=True, on_delete=models.SET_NULL)
    city = models.ForeignKey(City, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name
