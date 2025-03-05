from rest_framework import serializers
from .models import ExcelData

class ExcelDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExcelData
        fields = [
            'id', 'job_title', 'date_of_application', 'name', 'email_id', 
            'phone_number', 'current_location', 'preferred_locations', 
            'total_experience', 'current_company_name', 'current_company_designation',
            'department', 'role', 'industry', 'key_skills', 'annual_salary',
            'notice_period_availability_to_join', 'resume_headline', 'summary',
            'under_graduation_degree', 'ug_specialization', 'ug_university_institute_name',
            'ug_graduation_year', 'post_graduation_degree', 'pg_specialization',
            'pg_university_institute_name', 'pg_graduation_year', 'doctorate_degree',
            'doctorate_specialization', 'doctorate_university_institute_name',
            'doctorate_graduation_year', 'gender', 'marital_status', 'home_town_city',
            'pin_code', 'work_permit_for_usa', 'date_of_birth', 'permanent_address'
        ]