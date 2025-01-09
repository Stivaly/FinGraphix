from django.db.models.functions import TruncDay, TruncMonth
from django.db.models import Sum
from .models import Movimiento

def get_ingresos_por_dia(year, month):
    movimientos = Movimiento.objects.filter(
        timestamp__year=year,
        timestamp__month=month,
        tipo="entrada"
    )
    ingresos_por_dia = (
        movimientos.annotate(date=TruncDay("timestamp"))
        .values("date")
        .annotate(total=Sum("monto"))
        .order_by("date")
    )
    categorias = [ingreso["date"].strftime("%d-%b") for ingreso in ingresos_por_dia]
    datos = [float(ingreso["total"]) for ingreso in ingresos_por_dia]
    return {"categorias": categorias, "datos": datos}

def get_salidas_por_dia(year, month):
    movimientos = Movimiento.objects.filter(
        timestamp__year=year,
        timestamp__month=month,
        tipo="salida"
    )
    salidas_por_dia = (
        movimientos.annotate(date=TruncDay("timestamp"))
        .values("date")
        .annotate(total=Sum("monto"))
        .order_by("date")
    )
    categorias = [salida["date"].strftime("%d-%b") for salida in salidas_por_dia]
    datos = [float(salida["total"]) for salida in salidas_por_dia]
    return {"categorias": categorias, "datos": datos}

def get_balance_por_mes(year):
    # Obtener ingresos agrupados por mes
    ingresos = Movimiento.objects.filter(
        timestamp__year=year,
        tipo="entrada"
    ).annotate(month=TruncMonth("timestamp")).values("month").annotate(total=Sum("monto"))

    # Obtener salidas agrupadas por mes
    salidas = Movimiento.objects.filter(
        timestamp__year=year,
        tipo="salida"
    ).annotate(month=TruncMonth("timestamp")).values("month").annotate(total=Sum("monto"))

    # Calcular el balance por mes
    balance = {}
    for ingreso in ingresos:
        balance[ingreso["month"]] = float(ingreso["total"])
    for salida in salidas:
        balance[salida["month"]] = balance.get(salida["month"], 0) - float(salida["total"])

    # Crear listas de categorías y datos
    categorias = [month.strftime("%b") for month in sorted(balance.keys())]  # Nombres de los meses
    datos = [balance[month] for month in sorted(balance.keys())]  # Balance mensual
    return {"categorias": categorias, "datos": datos}
