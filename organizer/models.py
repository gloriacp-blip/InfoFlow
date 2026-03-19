"""
Modelos de la aplicación InfoFlow

Define la estructura de datos para categorías y recursos digitales.
Incluye validaciones, índices de base de datos y métodos útiles.

"""

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.utils import timezone


class Category(models.Model):
    """
    Modelo para categorizar recursos digitales.
    
    Permite organizar recursos por temas o áreas de interés.
    Cada categoría puede contener múltiples recursos.
    """
    
    name = models.CharField(
        "Nombre",
        max_length=100,
        unique=True,
        help_text="Nombre único de la categoría"
    )
    
    slug = models.SlugField(
        unique=True,
        blank=True,
        help_text="URL-friendly version del nombre (generado automáticamente)"
    )
    
    description = models.TextField(
        "Descripción",
        blank=True,
        help_text="Descripción detallada de la categoría"
    )
    
    created_at = models.DateTimeField(
        "Fecha de creación",
        auto_now_add=True
    )
    
    updated_at = models.DateTimeField(
        "Fecha de actualización",
        auto_now=True
    )
    
    class Meta:
        ordering = ["name"]
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        # Índices para mejorar rendimiento en búsquedas
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["slug"]),
        ]
    
    def __str__(self):
        """Retorna el nombre de la categoría."""
        return self.name
    
    def save(self, *args, **kwargs):
        """
        Sobrescribe el método save para generar automáticamente el slug.
        El slug se utiliza en URLs amigables.
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_resource_count(self):
        """Retorna la cantidad de recursos en esta categoría."""
        return self.resources.count()
    
    def get_resources_by_priority(self, priority):
        """
        Retorna recursos de esta categoría filtrados por prioridad.
        
        Args:
            priority: Una de las opciones de prioridad (alta, media, baja)
        
        Returns:
            QuerySet de recursos filtrados
        """
        return self.resources.filter(priority=priority)


class Resource(models.Model):
    """
    Modelo para recursos digitales (enlaces, documentos, referencias).
    
    Representa un recurso que puede ser un enlace, documento o referencia
    que el usuario desea organizar y seguir.
    """
    
    # Opciones de estado del recurso
    STATUS_CHOICES = [
        ("pendiente", "Pendiente"),
        ("revisado", "Revisado"),
        ("importante", "Importante"),
    ]
    
    # Opciones de prioridad del recurso
    PRIORITY_CHOICES = [
        ("alta", "Alta"),
        ("media", "Media"),
        ("baja", "Baja"),
    ]
    
    title = models.CharField(
        "Título",
        max_length=150,
        help_text="Título descriptivo del recurso"
    )
    
    slug = models.SlugField(
        unique=True,
        blank=True,
        help_text="URL-friendly version del título"
    )
    
    description = models.TextField(
        "Descripción",
        help_text="Descripción detallada del recurso"
    )
    
    url = models.URLField(
        "Enlace",
        blank=True,
        null=True,
        help_text="URL del recurso (opcional)"
    )
    
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="resources",
        verbose_name="Categoría",
        help_text="Categoría a la que pertenece este recurso"
    )
    
    status = models.CharField(
        "Estado",
        max_length=20,
        choices=STATUS_CHOICES,
        default="pendiente",
        help_text="Estado actual del recurso"
    )
    
    priority = models.CharField(
        "Prioridad",
        max_length=10,
        choices=PRIORITY_CHOICES,
        default="media",
        help_text="Nivel de prioridad del recurso"
    )
    
    created_at = models.DateTimeField(
        "Fecha de creación",
        auto_now_add=True
    )
    
    updated_at = models.DateTimeField(
        "Fecha de actualización",
        auto_now=True
    )
    
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Recurso"
        verbose_name_plural = "Recursos"
        # Índices para optimizar búsquedas comunes
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["status"]),
            models.Index(fields=["priority"]),
            models.Index(fields=["category"]),
            models.Index(fields=["-created_at"]),
        ]
    
    def __str__(self):
        """Retorna el título del recurso."""
        return self.title
    
    def save(self, *args, **kwargs):
        """
        Sobrescribe el método save para:
        1. Generar automáticamente el slug
        2. Validar que el URL sea válido si se proporciona
        """
        if not self.slug:
            self.slug = slugify(self.title)
        
        self.full_clean()  # Ejecuta validaciones del modelo
        super().save(*args, **kwargs)
    
    def clean(self):
        """
        Validaciones personalizadas del modelo.
        Se ejecuta cuando se llama a full_clean() o save().
        """
        # Validar que el título no esté vacío
        if not self.title or not self.title.strip():
            raise ValidationError("El título no puede estar vacío")
        
        # Validar que la descripción no esté vacía
        if not self.description or not self.description.strip():
            raise ValidationError("La descripción no puede estar vacía")
    
    def is_recent(self):
        """
        Verifica si el recurso fue creado en los últimos 7 días.
        
        Returns:
            bool: True si el recurso es reciente, False en caso contrario
        """
        days_ago = timezone.now() - timezone.timedelta(days=7)
        return self.created_at >= days_ago
    
    def is_high_priority(self):
        """
        Verifica si el recurso tiene prioridad alta.
        
        Returns:
            bool: True si la prioridad es alta, False en caso contrario
        """
        return self.priority == "alta"
    
    def get_status_badge_color(self):
        """
        Retorna el color del badge según el estado del recurso.
        Útil para mostrar visualmente el estado en templates.
        
        Returns:
            str: Clase CSS para el color del badge
        """
        status_colors = {
            "pendiente": "badge-warning",
            "revisado": "badge-info",
            "importante": "badge-danger",
        }
        return status_colors.get(self.status, "badge-secondary")
    
    def get_priority_badge_color(self):
        """
        Retorna el color del badge según la prioridad del recurso.
        
        Returns:
            str: Clase CSS para el color del badge
        """
        priority_colors = {
            "alta": "badge-danger",
            "media": "badge-warning",
            "baja": "badge-success",
        }
        return priority_colors.get(self.priority, "badge-secondary")
