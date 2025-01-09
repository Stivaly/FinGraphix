import os
import django
from faker import Faker
import random
from decimal import Decimal
from datetime import datetime
from fingraphixapp.models import Movimiento  # Cambia "fingraphixapp" por el nombre de tu aplicación

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fingraphixproject.settings')  # Cambia "fingraphixproject" por el nombre de tu proyecto
django.setup()

# Crear instancia de Faker
fake = Faker()

# Opciones para el campo 'tipo'
TIPOS = ['entrada', 'salida']

# Función para poblar datos
def populate(n=10):
    for _ in range(n):
        tipo = random.choice(TIPOS)
        monto = Decimal(random.randint(2001, 100000)).quantize(Decimal('0.00'))
        descripcion = fake.sentence(nb_words=6)  # Generar una descripción falsa
        start_date = datetime(datetime.now().year, 11, 1)
        end_date = datetime(datetime.now().year, 11, 30, 23, 59, 59)
        timestamp = fake.date_time_between(start_date=start_date, end_date=end_date)

        # Crear un movimiento en la base de datos
        Movimiento.objects.create(
            tipo=tipo,
            monto=monto,
            timestamp=timestamp,
            descripcion=descripcion,
        )

    print(f"Se han creado {n} movimientos financieros.")


