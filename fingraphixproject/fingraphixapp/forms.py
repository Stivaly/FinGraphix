from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Movimiento

class MovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = ['tipo', 'monto', 'descripcion'] 
        widgets = {
            'monto': forms.NumberInput(attrs={
                'class': 'form-control',
                'required': True,
                'oninvalid': (
                    "if (this.validity.typeMismatch || this.validity.badInput) {"
                    "    this.setCustomValidity('Por favor, ingresa solo números válidos.');"
                    "} else {"
                    "    this.setCustomValidity('Este campo es obligatorio.');"
                    "}"
                ),
                'oninput': "this.setCustomValidity('')",
                }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 2,
                'required': True,
                'oninvalid': "this.setCustomValidity('La descripción es obligatoria.')",
                'oninput': "this.setCustomValidity('')",
                }),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo'].choices = [('', 'Seleccionar tipo')] + list(Movimiento.TIPO_MOVIMIENTO)
        self.fields['tipo'].widget.attrs.update({
            'class': 'form-control',
            'required': True,
            'oninvalid': "this.setCustomValidity('Por favor selecciona un tipo válido.')",
            'oninput': "this.setCustomValidity('')",
            })
        
        self.fields['tipo'].widget.choices[0] = ('', 'Seleccionar tipo') 
    
    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        monto = cleaned_data.get('monto')
        descripcion = cleaned_data.get('descripcion')

        if monto is None:
            raise forms.ValidationError("El monto no puede estar vacío.")
        try:
            int(monto)  
        except ValueError:
            raise forms.ValidationError("El monto debe ser un número entero válido.")
        if int(monto) <= 0:
            raise forms.ValidationError("El monto debe ser mayor a 0.")
        if tipo is None or tipo == '':
            raise forms.ValidationError("Por favor selecciona un tipo de movimiento.")
        elif tipo not in dict(Movimiento.TIPO_MOVIMIENTO).keys():
            raise forms.ValidationError("Por favor selecciona un tipo de movimiento válido.")
        if descripcion is None or descripcion == '':
            raise forms.ValidationError("Por favor ingresa una descripción.")

        return cleaned_data

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Introduce una dirección de correo válida.")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')   
  