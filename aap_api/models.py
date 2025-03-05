from django.db import models
from django.core.mail import send_mass_mail
from django.conf import settings
from typing import Dict, Any
import os
import zipfile
from django.core.files.storage import default_storage
import pandas as pd  # For processing Excel/CSV


# Create your models here.

class ExcelData(models.Model):
    JOB_TITLE_CHOICES = (
        ('Software Engineer', 'Software Engineer'),
        ('Data Analyst', 'Data Analyst'),
        ('Product Manager', 'Product Manager'),
        ('DevOps Engineer', 'DevOps Engineer'),
        ('Quality Assurance Engineer', 'Quality Assurance Engineer'),
        ('UX Designer', 'UX Designer'),
        ('Front End Developer', 'Front End Developer'),
        ('Back End Developer', 'Back End Developer'),
        ('Full Stack Developer', 'Full Stack Developer'),
        ('Other', 'Other')
    )

    job_title = models.CharField(max_length=255, choices=JOB_TITLE_CHOICES, blank=True, db_index=True)
    date_of_application = models.DateField(null=True, blank=True, db_index=True)
    name = models.CharField(max_length=255, blank=True, db_index=True)
    email_id = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=255, blank=True)
    current_location = models.CharField(max_length=255, blank=True, db_index=True)
    preferred_locations = models.CharField(max_length=255, blank=True)
    total_experience = models.CharField(max_length=255, blank=True, db_index=True)
    current_company_name = models.CharField(max_length=255, blank=True, db_index=True)
    current_company_designation = models.CharField(max_length=255, blank=True)
    department = models.CharField(max_length=255, blank=True)
    role = models.CharField(max_length=255, blank=True)
    industry = models.CharField(max_length=255, blank=True)
    key_skills = models.CharField(max_length=255, blank=True)
    annual_salary = models.CharField(max_length=100, blank=True)
    notice_period_availability_to_join = models.CharField(max_length=255, blank=True)
    resume_headline = models.CharField(max_length=255, blank=True)
    summary = models.TextField(blank=True)
    under_graduation_degree = models.CharField(max_length=255, blank=True)
    ug_specialization = models.CharField(max_length=255, blank=True)
    ug_university_institute_name = models.CharField(max_length=255, blank=True)
    ug_graduation_year = models.CharField(max_length=255, blank=True)
    post_graduation_degree = models.CharField(max_length=255, blank=True)
    pg_specialization = models.CharField(max_length=255, blank=True)
    pg_university_institute_name = models.CharField(max_length=255, blank=True)
    pg_graduation_year = models.CharField(max_length=255, blank=True)
    doctorate_degree = models.CharField(max_length=255, blank=True)
    doctorate_specialization = models.CharField(max_length=255, blank=True)
    doctorate_university_institute_name = models.CharField(max_length=255, blank=True)
    doctorate_graduation_year = models.CharField(max_length=255, blank=True)
    gender = models.CharField(max_length=255, blank=True)
    marital_status = models.CharField(max_length=255, blank=True)
    home_town_city = models.CharField(max_length=255, blank=True)
    pin_code = models.CharField(max_length=255, blank=True)
    work_permit_for_usa = models.CharField(max_length=255, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    permanent_address = models.TextField(blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['job_title', 'current_location']),
            models.Index(fields=['name', 'current_company_name']),
            models.Index(fields=['date_of_application', 'total_experience']),
        ]

    def _str_(self):
        return self.name or 'Unnamed Record'

class UploadedExcel(models.Model):
    def upload_path(instance, filename):
        # Create upload directory if it doesn't exist
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        os.makedirs(upload_dir, exist_ok=True)
        return os.path.join('uploads', filename)

    file = models.FileField(upload_to=upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Excel file uploaded at {self.uploaded_at}"

class DownloadHistory(models.Model):
    user = models.CharField(max_length=255, blank=True, null=True)  # Assuming user is a string, adjust as needed
    download_time = models.DateTimeField(auto_now_add=True)
    filters = models.JSONField()  # Store filters as JSON
    record_count = models.IntegerField()

    def _str_(self):
        return f"Download by {self.user} at {self.download_time}"
    
class UploadedZip(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to="zip_uploads/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the uploaded file

        # Extract ZIP file after saving
        zip_path = os.path.join(settings.MEDIA_ROOT, self.file.name)
        extract_to = os.path.join(settings.MEDIA_ROOT, "extracted_files", self.name)
        os.makedirs(extract_to, exist_ok=True)

        if zipfile.is_zipfile(zip_path):
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(extract_to)

            # Process Extracted Files (CSV or Excel)
            for file_name in os.listdir(extract_to):
                file_path = os.path.join(extract_to, file_name)
                if file_name.endswith(".csv"):
                    self.process_csv(file_path)
                elif file_name.endswith(".xlsx"):
                    self.process_excel(file_path)

    def process_csv(self, file_path):
        """Read CSV and save data to the database"""
        import csv
        from .models import ExcelData  # Import the model to save data

        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                ExcelData.objects.create(
                    job_title=row.get("job_title", ""),
                    name=row.get("name", ""),
                    email_id=row.get("email_id", ""),
                    phone_number=row.get("phone_number", ""),
                    current_location=row.get("current_location", ""),
                    total_experience=row.get("total_experience", ""),
                    current_company_name=row.get("current_company_name", ""),
                )

    def process_excel(self, file_path):
        """Read Excel and save data to the database"""
        from .models import ExcelData  # Import the model

        df = pd.read_excel(file_path)
        for _, row in df.iterrows():
            ExcelData.objects.create(
                job_title=row.get("job_title", ""),
                name=row.get("name", ""),
                email_id=row.get("email_id", ""),
                phone_number=row.get("phone_number", ""),
                current_location=row.get("current_location", ""),
                total_experience=row.get("total_experience", ""),
                current_company_name=row.get("current_company_name", ""),
            )
            