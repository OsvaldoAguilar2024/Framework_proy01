# myapp/utils.py

from .models import RequisitoPorEmpresaDetalle, Plan, Empresa
from django.forms import ValidationError
from datetime import date
def duplicate_requisitos_to_plan(target_year, company_id=None):
    """
    Duplicates RequisitoPorEmpresaDetalle records into the Plan model for a specific year.

    Args:
        target_year (int): The year for which to create new Plan records.
        company_id (str, optional): The ID of a specific company to duplicate for. If None, duplicates for all companies.
    """
    # Check if target_year is a valid year
    if not isinstance(target_year, int) or target_year < 1900 or target_year > 2100:
        raise ValueError("target_year must be a valid year between 1900 and 2100.")
    
    # get the list of companies to work with
    if company_id:
        try:
            company = Empresa.objects.get(codigoempresa = company_id)
            requisitos_detalle = RequisitoPorEmpresaDetalle.objects.filter(matriz__empresa=company)
        except Empresa.DoesNotExist:
             raise ValidationError(f"No se encuentra la empresa {company_id}.")
        
    else:
       requisitos_detalle = RequisitoPorEmpresaDetalle.objects.all()

    # Iterate over the requirements details
    for requisito_detalle in requisitos_detalle:
       # Check if exists
        exists = Plan.objects.filter(year=target_year, requisito_empresa=requisito_detalle).exists()
        if not exists:
            # Create the new plan object
            new_plan = Plan(
                empresa=requisito_detalle.matriz.empresa,
                requisito_empresa=requisito_detalle,
                year=target_year,
                periodicidad=requisito_detalle.periodicidad,
                fecha_inicio = requisito_detalle.fecha_inicio

                # You can copy other fields from RequisitoPorEmpresaDetalle to Plan if needed
            )
            new_plan.save()
        else:
            print(f"Ya existe un plan para {requisito_detalle} en el año {target_year}.")

