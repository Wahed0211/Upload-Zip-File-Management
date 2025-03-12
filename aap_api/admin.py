from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import ExcelData, UploadedZip
from django.utils.html import format_html
import zipfile
import io


# Admin for ExcelData Model (CRUD operations)
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
    
    # Customize list view for additional actions (e.g., filtering, search, etc.)
    search_fields = ('email_id', 'phone_number', 'job_title')
    list_filter = ('job_title', 'current_location')

    # Override to define custom validation or actions if needed
    def save_model(self, request, obj, form, change):
        # You can perform custom save operations here if necessary
        obj.save()


# Admin for UploadedZip Model (CRUD operations)
@admin.register(UploadedZip)
class UploadedZipAdmin(admin.ModelAdmin):
    list_display = ("name", "file", "uploaded_at")
    
    search_fields = ('name',)  # You can search by name in the admin panel

    # Override formfield_for_dbfield to restrict file input to .zip files
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name == "file":
            formfield.widget.attrs["accept"] = ".zip"  # Only allow ZIP uploads
        return formfield

    # To handle ZIP extraction logic (if needed)
    def save_model(self, request, obj, form, change):
        # For example, you can handle ZIP file extraction upon upload
        if obj.file:
            # You can add zip extraction logic here if you want
            zip_file = zipfile.ZipFile(obj.file)
            # Do something with the extracted files, like saving them in a specific folder
            # You can also read the files inside the ZIP file if necessary.
            zip_file.close()
        super().save_model(request, obj, form, change)

from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Custom UserAdmin class
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'date_joined', 'last_login', 'is_user_active')
    list_filter = ('is_active', 'date_joined')

    actions = ['activate_users', 'deactivate_users']  # Add custom actions here
    
    # Custom method to change the user status to active
    def activate_users(self, request, queryset):
        updated_count = queryset.update(is_active=True)
        self.message_user(request, f'{updated_count} user(s) have been activated.')
    activate_users.short_description = _('Activate selected users')

    # Custom method to change the user status to inactive
    def deactivate_users(self, request, queryset):
        updated_count = queryset.update(is_active=False)
        self.message_user(request, f'{updated_count} user(s) have been deactivated.')
    deactivate_users.short_description = _('Deactivate selected users')

    # Custom method to display user status in the list
    def is_user_active(self, obj):
        return "Active" if obj.is_active else "Inactive"
    is_user_active.short_description = _('Status')

# Register the custom user admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)