from django.shortcuts import render
import requests
from deep_translator import GoogleTranslator
from datetime import datetime
import calendar, locale
from django.views.generic import ListView, CreateView
from django.http import JsonResponse
from .forms import MovimientoForm, CustomUserCreationForm
from .models import Movimiento
from django.contrib import messages 
from django.urls import reverse_lazy
from .charts import get_ingresos_por_dia, get_salidas_por_dia, get_balance_por_mes
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from dotenv import load_dotenv

locale.setlocale(locale.LC_TIME, 'es_CL.UTF-8')
load_dotenv()

def get_current_month_context(request=None):
    now = datetime.now()
    year = now.year
    month = now.month
    if request:
        year = int(request.GET.get('year', year))
        month = int(request.GET.get('month', month))

    return {
        "current_month": calendar.month_name[month].capitalize(),
        "current_year": year,
        "current_month_number": month,
    }

class RegisterUserView(CreateView):
    template_name = 'registration/registration_form.html'  
    form_class = CustomUserCreationForm 
    success_url = reverse_lazy('login')

class MovimientoListView(ListView):
    model = Movimiento
    template_name = 'fingraphixapp/dashboard.html'
    context_object_name = 'movimientos'
    paginate_by = 15
    ordering = ['-timestamp']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_current_month_context())
        context["form"] = MovimientoForm()
        return context

class MovimientoCreateView(CreateView):
    model = Movimiento
    form_class = MovimientoForm
    template_name = 'fingraphixapp/movimiento_form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        messages.success(self.request, 'El movimiento se ha creado exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        errors = form.non_field_errors()
        if errors:
            messages.error(self.request, errors[1])
        else:
            messages.error(self.request, 'Hubo un error al crear el movimiento, contacte al administrador.')
        return super().form_invalid(form)


class DashboardView(LoginRequiredMixin, MovimientoListView):
    template_name = 'fingraphixapp/dashboard.html'
    success_url = reverse_lazy('dashboard')
    
    def get(self, request, *args, **kwargs):
        self.object = None
        self.object_list = self.get_queryset()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        list_context = super().get_context_data(**kwargs)
        create_context = {
            'form': MovimientoForm(),
        }
        context = {**list_context, **create_context, **get_current_month_context()}
        return context
   
def base(request):
    return render(request, 'fingraphixapp/index.html')

def analisis(request):
    data = get_current_month_context()
    return render(request, 'fingraphixapp/analisis.html', context=data)

def contacto(request):
    return render(request, 'fingraphixapp/contacto.html')

def datos_ingresos(request):
    context = get_current_month_context(request) 
    datos = get_ingresos_por_dia(context["current_year"], context["current_month_number"])
    return JsonResponse(datos)

def datos_egresos(request):
    context = get_current_month_context(request) 
    datos = get_salidas_por_dia(context["current_year"], context["current_month_number"])
    return JsonResponse(datos)

def balance(request):
    context = get_current_month_context(request) 
    datos = get_balance_por_mes(context["current_year"])
    return JsonResponse(datos)

@login_required
def mostrar_noticias(request):
    api_key = os.getenv("API_KEY")
    url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=" + api_key
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        noticias = response.json().get('articles', [])
        
        noticias_filtradas = [
            noticia for noticia in noticias
            if noticia['source']['name'] != "[Removed]"
            and noticia['title'] != "[Removed]"
            and noticia['description'] != "[Removed]"
        ]
        
        # Traducir las noticias
        translator = GoogleTranslator(source='auto', target='es')
        for noticia in noticias_filtradas:
            if 'title' in noticia:
                noticia['title'] = translator.translate(noticia['title'])
            if 'description' in noticia and noticia['description']:
                noticia['description'] = translator.translate(noticia['description'])

    except requests.exceptions.RequestException as e:
        noticias = []
        print(f"Error al consultar la API: {e}")

    return render(request, 'fingraphixapp/noticias.html', {'noticias': noticias_filtradas})

def logged_out(request):
    return render(request, 'registration/logged_out.html')

def test_form(request):
    form = MovimientoForm()
    return render(request, 'fingraphixapp/test_form.html', {'form': form})