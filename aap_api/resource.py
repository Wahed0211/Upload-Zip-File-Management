from import_export import resources
from .models import ExcelData

class ExcelDataResource(resources.ModelResource):
    class Meta:
        model = ExcelData
        