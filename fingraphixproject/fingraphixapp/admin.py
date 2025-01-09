from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Movimiento

# Register your models here.
class MovimientoAdmin(admin.ModelAdmin):
    # Campos que se mostrarán en la lista del administrador
    list_display = ('id', 'tipo', 'monto', 'formato_24_horas', 'descripcion')
    
    def formato_24_horas(self, obj):
        return obj.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    formato_24_horas.short_description = 'timestamp'
    # Campos por los cuales se podrá buscar en el administrador
    search_fields = ('descripcion',)
    # Campos para aplicar filtros
    list_filter = ('tipo', 'timestamp')
    
admin.site.register(Movimiento, MovimientoAdmin)

