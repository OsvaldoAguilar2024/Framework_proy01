# Create your models here.

from django.db import models
from django.forms import ValidationError
from django.contrib.auth.models import User
from datetime import date, timedelta
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone


# ... your existing code ...

class Pais(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    codigo = models.CharField(max_length=5, unique=True)  # Optional: ISO country code

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Pais"
        verbose_name_plural = "Paises"



class Industria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Industria"
        verbose_name_plural = "Industrias"


class Empresa(models.Model):
    codigoempresa = models.CharField(max_length = 50, primary_key=True ,  blank=False,  null=False , default="")  
    nombreempresa = models.CharField(max_length= 150 , blank=False,  null=False , default="")  
    direccion = models.CharField(max_length=200, blank=False, null=False, default="")
    telefono = models.CharField(max_length=20, blank=True, null=True, default="")
    email = models.EmailField(blank=True, null=True)
    logo = models.ImageField(upload_to='', blank=True, null=True)
    activo = models.BooleanField(default=True)  
     
    def clean(self):
        # Verificar que el código de cuenta no se repita
        if self.codigoempresa in self.__class__.objects.values_list('codigoempresa'):
            raise ValidationError("El código de empresa ya está en uso")

    def __str__(self):
        return self.nombreempresa

     
    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"   

class RequisitoLegal(models.Model):
    TIPO_REQUISITO_CHOICES = [
        ('Local', 'Local'),
        ('Externo', 'Externo'),
        ('Ambos', 'Ambos'),
    ]
  
    id = models.AutoField(primary_key=True)
    tema = models.CharField(max_length=50)
    entidad_que_emite = models.CharField(max_length=255)
    jerarquia_de_la_norma = models.CharField(max_length=255)
    numero = models.CharField(max_length=50)
    fecha = models.DateField()
    tiempo_validacion = models.DurationField(
        null=True,  # Permite que el campo sea nulo en la base de datos
        blank=True, # Permite que el campo esté vacío en formularios
        verbose_name="Tiempo de Validación",
        help_text="Tiempo estimado o requerido para validar el cumplimiento del requisito (ej. '30 days', '6 months')."
    )
    articulo_aplicable = models.TextField()
    Obligacion = models.TextField()
    proceso_que_aplica = models.CharField(max_length=255)
    tipo_requisito = models.CharField(
        max_length=10,
        choices=TIPO_REQUISITO_CHOICES,
        default='Local'
    )
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE, null=True)  # New field
    industria = models.ForeignKey(Industria, on_delete=models.CASCADE, null=True)  # New field




    def __str__(self):
        return f"{self.tema} - {self.entidad_que_emite} - {self.jerarquia_de_la_norma} "

    class Meta:
        verbose_name = "Requisito Legal"
        verbose_name_plural = "Requisitos Legales"

class RequisitosPorEmpresa(models.Model): # Renamed from MatrizEmpresa
    id = models.AutoField(primary_key=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, to_field='codigoempresa')
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.empresa.nombreempresa}"


     
    class Meta:
        verbose_name = "Requisitos Por Empresa" # Renamed from MatrizEmpresa
        verbose_name_plural = "Requisitos Por Empresa" # Renamed from MatricesEmpresa
           

class RequisitoPorEmpresaDetalle(models.Model):
    PERIODICIDAD_CHOICES = [
        ('Diaria', 'Diaria'),
        ('Semanal', 'Semanal'),
        ('Quincenal', 'Quincenal'),
        ('Mensual', 'Mensual'),
        ('Bimestral', 'Bimestral'),
        ('Trimestral', 'Trimestral'),
        ('Semestral', 'Semestral'),
        ('Anual', 'Anual'),
        ('Unica', 'Única'),
        ('Otro', 'Otro')
    ]

    matriz = models.ForeignKey(RequisitosPorEmpresa, on_delete=models.CASCADE)
    requisito = models.ForeignKey(RequisitoLegal, on_delete=models.CASCADE)
    descripcion_cumplimiento = models.TextField(blank=True, null=True)
    periodicidad = models.CharField(
        max_length=20,
        choices=PERIODICIDAD_CHOICES,
        default='Mensual'
    )
    
    fecha_inicio = models.DateField(blank=False, null=False, default=timezone.now) # Usar timezone.now es mejor práctica

    # --- NUEVO CAMPO TIEMPO VALIDACION ---
    tiempo_validacion = models.DurationField(
        null=True,
        blank=True,
        verbose_name="Tiempo de Validación",
        help_text="Tiempo estimado o requerido para validar el cumplimiento del requisito (ej. '30 days', '6 months'). Se usará para calcular la Fecha Final."
    )
    # --- FIN NUEVO CAMPO TIEMPO VALIDACION ---

    # --- NUEVO CAMPO FECHA FINAL (CALCULADO) ---
    fecha_final = models.DateField(
        null=True,
        blank=True, # Permitir blank=True ya que se calcula en save()
        verbose_name="Fecha Final Estimada",
        help_text="Fecha calculada automáticamente basada en la Fecha de Inicio y el Tiempo de Validación.",
        editable=False # Hacerlo no editable en el admin, ya que se calcula
    )
    # --- FIN NUEVO CAMPO FECHA FINAL ---


    def __str__(self):
        return f"{self.matriz.nombre} - {self.requisito.tema}"

    def save(self, *args, **kwargs):
        # Calcular fecha_final antes de guardar
        if self.fecha_inicio and self.tiempo_validacion:
            try:
                # Asegurarse de que fecha_inicio es un objeto date
                if isinstance(self.fecha_inicio, str):
                     self.fecha_inicio = date.fromisoformat(self.fecha_inicio)
                # Asegurarse de que tiempo_validacion es un timedelta
                if isinstance(self.tiempo_validacion, str):
                     # Django puede necesitar ayuda para parsear strings a timedelta a veces
                     # Esta es una forma simple, puede necesitar ajustes según el formato exacto
                     # que esperes del input string.
                     # Por ahora, asumimos que Django lo maneja bien o viene como timedelta.
                     pass # Asumiendo que Django lo convierte o ya es timedelta

                self.fecha_final = self.fecha_inicio + self.tiempo_validacion
            except (TypeError, ValueError) as e:
                # Manejar posible error si los tipos no son compatibles o el formato es incorrecto
                print(f"Error calculating fecha_final: {e}") # Loggear el error
                self.fecha_final = None # Dejar como None si hay error
        else:
            self.fecha_final = None # Si falta fecha_inicio o tiempo_validacion, fecha_final es None

        super().save(*args, **kwargs) # Llamar al método save original

    class Meta:
        unique_together = ('matriz', 'requisito')
        verbose_name = "Requisito Por Empresa Detalle"
        verbose_name_plural = "Requisitos Por Empresa Detalle"


class Plan(models.Model):
    PERIODICIDAD_CHOICES = [
        ('Diaria', 'Diaria'),
        ('Semanal', 'Semanal'),
        ('Quincenal', 'Quincenal'),
        ('Mensual', 'Mensual'),
        ('Bimestral', 'Bimestral'),
        ('Trimestral', 'Trimestral'),
        ('Semestral', 'Semestral'),
        ('Anual', 'Anual'),
        ('Unica', 'Única'),  # For one-time requirements
        ('Otro', 'Otro')  # in case you want to add a free text
    ]
    id = models.AutoField(primary_key=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, to_field='codigoempresa')
    requisito_empresa = models.ForeignKey(RequisitoPorEmpresaDetalle, on_delete=models.CASCADE) #Renamed from RequisitosPorEmpresa
    periodicidad = models.CharField(
        max_length=20,
        choices=PERIODICIDAD_CHOICES,
        default='Mensual'
    )
    fecha_inicio = models.DateField(blank=False, null=False, default=date.today)
    fecha_proximo_cumplimiento = models.DateField(blank=True, null=True)
    descripcion_periodicidad = models.TextField(blank=True, null=True)
    year = models.PositiveIntegerField()  # Add the field year
    def __str__(self):
        return f"Plan {self.year} para {self.empresa.nombreempresa} - {self.requisito_empresa.requisito.tema} - {self.periodicidad}"

    def clean(self):
        errors = {}
        # if the periodicity is Unica, and the next date is not completed.
        if self.periodicidad == 'Unica' and not self.fecha_proximo_cumplimiento:
            errors['fecha_proximo_cumplimiento'] = ["Si la periodicidad es 'Única', debe especificar una fecha de próximo cumplimiento."]
        # if the periodicity is Other, and the description is not completed.
        if self.periodicidad == 'Otro' and not self.descripcion_periodicidad:
            errors['descripcion_periodicidad'] = ["Si la periodicidad es 'Otro', debe especificar una descripción."]
        if errors:
            raise ValidationError(errors)
    def save(self, *args, **kwargs):
        if self.periodicidad != 'Unica':
            self.fecha_proximo_cumplimiento = self.calculate_next_compliance_date()

        super().save(*args, **kwargs)
        
    def calculate_next_compliance_date(self):
        if self.periodicidad == 'Unica':
            return self.fecha_proximo_cumplimiento

        base_date = self.fecha_inicio

        if self.periodicidad == 'Diaria':
            next_date = base_date + timedelta(days=1)
        elif self.periodicidad == 'Semanal':
            next_date = base_date + timedelta(weeks=1)
        elif self.periodicidad == 'Quincenal':
            next_date = base_date + timedelta(weeks=2)
        elif self.periodicidad == 'Mensual':
            next_date = base_date + timedelta(days=30)
        elif self.periodicidad == 'Bimestral':
            next_date = base_date + timedelta(days=60)
        elif self.periodicidad == 'Trimestral':
            next_date = base_date + timedelta(days=90)
        elif self.periodicidad == 'Semestral':
            next_date = base_date + timedelta(days=180)
        elif self.periodicidad == 'Anual':
            next_date = base_date + timedelta(days=365)
        else:
            return None
        return next_date

    class Meta:
        verbose_name = "Plan"
        verbose_name_plural = "Planes"


class EjecucionMatriz(models.Model):
    matriz = models.ForeignKey(RequisitosPorEmpresa, on_delete=models.CASCADE) #Renamed from MatrizEmpresa
    requisito = models.ForeignKey(RequisitoLegal, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, blank=True, null=True)
    porcentaje_cumplimiento = models.IntegerField(default=0,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ]
    )
    evidencia_cumplimiento = models.FileField(upload_to='evidencia_legal/', blank=True, null=True)
    responsable = models.CharField(max_length=255, blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    fecha_ejecucion = models.DateField(blank=True, null=True)  # Actual date of execution
    resultado_evaluacion = models.TextField(blank=True, null=True)
    ejecucion = models.BooleanField(default=False)  # Yes or No
    CONFORME_CHOICES = [
        ('Si', 'Sí'),
        ('No', 'No'),
    ]
    conforme = models.CharField(max_length=2, choices=CONFORME_CHOICES, default='No')
    razon_no_conforme = models.TextField(
        blank=False,
        null=False,
        default='.',
        error_messages={'required': "Por favor, ingrese una razón."}
        )

    def __str__(self):
        return f"{self.matriz.nombre} - {self.requisito.tema} - {self.plan.year if self.plan else ''}"

    def save(self, *args, **kwargs):
        errors = {}

        # If the execution is being done, it updates the date.
        if self.porcentaje_cumplimiento > 0:
            self.fecha_ejecucion = date.today()
        if self.conforme == 'Si':
           self.razon_no_conforme = "."
        if self.conforme == 'No' and (self.razon_no_conforme is None or self.razon_no_conforme.strip() == ''):
            errors['razon_no_conforme'] = ["Si el resultado es 'No conforme', debe especificar una razón."]
        if errors:
            raise ValidationError(errors)
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('matriz', 'requisito', 'plan')  # each plan can have only one matrix
        verbose_name = "Ejecucion del Plan"
        verbose_name_plural = "Ejecucion de los Planes"



