from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', views.base, name='base'),
    path('analisis/', views.analisis, name='analisis'),
    path('contacto/', views.contacto, name='contacto'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('movimiento/add/', views.MovimientoCreateView.as_view(), name='crear-movimiento'),
    path('test_form/', views.test_form, name='test_form'),
    path('api/datos-ingresos/', views.datos_ingresos, name='datos_ingresos'),
    path('api/datos-egresos/', views.datos_egresos, name='datos_egresos'),
    path('api/datos-balance/', views.balance, name='datos_balance'),
    path('noticias/', login_required(views.mostrar_noticias), name='mostrar_noticias'),
    # Add Django site authentication urls (for login, logout, password management)
    path('accounts/', include('django.contrib.auth.urls')),
    # urls para manejo de autenticación.
    path('accounts/register/', views.RegisterUserView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page='/logged_out/'), name='logout'),
    path('logged_out/', views.logged_out, name='logged_out'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
]
