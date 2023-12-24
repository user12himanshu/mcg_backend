from django.db import models
from django.core.validators import MaxValueValidator, FileExtensionValidator
from datetime import date


class CarBrand(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    name = models.CharField(max_length=200)
    brand = models.ForeignKey(CarBrand, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class CarYear(models.Model):
    year = models.IntegerField(validators=[MaxValueValidator(date.today().year)])
    car = models.ForeignKey(CarModel, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.year)


class Diagnostic(models.Model):
    file_extension_validator = FileExtensionValidator(allowed_extensions=['pdf'])
    car = models.ForeignKey(CarModel, on_delete=models.DO_NOTHING)
    brand = models.ForeignKey(CarBrand, on_delete=models.DO_NOTHING)
    year = models.ForeignKey(CarYear, on_delete=models.DO_NOTHING)
    file = models.FileField(upload_to='media/diagnostics/', validators=[file_extension_validator])

    def __str__(self):
        return self.file.name
