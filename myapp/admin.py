import json
from django.contrib import admin
from django.forms import ValidationError
from import_export import resources
from myapp.models import Empresa, RequisitoLegal, EjecucionMatriz, RequisitosPorEmpresa, Plan, Pais, Industria, RequisitoPorEmpresaDetalle
from users_app.models import CustomUser, UserCompany # Add UserCompany here
from .utils import duplicate_requisitos_to_plan
from django.http import HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.urls import path, reverse
from django.shortcuts import render
from django.contrib import messages
from django.utils.html import format_html
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.contrib.admin import SimpleListFilter

# Import the correct model and classes for semantic_admin
from semantic_admin import SemanticModelAdmin, SemanticStackedInline, SemanticTabularInline
from semantic_admin.contrib.import_export.admin import SemanticImportExportModelAdmin
from import_export.admin import ImportExportModelAdmin

from .forms import CustomAdminLoginForm # Add this line
from django.core.exceptions import PermissionDenied 


def app_resort(func):
    def inner(*args, **kwargs):
        app_list = func(*args, **kwargs)
        app_sort_key = 'name'
        app_ordering = {
            "Gestion de Requisitos": 1,
            "Usuarios por Empresa": 2,
        }

        resorted_app_list = sorted(app_list, key=lambda x: app_ordering[x[app_sort_key]] if x[app_sort_key] in app_ordering else 1000)

        model_sort_key = 'object_name'
        model_ordering = {
            "Pais": 1,
            "Industria": 2,
            "Empresa": 3,
            "RequisitoLegal": 4,
            "RequisitosPorEmpresa": 5,
            "RequisitoPorEmpresaDetalle": 6,
            "Plan": 7,
            "EjecucionMatriz": 8,


        }
        for app in resorted_app_list:
            app['models'].sort(key=lambda x: model_ordering[x[model_sort_key]] if x[model_sort_key] in model_ordering else 1000)
        return resorted_app_list
    return inner


class UserCompanyInline(admin.TabularInline): #new class
    model = UserCompany
    extra = 1
    verbose_name = "Empresa del usuario"  # Correct label
    verbose_name_plural = "Empresas del usuario"  # Correct label (plural)
    fields = ('company',) # This is the line we need.
    
    
class YearPlanListFilter(admin.SimpleListFilter):
    title = 'Año'
    parameter_name = 'year'

    def lookups(self, request, model_admin):
        if request.user.is_superuser:
            years = Plan.objects.values_list('year', flat=True).distinct()
        elif request.selected_company:
            years = Plan.objects.filter(empresa=request.selected_company).values_list('year', flat=True).distinct()
        else:
            years = []
        return [(year, str(year)) for year in sorted(years)]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(year=self.value())
        return queryset

    def choices(self, changelist):
        all_choice = next(super().choices(changelist))
        yield all_choice
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == str(lookup),
                'query_string': changelist.get_query_string({self.parameter_name: lookup}),
                'display': title,
            }
  

##### inicio de resources para importar  ###################

class PaisResource(resources.ModelResource):
    class Meta:
        model = Pais
        import_id_fields = ('codigo',)


class IndustriaResource(resources.ModelResource):
    class Meta:
        model = Industria
        import_id_fields = ('nombre',)


class EmpresaResource(resources.ModelResource):
    class Meta:
        model = Empresa
        import_id_fields = ('codigoempresa',)


class RequisitoLegalResource(resources.ModelResource):
    class Meta:
        model = RequisitoLegal
        import_id_fields = ('id',)


class RequisitosPorEmpresaResource(resources.ModelResource):
    class Meta:
        model = RequisitosPorEmpresa
        import_id_fields = ('id',)


class RequisitoPorEmpresaDetalleResource(resources.ModelResource):
    class Meta:
        model = RequisitoPorEmpresaDetalle
        import_id_fields = ('matriz', 'requisito',)


class EjecucionMatrizResource(resources.ModelResource):
    class Meta:
        model = EjecucionMatriz
        import_id_fields = ('matriz', 'requisito',)


class PlanResource(resources.ModelResource):
    class Meta:
        model = Plan
        import_id_fields = ('id',)


class CustomUserResource(resources.ModelResource):
    class Meta:
        model = CustomUser
        import_id_fields = ('username')


##### fin de resources para importar  ###################

##### inicio creacion de classes para admin ###################

# new classes for filters ################################

class EmpresaRequisitoLegalListFilter(admin.SimpleListFilter):
    title = 'Requisito Legal'
    parameter_name = 'requisito'

    def lookups(self, request, model_admin):
        if request.user.is_superuser:
            queryset = RequisitoLegal.objects.all()
        elif request.selected_company: # New change
            queryset = RequisitoLegal.objects.filter(requisitoporempresadetalle__matriz__empresa=request.selected_company).distinct() # New Change
        else:
            queryset = RequisitoLegal.objects.none()
        return [(r.id, str(r)) for r in queryset]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(requisito__id=self.value())
        return queryset

class EmpresaRequisitosPorEmpresaListFilter(admin.SimpleListFilter):
    title = 'Requisito por Empresa'
    parameter_name = 'matriz'

    def lookups(self, request, model_admin):
        if request.user.is_superuser:
            queryset = RequisitosPorEmpresa.objects.all()
        elif request.selected_company: # New change
            queryset = RequisitosPorEmpresa.objects.filter(empresa=request.selected_company) # New change
        else:
            queryset = RequisitosPorEmpresa.objects.none() # New Change
        return [(r.id, str(r)) for r in queryset]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(matriz__id=self.value())
        return queryset
    
class EmpresaPlanListFilter(admin.SimpleListFilter):
    title = 'Plan'
    parameter_name = 'plan'

    def lookups(self, request, model_admin):
        if request.user.is_superuser:
            queryset = Plan.objects.all()
        elif request.selected_company: # New Change
            queryset = Plan.objects.filter(empresa=request.selected_company) # New Change
        else:
            queryset = Plan.objects.none()
        return [(r.id, str(r)) for r in queryset]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(plan__id=self.value())
        return queryset

class EmpresaPlanFilter(admin.SimpleListFilter):
    title = 'Empresa'
    parameter_name = 'empresa'

    def lookups(self, request, model_admin):
        if request.user.is_superuser:
            return [(e.codigoempresa, e.nombreempresa) for e in Empresa.objects.all()]
        elif request.selected_company: # New Change
            return [(request.selected_company.codigoempresa, request.selected_company.nombreempresa)] # New Change
        else:
            return []

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(empresa__codigoempresa=self.value())
        return queryset

class EmpresaRequisitoPorEmpresaDetalleListFilter(admin.SimpleListFilter):
    title = 'Requisito por Empresa'
    parameter_name = 'requisito_empresa'

    def lookups(self, request, model_admin):
        if request.user.is_superuser:
            return [(r.id, str(r)) for r in RequisitoPorEmpresaDetalle.objects.all()]
        elif request.selected_company: # New Change
            return [(r.id, str(r)) for r in RequisitoPorEmpresaDetalle.objects.filter(matriz__empresa=request.selected_company)] # New change
        else:
            return []

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(requisito_empresa__id=self.value())
        return queryset

# End of new classes for filters ###########################


class PaisAdmin(SemanticImportExportModelAdmin):
    resource_classes = [PaisResource]
    list_display = ('codigo', 'nombre')
    list_filter = ('codigo', 'nombre')
    search_fields = ('codigo', 'nombre')

    class Meta:
        verbose_name = " Pais "
        model = Pais


class IndustriaAdmin(SemanticImportExportModelAdmin):
    resource_classes = [IndustriaResource]
    list_display = ('nombre', 'descripcion')
    list_filter = ('nombre', 'descripcion')
    search_fields = ('nombre', 'descripcion')

    class Meta:
        verbose_name = " Industria "
        model = Industria


class EmpresaAdmin(SemanticImportExportModelAdmin):
    resource_classes = [EmpresaResource]
    list_display = ('codigoempresa', 'nombreempresa')
    list_filter = ('codigoempresa', 'nombreempresa')
    search_fields = ('codigoempresa', 'nombreempresa')

    class Meta:
        verbose_name = " Empresa "
        model = Empresa



class RequisitosLegalAdmin(SemanticImportExportModelAdmin):
    resource_classes = [RequisitoLegalResource]
    list_display = ('id', 'tema', 'entidad_que_emite' ,'jerarquia_de_la_norma' , 'numero', 'fecha', 'articulo_aplicable', 'Obligacion', 'pais' , 'industria', 'tiempo_validacion') # <-- Añadido aquí
    list_filter = ('tema', 'entidad_que_emite', 'tiempo_validacion') # <-- Añadido aquí (opcional)
    search_fields = ('tema', 'entidad_que_emite', 'tiempo_validacion') # <-- Añadido aquí (opcional, buscar en DurationField puede ser limitado)

    class Meta:
        verbose_name = " Requisito Legal "
        model = RequisitoLegal




class RequisitosPorEmpresaDetalleInline(SemanticTabularInline): # O SemanticStackedInline si prefieres esa vista
    """
    Inline para mostrar y editar los detalles de los requisitos asociados
    a una 'RequisitosPorEmpresa'.
    """
    model = RequisitoPorEmpresaDetalle
    extra = 1 # Número de formularios extra vacíos para añadir nuevos detalles
    # Especifica los campos a mostrar en el inline
    fields = (
        'requisito',
        'descripcion_cumplimiento',
        'periodicidad',
        'fecha_inicio',
        'tiempo_validacion', # Nuevo campo añadido
        'fecha_final'        # Nuevo campo calculado añadido
    )
    # Marca 'fecha_final' como de solo lectura, ya que se calcula automáticamente
    readonly_fields = ('fecha_final',)
    verbose_name = "Detalle de Requisito por Empresa"
    verbose_name_plural = "Detalles de Requisitos por Empresa"

class RequisitosPorEmpresaAdmin(SemanticImportExportModelAdmin):
    """
    Configuración del Admin para el modelo RequisitosPorEmpresa.
    Permite la gestión de las matrices de requisitos por empresa y
    la duplicación de requisitos a planes anuales.
    """
    resource_classes = [RequisitosPorEmpresaResource] # Para import/export
    list_display = ('id', 'get_empresa_nombre', 'nombre', 'descripcion', 'duplicate_link') # Usar método para nombre empresa
    list_filter = (EmpresaPlanFilter, 'nombre') # Usar filtro de empresa personalizado
    search_fields = ('empresa__nombreempresa', 'nombre', 'descripcion') # Buscar por nombre de empresa
    inlines = [RequisitosPorEmpresaDetalleInline] # Incluir el inline definido arriba

    def get_empresa_nombre(self, obj):
        """Método para mostrar el nombre de la empresa en list_display."""
        return obj.empresa.nombreempresa
    get_empresa_nombre.short_description = 'Empresa'
    get_empresa_nombre.admin_order_field = 'empresa__nombreempresa'

    # --- Funcionalidad de Duplicación ---
    def duplicate_to_plan(self, request):
        """
        Vista personalizada del admin para manejar la duplicación de requisitos
        de todas las matrices a los planes de un año específico.
        """
        if request.method == 'POST':
            target_year = request.POST.get('target_year')
            if target_year:
                try:
                    target_year = int(target_year)
                    # Llama a la función de utilidad que realiza la duplicación
                    # (Asegúrate que la función `duplicate_requisitos_to_plan` esté definida en utils.py)
                    duplicate_requisitos_to_plan(target_year)
                    messages.success(request, f'Requisitos duplicados al plan del año {target_year} exitosamente.')
                except ValueError:
                    messages.error(request, 'Año inválido. Debe ser un número entero.')
                except Exception as e:
                    messages.error(request, f'Error al duplicar: {e}')
            else:
                messages.error(request, 'Debe seleccionar un año de destino.')

            # Redirige de vuelta a la lista de RequisitosPorEmpresa después de la acción
            return HttpResponseRedirect(reverse('admin:myapp_requisitosporempresa_changelist'))

        # Contexto para renderizar la plantilla del formulario de duplicación
        context = dict(
           self.admin_site.each_context(request),
           opts=self.model._meta, # Pasa las opciones del modelo a la plantilla
           title="Duplicar Requisitos al Plan Anual" # Título para la página
        )
        # Renderiza la plantilla HTML que contiene el formulario para ingresar el año
        return render(request, 'admin/duplicate_to_plan.html', context)

    duplicate_to_plan.short_description = "Duplicar Todos los Requisitos al Plan Anual"

    def get_urls(self):
        """Añade la URL personalizada para la vista de duplicación."""
        urls = super().get_urls()
        custom_urls = [
            path(
                'duplicate_to_plan/',
                self.admin_site.admin_view(self.duplicate_to_plan),
                # Nombre único para la URL, incluyendo app_label y model_name
                name='myapp_requisitosporempresa_duplicate_to_plan',
            ),
        ]
        return custom_urls + urls

    def duplicate_link(self, obj):
        """
        Genera un enlace en la columna 'duplicate_link' de list_display
        para acceder a la vista de duplicación.
        Nota: Este enlace aparecerá en cada fila, pero la acción es global.
              Podría ser más intuitivo mover esto a las acciones globales del admin.
        """
        # Enlaza a la vista de duplicación general
        url = reverse('admin:myapp_requisitosporempresa_duplicate_to_plan')
        return format_html('<a href="{}">Iniciar Duplicación</a>', url)

    duplicate_link.short_description = "Acción Duplicar" # Nombre de la columna

    # --- Fin Funcionalidad de Duplicación ---

    class Meta:
        verbose_name = "Requisito Por Empresa" # Nombre singular
        verbose_name_plural = "Requisitos Por Empresa" # Nombre plural
        model = RequisitosPorEmpresa

class EjecucionMatrizAdmin(SemanticImportExportModelAdmin):
    resource_classes = [EjecucionMatrizResource]
    list_display = (
        'matriz', 'requisito', 'plan', 'porcentaje_cumplimiento', 'responsable', 'fecha_ejecucion', 'ejecucion',
        'get_conforme', 'get_next_compliance_date')
    list_filter = (
        EmpresaRequisitosPorEmpresaListFilter,
        EmpresaRequisitoLegalListFilter,
        EmpresaPlanListFilter,
        'ejecucion',
        'conforme',
        'porcentaje_cumplimiento',
        'fecha_ejecucion',
        )
    search_fields = (
        'matriz__nombre', 'requisito__tema', 'plan__empresa__nombreempresa', 'plan__periodicidad', 'responsable')
    
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['razon_no_conforme'].label = "Razon"
        return form
    
    
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'plan':
            kwargs['label'] = "Plan"
            if not request.user.is_superuser and request.selected_company: # Change this line
                kwargs['queryset'] = Plan.objects.filter(empresa=request.selected_company) #Change this line

        if db_field.name == 'matriz':
            kwargs['label'] = "Requisito por Empresa"
            if not request.user.is_superuser and request.selected_company: # Change this line
                kwargs['queryset'] = RequisitosPorEmpresa.objects.filter(empresa=request.selected_company) # Change this line
        
        if db_field.name == 'requisito':
            kwargs['label'] = "Requisito Legal"
            if not request.user.is_superuser and request.selected_company: # Change this line
                kwargs['queryset'] = RequisitoLegal.objects.filter(requisitoporempresadetalle__matriz__empresa=request.selected_company).distinct() # Change this line

            
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_next_compliance_date(self, obj):
        if obj.plan:
            return obj.plan.calculate_next_compliance_date()
        return None

    get_next_compliance_date.short_description = "Fecha Próximo Cumplimiento"
    get_next_compliance_date.admin_order_field = 'plan__fecha_proximo_cumplimiento'

    def get_conforme(self, obj):
        if obj.conforme == 'Si':
            return 'Sí'
        else:
            return 'No'

    get_conforme.short_description = 'Conforme'
    
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'conforme':
            kwargs['widget'] = admin.widgets.AdminRadioSelect(attrs={'class': 'ui'}) #change this line
        return super().formfield_for_dbfield(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.selected_company: # Change this line
            return qs.filter(plan__empresa=request.selected_company) #Change this line
        else:
            return qs.none()

    def save_model(self, request, obj, form, change):
        if obj.conforme == 'No' and (obj.razon_no_conforme is None or obj.razon_no_conforme.strip() == ''):
            print("Excepción capturada osvaldo check:")
            form_errors = {'razon_no_conforme': ["Si el resultado es 'No conforme', debe especificar una razón."]}
            first_error_message = " ".join(form_errors['razon_no_conforme'])
            raise PermissionDenied(first_error_message)
        try:
            super().save_model(request, obj, form, change)
        except Exception as e:
            print("Excepción general capturada:", e)
            raise PermissionDenied(f"An unexpected error occurred: {e}")

                 
    class Meta:
        verbose_name = " Ejecucion Del Plan "
        model = EjecucionMatriz

class PlanAdmin(SemanticImportExportModelAdmin):
    resource_classes = [PlanResource]
    list_display = ('get_id', 'empresa', 'get_requisito_empresa', 'periodicidad', 'fecha_inicio', 'fecha_proximo_cumplimiento', 'descripcion_periodicidad','get_year')
    list_filter = ( EmpresaPlanFilter,EmpresaRequisitoPorEmpresaDetalleListFilter, 'periodicidad', YearPlanListFilter)
    search_fields = ('empresa__nombreempresa', 'requisito_empresa__requisito__tema', 'periodicidad', 'descripcion_periodicidad')

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'year':
            kwargs['label'] = 'Año'

        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)
        return formfield

    def get_id(self, obj):
        return obj.id

    get_id.short_description = 'ID'  # Set the column header for id

    def get_requisito_empresa(self, obj):
        return obj.requisito_empresa

    get_requisito_empresa.short_description = 'Requisito Empresa' # Set the column header for requisito_empresa

    def get_year(self, obj):
        return obj.year

    get_year.short_description = 'Año'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.selected_company: # change this line
            return qs.filter(empresa=request.selected_company) # Change this line
        else:
            return qs.none()

    def save_model(self, request, obj, form, change):
        if obj.periodicidad == 'Unica' and not obj.fecha_proximo_cumplimiento:
            form_errors = {'fecha_proximo_cumplimiento': ["Si la periodicidad es 'Única', debe especificar una fecha de próximo cumplimiento."]}
            first_error_message = " ".join(form_errors['fecha_proximo_cumplimiento'])
            raise PermissionDenied(first_error_message)
        if obj.periodicidad == 'Otro' and not obj.descripcion_periodicidad:
            form_errors = {'descripcion_periodicidad': ["Si la periodicidad es 'Otro', debe especificar una descripción."]}
            first_error_message = " ".join(form_errors['descripcion_periodicidad'])
            raise PermissionDenied(first_error_message)
        try:
            super().save_model(request, obj, form, change)
        except Exception as e:
            print("Excepción general capturada:", e)
            raise PermissionDenied(f"An unexpected error occurred: {e}")



    class Meta:
        verbose_name = " Plan "
        model = Plan



        
class CustomUserAdmin(SemanticImportExportModelAdmin):
    resource_classes = [CustomUserResource]
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'get_empresa_name')  # I add get_empresa_name here
    list_filter = ('username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active')
    #filter_horizontal = ('Empresa',) #remove this line
    inlines = [UserCompanyInline] #Add this line

    def get_empresa_name(self, obj):
        return ", ".join([e.nombreempresa for e in obj.Empresa.all()])

    get_empresa_name.short_description = 'Empresa'

    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)

    # def save_related(self, request, form, formsets, change): #remove this function
    #     # Call super to save M2M relations that do not need to be on our table
    #     super().save_related(request, form, formsets, change)
    #     #delete all registers for recreate the values.
    #     UserCompany.objects.filter(user=form.instance).delete()
    #     # Iterate through the selected companies and create UserCompany instances
    #     for company in form.cleaned_data['Empresa']:
    #         UserCompany.objects.create(user=form.instance, company=company)

    class Meta:
        verbose_name = " Usuarios Empresa "
        model = CustomUser


        
##### fin prepracion de clases para el admin  #######


admin.site.site_header = "Framework SAS"
admin.site.site_title = "Framework SAS"
admin.site.index_title = "Framework SAS"
admin.site.login_form = CustomAdminLoginForm # Add this line



admin.site.register(Pais, PaisAdmin)
admin.site.register(Industria, IndustriaAdmin)
admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(RequisitoLegal, RequisitosLegalAdmin)
admin.site.register(RequisitosPorEmpresa, RequisitosPorEmpresaAdmin)  # Renamed from MatrizEmpresa
admin.site.register(EjecucionMatriz, EjecucionMatrizAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Plan, PlanAdmin)

admin.site.get_app_list = app_resort(admin.site.get_app_list)

