from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True, verbose_name="Nombre")),
                ("description", models.TextField(blank=True, verbose_name="Descripción")),
            ],
            options={"ordering": ["name"], "verbose_name": "Categoría", "verbose_name_plural": "Categorías"},
        ),
        migrations.CreateModel(
            name="Resource",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=150, verbose_name="Título")),
                ("description", models.TextField(verbose_name="Descripción")),
                ("url", models.URLField(blank=True, verbose_name="Enlace")),
                ("status", models.CharField(choices=[("pendiente","Pendiente"),("revisado","Revisado"),("importante","Importante")], default="pendiente", max_length=20, verbose_name="Estado")),
                ("priority", models.CharField(choices=[("alta","Alta"),("media","Media"),("baja","Baja")], default="media", max_length=10, verbose_name="Prioridad")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")),
                ("category", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="resources", to="organizer.category", verbose_name="Categoría")),
            ],
            options={"ordering": ["-created_at"], "verbose_name": "Recurso", "verbose_name_plural": "Recursos"},
        ),
    ]
