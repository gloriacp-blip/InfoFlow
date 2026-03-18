"""
Formularios de la aplicación InfoFlow

Define los formularios para crear y editar categorías y recursos.
Incluye validaciones personalizadas y widgets mejorados.

Autor: Tu Nombre
Fecha: 2024
"""

from django import forms
from django.core.exceptions import ValidationError
from .models import Category, Resource


class CategoryForm(forms.ModelForm):
    """
    Formulario para crear y editar categorías.
    
    Valida que el nombre sea único y no esté vacío.
    """
    
    class Meta:
        model = Category
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ej: Python, Diseño, Marketing",
                    "maxlength": "100",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Describe brevemente el contenido de esta categoría",
                }
            ),
        }
    
    def clean_name(self):
        """
        Valida que el nombre de la categoría sea válido.
        
        Returns:
            str: El nombre limpio y validado
        
        Raises:
            ValidationError: Si el nombre está vacío o es muy corto
        """
        name = (self.cleaned_data.get("name") or "").strip()
        
        # Validar que no esté vacío
        if not name:
            raise ValidationError("El nombre de la categoría no puede estar vacío.")
        
        # Validar longitud mínima
        if len(name) < 2:
            raise ValidationError("El nombre debe tener al menos 2 caracteres.")
        
        # Validar que no contenga solo números
        if name.isdigit():
            raise ValidationError("El nombre no puede contener solo números.")
        
        return name
    
    def clean_description(self):
        """
        Valida la descripción de la categoría.
        
        Returns:
            str: La descripción limpia y validada
        """
        description = (self.cleaned_data.get("description") or "").strip()
        
        # Validar longitud máxima
        if len(description) > 500:
            raise ValidationError("La descripción no puede exceder 500 caracteres.")
        
        return description


class ResourceForm(forms.ModelForm):
    """
    Formulario para crear y editar recursos.
    
    Valida que los campos requeridos estén completos y sean válidos.
    Incluye validación de URLs y longitud de texto.
    """
    
    class Meta:
        model = Resource
        fields = ["title", "description", "url", "category", "status", "priority"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Título descriptivo del recurso",
                    "maxlength": "150",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Describe el contenido y por qué es importante este recurso",
                }
            ),
            "url": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://ejemplo.com (opcional)",
                }
            ),
            "category": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "status": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "priority": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }
    
    def clean_title(self):
        """
        Valida el título del recurso.
        
        Returns:
            str: El título limpio y validado
        
        Raises:
            ValidationError: Si el título es inválido
        """
        title = (self.cleaned_data.get("title") or "").strip()
        
        # Validar que no esté vacío
        if not title:
            raise ValidationError("El título del recurso no puede estar vacío.")
        
        # Validar longitud mínima
        if len(title) < 3:
            raise ValidationError("El título debe tener al menos 3 caracteres.")
        
        # Validar que no contenga solo números
        if title.isdigit():
            raise ValidationError("El título no puede contener solo números.")
        
        return title
    
    def clean_description(self):
        """
        Valida la descripción del recurso.
        
        Returns:
            str: La descripción limpia y validada
        
        Raises:
            ValidationError: Si la descripción es inválida
        """
        description = (self.cleaned_data.get("description") or "").strip()
        
        # Validar que no esté vacío
        if not description:
            raise ValidationError("La descripción del recurso no puede estar vacía.")
        
        # Validar longitud mínima
        if len(description) < 10:
            raise ValidationError(
                "La descripción debe tener al menos 10 caracteres."
            )
        
        # Validar longitud máxima
        if len(description) > 2000:
            raise ValidationError(
                "La descripción no puede exceder 2000 caracteres."
            )
        
        return description
    
    def clean_url(self):
        """
        Valida la URL del recurso (si se proporciona).
        
        Returns:
            str: La URL validada o vacío si no se proporciona
        
        Raises:
            ValidationError: Si la URL es inválida
        """
        url = (self.cleaned_data.get("url") or "").strip()
        
        # Si no hay URL, es válido (es opcional)
        if not url:
            return ""
        
        # Validar que la URL comience con http:// o https://
        if not url.startswith(("http://", "https://")):
            raise ValidationError(
                "La URL debe comenzar con http:// o https://"
            )
        
        return url
    
    def clean(self):
        """
        Validaciones adicionales del formulario.
        
        Returns:
            dict: Los datos limpios del formulario
        
        Raises:
            ValidationError: Si hay errores de validación
        """
        cleaned_data = super().clean()
        
        # Validar que se haya seleccionado una categoría
        category = cleaned_data.get("category")
        if not category:
            raise ValidationError("Debe seleccionar una categoría.")
        
        # Validar que se haya seleccionado un estado
        status = cleaned_data.get("status")
        if not status:
            raise ValidationError("Debe seleccionar un estado.")
        
        # Validar que se haya seleccionado una prioridad
        priority = cleaned_data.get("priority")
        if not priority:
            raise ValidationError("Debe seleccionar una prioridad.")
        
        return cleaned_data
