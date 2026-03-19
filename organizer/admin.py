"""
Configuración del panel de administración de Django para InfoFlow

Define cómo se muestran y gestionan los modelos en el panel admin.
Incluye filtros, búsqueda, acciones personalizadas y optimizaciones.

"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Resource


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Configuración del administrador para el modelo Category.
    
    Proporciona una interfaz mejorada para gestionar categorías
    con búsqueda, filtros y visualización personalizada.
    """
    
    # Campos que se muestran en la lista
    list_display = (
        "name",
        "slug",
        "resource_count",
        "created_at",
        "updated_at",
    )
    
    # Campos que permiten búsqueda
    search_fields = ("name", "description")
    
    # Campos que permiten filtrado
    list_filter = ("created_at", "updated_at")
    
    # Campos de solo lectura
    readonly_fields = ("slug", "created_at", "updated_at")
    
    # Ordenamiento por defecto
    ordering = ("name",)
    
    # Campos que se muestran al editar
    fieldsets = (
        ("Información Básica", {
            "fields": ("name", "slug", "description")
        }),
        ("Fechas", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )
    
    def resource_count(self, obj):
        """
        Muestra el conteo de recursos en la categoría.
        
        Args:
            obj: Instancia de Category
        
        Returns:
            str: HTML con el conteo formateado
        """
        count = obj.resources.count()
        color = "green" if count > 0 else "gray"
        return format_html(
            '<span style="color: {}; font-weight: bold;">{} recursos</span>',
            color,
            count
        )
    
    resource_count.short_description = "Recursos"


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    """
    Configuración del administrador para el modelo Resource.
    
    Proporciona una interfaz mejorada para gestionar recursos
    con búsqueda, filtros, acciones y visualización personalizada.
    """
    
    # Campos que se muestran en la lista
    list_display = (
        "title",
        "category",
        "status_badge",
        "priority_badge",
        "has_url",
        "created_at",
    )
    
    # Campos que permiten búsqueda
    search_fields = ("title", "description", "category__name")
    
    # Campos que permiten filtrado
    list_filter = (
        "status",
        "priority",
        "category",
        "created_at",
        "updated_at",
    )
    
    # Campos de solo lectura
    readonly_fields = (
        "slug",
        "created_at",
        "updated_at",
        "url_preview",
    )
    
    # Ordenamiento por defecto (más recientes primero)
    ordering = ("-created_at",)
    
    # Campos que se muestran al editar
    fieldsets = (
        ("Información Básica", {
            "fields": ("title", "slug", "description", "category")
        }),
        ("Detalles", {
            "fields": ("url", "url_preview", "status", "priority")
        }),
        ("Fechas", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )
    
    # Acciones personalizadas
    actions = [
        "mark_as_pending",
        "mark_as_reviewed",
        "mark_as_important",
        "set_priority_high",
        "set_priority_medium",
        "set_priority_low",
    ]
    
    def status_badge(self, obj):
        """
        Muestra el estado del recurso como un badge coloreado.
        
        Args:
            obj: Instancia de Resource
        
        Returns:
            str: HTML con el badge formateado
        """
        colors = {
            "pendiente": "#FFA500",    # Naranja
            "revisado": "#4CAF50",     # Verde
            "importante": "#F44336",   # Rojo
        }
        color = colors.get(obj.status, "#999999")
        
        return format_html(
            '<span style="background-color: {}; color: white; '
            'padding: 3px 8px; border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    
    status_badge.short_description = "Estado"
    
    def priority_badge(self, obj):
        """
        Muestra la prioridad del recurso como un badge coloreado.
        
        Args:
            obj: Instancia de Resource
        
        Returns:
            str: HTML con el badge formateado
        """
        colors = {
            "alta": "#F44336",      # Rojo
            "media": "#FFA500",     # Naranja
            "baja": "#4CAF50",      # Verde
        }
        color = colors.get(obj.priority, "#999999")
        
        return format_html(
            '<span style="background-color: {}; color: white; '
            'padding: 3px 8px; border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_priority_display()
        )
    
    priority_badge.short_description = "Prioridad"
    
    def has_url(self, obj):
        """
        Muestra si el recurso tiene una URL asociada.
        
        Args:
            obj: Instancia de Resource
        
        Returns:
            str: HTML con un icono o texto
        """
        if obj.url:
            return format_html(
                '<a href="{}" target="_blank" rel="noopener">🔗 Ver enlace</a>',
                obj.url
            )
        return format_html('<span style="color: gray;">Sin enlace</span>')
    
    has_url.short_description = "Enlace"
    
    def url_preview(self, obj):
        """
        Muestra una vista previa del URL.
        
        Args:
            obj: Instancia de Resource
        
        Returns:
            str: HTML con el URL o un mensaje
        """
        if obj.url:
            return format_html(
                '<a href="{}" target="_blank" rel="noopener">{}</a>',
                obj.url,
                obj.url
            )
        return "No hay URL asociada"
    
    url_preview.short_description = "Vista previa del enlace"
    
    # Acciones personalizadas
    
    def mark_as_pending(self, request, queryset):
        """Marca recursos como pendientes."""
        updated = queryset.update(status="pendiente")
        self.message_user(request, f"{updated} recurso(s) marcado(s) como pendiente.")
    
    mark_as_pending.short_description = "Marcar como pendiente"
    
    def mark_as_reviewed(self, request, queryset):
        """Marca recursos como revisados."""
        updated = queryset.update(status="revisado")
        self.message_user(request, f"{updated} recurso(s) marcado(s) como revisado.")
    
    mark_as_reviewed.short_description = "Marcar como revisado"
    
    def mark_as_important(self, request, queryset):
        """Marca recursos como importantes."""
        updated = queryset.update(status="importante")
        self.message_user(request, f"{updated} recurso(s) marcado(s) como importante.")
    
    mark_as_important.short_description = "Marcar como importante"
    
    def set_priority_high(self, request, queryset):
        """Establece prioridad alta."""
        updated = queryset.update(priority="alta")
        self.message_user(request, f"{updated} recurso(s) con prioridad alta.")
    
    set_priority_high.short_description = "Establecer prioridad alta"
    
    def set_priority_medium(self, request, queryset):
        """Establece prioridad media."""
        updated = queryset.update(priority="media")
        self.message_user(request, f"{updated} recurso(s) con prioridad media.")
    
    set_priority_medium.short_description = "Establecer prioridad media"
    
    def set_priority_low(self, request, queryset):
        """Establece prioridad baja."""
        updated = queryset.update(priority="baja")
        self.message_user(request, f"{updated} recurso(s) con prioridad baja.")
    
    set_priority_low.short_description = "Establecer prioridad baja"
