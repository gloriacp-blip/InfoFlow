"""
Vistas de la aplicación InfoFlow

Contiene las vistas para mostrar y gestionar categorías y recursos.
Incluye búsqueda, filtros, paginación y optimizaciones de rendimiento.

Autor: Tu Nombre
Fecha: 2024
"""

from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_http_methods
from django.contrib import messages

from .forms import CategoryForm, ResourceForm
from .models import Category, Resource


# ============================================================================
# VISTAS DEL DASHBOARD
# ============================================================================

def dashboard(request):
    """
    Vista principal del dashboard.
    
    Muestra un resumen de estadísticas, recursos recientes y permite
    búsqueda y filtrado rápido de recursos.
    
    Args:
        request: HttpRequest object
    
    Returns:
        HttpResponse con el template del dashboard
    """
    
    # Obtener parámetros de búsqueda y filtro
    query = request.GET.get("q", "").strip()
    category_id = request.GET.get("category", "").strip()
    status = request.GET.get("status", "").strip()
    
    # Inicializar queryset con select_related para evitar N+1 queries
    resources = Resource.objects.select_related("category")
    
    # Aplicar filtros de búsqueda
    if query:
        # Búsqueda en título y descripción (case-insensitive)
        resources = resources.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    
    # Filtrar por categoría si se especifica
    if category_id:
        resources = resources.filter(category_id=category_id)
    
    # Filtrar por estado si se especifica
    if status:
        resources = resources.filter(status=status)
    
    # Obtener estadísticas generales
    # Usando count() en lugar de len() para mejor rendimiento
    total_resources = Resource.objects.count()
    pending_resources = Resource.objects.filter(status="pendiente").count()
    reviewed_resources = Resource.objects.filter(status="revisado").count()
    important_resources = Resource.objects.filter(status="importante").count()
    
    # Obtener categorías con más recursos (top 5)
    category_summary = (
        Category.objects
        .annotate(total=Count("resources"))
        .order_by("-total", "name")[:5]
    )
    
    # Contexto para el template
    context = {
        "resources": resources[:5],  # Mostrar solo los 5 más recientes
        "categories": Category.objects.all(),
        "query": query,
        "category_id": category_id,
        "status": status,
        "total_resources": total_resources,
        "pending_resources": pending_resources,
        "reviewed_resources": reviewed_resources,
        "important_resources": important_resources,
        "category_summary": category_summary,
    }
    
    return render(request, "organizer/dashboard.html", context)


# ============================================================================
# VISTAS DE RECURSOS
# ============================================================================

def resource_list(request):
    """
    Vista para listar todos los recursos con búsqueda y filtros.
    
    Incluye paginación para mejorar rendimiento con muchos recursos.
    
    Args:
        request: HttpRequest object
    
    Returns:
        HttpResponse con la lista de recursos
    """
    
    # Obtener parámetros de búsqueda y filtro
    query = request.GET.get("q", "").strip()
    category_id = request.GET.get("category", "").strip()
    status = request.GET.get("status", "").strip()
    page = request.GET.get("page", 1)
    
    # Inicializar queryset con select_related para evitar N+1 queries
    resources = Resource.objects.select_related("category")
    
    # Aplicar filtros
    if query:
        resources = resources.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    
    if category_id:
        resources = resources.filter(category_id=category_id)
    
    if status:
        resources = resources.filter(status=status)
    
    # Implementar paginación (20 recursos por página)
    paginator = Paginator(resources, 20)
    
    try:
        resources_page = paginator.page(page)
    except PageNotAnInteger:
        # Si la página no es un entero, mostrar la primera página
        resources_page = paginator.page(1)
    except EmptyPage:
        # Si la página está fuera de rango, mostrar la última página
        resources_page = paginator.page(paginator.num_pages)
    
    context = {
        "resources": resources_page,
        "categories": Category.objects.all(),
        "query": query,
        "category_id": category_id,
        "status": status,
    }
    
    return render(request, "organizer/resource_list.html", context)


@require_http_methods(["GET", "POST"])
def resource_create(request):
    """
    Vista para crear un nuevo recurso.
    
    GET: Muestra el formulario vacío
    POST: Procesa el formulario y crea el recurso
    
    Args:
        request: HttpRequest object
    
    Returns:
        HttpResponse con el formulario o redirección a la lista
    """
    
    form = ResourceForm(request.POST or None)
    
    if request.method == "POST" and form.is_valid():
        # Guardar el nuevo recurso
        resource = form.save()
        
        # Mostrar mensaje de éxito
        messages.success(
            request,
            f"Recurso '{resource.title}' creado exitosamente."
        )
        
        return redirect("resource_list")
    
    context = {
        "form": form,
        "title": "Nuevo recurso",
        "action": "Crear",
    }
    
    return render(request, "organizer/resource_form.html", context)


@require_http_methods(["GET", "POST"])
def resource_update(request, pk):
    """
    Vista para editar un recurso existente.
    
    GET: Muestra el formulario con los datos actuales
    POST: Procesa el formulario y actualiza el recurso
    
    Args:
        request: HttpRequest object
        pk: Primary key del recurso a editar
    
    Returns:
        HttpResponse con el formulario o redirección a la lista
    """
    
    # Obtener el recurso o retornar 404 si no existe
    resource = get_object_or_404(Resource, pk=pk)
    
    form = ResourceForm(request.POST or None, instance=resource)
    
    if request.method == "POST" and form.is_valid():
        # Guardar los cambios
        resource = form.save()
        
        # Mostrar mensaje de éxito
        messages.success(
            request,
            f"Recurso '{resource.title}' actualizado exitosamente."
        )
        
        return redirect("resource_list")
    
    context = {
        "form": form,
        "title": "Editar recurso",
        "action": "Actualizar",
        "resource": resource,
    }
    
    return render(request, "organizer/resource_form.html", context)


@require_http_methods(["GET", "POST"])
def resource_delete(request, pk):
    """
    Vista para eliminar un recurso.
    
    GET: Muestra página de confirmación
    POST: Elimina el recurso
    
    Args:
        request: HttpRequest object
        pk: Primary key del recurso a eliminar
    
    Returns:
        HttpResponse con confirmación o redirección a la lista
    """
    
    # Obtener el recurso o retornar 404 si no existe
    resource = get_object_or_404(Resource, pk=pk)
    
    if request.method == "POST":
        # Guardar el título antes de eliminar
        resource_title = resource.title
        
        # Eliminar el recurso
        resource.delete()
        
        # Mostrar mensaje de éxito
        messages.success(
            request,
            f"Recurso '{resource_title}' eliminado exitosamente."
        )
        
        return redirect("resource_list")
    
    context = {"resource": resource}
    
    return render(request, "organizer/resource_confirm_delete.html", context)


# ============================================================================
# VISTAS DE CATEGORÍAS
# ============================================================================

def category_list(request):
    """
    Vista para listar todas las categorías con conteo de recursos.
    
    Args:
        request: HttpRequest object
    
    Returns:
        HttpResponse con la lista de categorías
    """
    
    # Usar annotate para contar recursos por categoría en una sola query
    categories = Category.objects.annotate(
        total_resources=Count("resources")
    ).order_by("name")
    
    context = {"categories": categories}
    
    return render(request, "organizer/category_list.html", context)


@require_http_methods(["GET", "POST"])
def category_create(request):
    """
    Vista para crear una nueva categoría.
    
    GET: Muestra el formulario vacío
    POST: Procesa el formulario y crea la categoría
    
    Args:
        request: HttpRequest object
    
    Returns:
        HttpResponse con el formulario o redirección a la lista
    """
    
    form = CategoryForm(request.POST or None)
    
    if request.method == "POST" and form.is_valid():
        # Guardar la nueva categoría
        category = form.save()
        
        # Mostrar mensaje de éxito
        messages.success(
            request,
            f"Categoría '{category.name}' creada exitosamente."
        )
        
        return redirect("category_list")
    
    context = {
        "form": form,
        "title": "Nueva categoría",
        "action": "Crear",
    }
    
    return render(request, "organizer/category_form.html", context)


@require_http_methods(["GET", "POST"])
def category_update(request, pk):
    """
    Vista para editar una categoría existente.
    
    GET: Muestra el formulario con los datos actuales
    POST: Procesa el formulario y actualiza la categoría
    
    Args:
        request: HttpRequest object
        pk: Primary key de la categoría a editar
    
    Returns:
        HttpResponse con el formulario o redirección a la lista
    """
    
    # Obtener la categoría o retornar 404 si no existe
    category = get_object_or_404(Category, pk=pk)
    
    form = CategoryForm(request.POST or None, instance=category)
    
    if request.method == "POST" and form.is_valid():
        # Guardar los cambios
        category = form.save()
        
        # Mostrar mensaje de éxito
        messages.success(
            request,
            f"Categoría '{category.name}' actualizada exitosamente."
        )
        
        return redirect("category_list")
    
    context = {
        "form": form,
        "title": "Editar categoría",
        "action": "Actualizar",
        "category": category,
    }
    
    return render(request, "organizer/category_form.html", context)


@require_http_methods(["GET", "POST"])
def category_delete(request, pk):
    """
    Vista para eliminar una categoría.
    
    GET: Muestra página de confirmación
    POST: Elimina la categoría
    
    Args:
        request: HttpRequest object
        pk: Primary key de la categoría a eliminar
    
    Returns:
        HttpResponse con confirmación o redirección a la lista
    """
    
    # Obtener la categoría o retornar 404 si no existe
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == "POST":
        # Guardar el nombre antes de eliminar
        category_name = category.name
        
        # Eliminar la categoría
        category.delete()
        
        # Mostrar mensaje de éxito
        messages.success(
            request,
            f"Categoría '{category_name}' eliminada exitosamente."
        )
        
        return redirect("category_list")
    
    context = {"category": category}
    
    return render(request, "organizer/category_confirm_delete.html", context)
