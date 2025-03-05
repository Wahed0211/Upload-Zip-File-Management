from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import ExcelData
from .models import UploadedZip

@admin.register(ExcelData)
class ExcelDataAdmin(ImportExportModelAdmin):
    list_display = (
        'job_title',
        'date_of_application',
        'email_id',
        'phone_number',
        'current_location',
        'preferred_locations',
        'total_experience',
        'current_company_name',
        'current_company_designation',
        'key_skills',
        'annual_salary',
        'notice_period_availability_to_join',
        'resume_headline',
        'under_graduation_degree',
        'ug_specialization',
        'ug_university_institute_name',
        'ug_graduation_year',
        'post_graduation_degree',
        'pg_specialization',
        'pg_university_institute_name',
        'pg_graduation_year',
        'doctorate_degree',
        'doctorate_specialization',
    )

@admin.register(UploadedZip)
class UploadedZipAdmin(admin.ModelAdmin):
    list_display = ("name", "file", "uploaded_at")
    
    # Override formfield_for_dbfield to prevent decoding errors
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name == "file":
            formfield.widget.attrs["accept"] = ".zip"  # Only allow ZIP uploads
        return formfield
