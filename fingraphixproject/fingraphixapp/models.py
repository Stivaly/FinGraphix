from django.db import models
from django.core.exceptions import ValidationError


class Movimiento(models.Model):
    TIPO_MOVIMIENTO = [
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
    ]

    id = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=7, choices=TIPO_MOVIMIENTO)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField()
    descripcion = models.TextField()

    def clean(self):
        if self.monto is None:
            raise ValidationError("El monto no puede estar vacío.")
        try:
            int(self.monto)
        except ValueError:
            raise ValidationError("El monto debe ser un número entero válido.")
        if int(self.monto) <= 0:
            raise ValidationError("El monto debe ser mayor a 0.")
        if self.tipo is None or self.tipo == '':
            raise ValidationError("Por favor selecciona un tipo de movimiento.")
        elif self.tipo not in dict(self.TIPO_MOVIMIENTO).keys():
            raise ValidationError("Por favor selecciona un tipo de movimiento válido.")
        if self.descripcion is None or self.descripcion == '':
            raise ValidationError("Por favor ingresa una descripción.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def monto_formateado(self):
        return "${:,.2f}".format(self.monto)

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.monto} - {self.timestamp}"

    class Meta:
        db_table = 'movimiento'
