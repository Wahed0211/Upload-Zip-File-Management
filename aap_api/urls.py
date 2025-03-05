from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter
from .views import ExcelDataViewSet, DownloadHistoryListView, ExcelDataListView
from .auth_views import login_view, register_view, logout_view
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'items', ExcelDataViewSet, basename='item')  # This creates /api/items/ endpoints

app_name = 'aap_api'

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', register_view, name='register'),
    path('auth/login/', login_view, name='login'),
    path('auth/logout/', logout_view, name='logout'),
    
    # Main application views
    path('items/', ExcelDataListView.as_view(), name='item_list'),
    
    # API endpoints
    path('', include(router.urls)),
    
    # File handling endpoints
    path('import-excel/', ExcelDataViewSet.as_view({'post': 'import_excel'}), name='data-import-excel'),
    path('import-zip/', ExcelDataViewSet.as_view({'post': 'import_zip_excel'}), name='data-import-zip-excel'),
    path('download-history/', DownloadHistoryListView.as_view(), name='download_history'),
    path('data/export-excel/', ExcelDataViewSet.as_view({'get': 'export_excel'}), name='data-export-excel'),
    path('task-status/', ExcelDataViewSet.as_view({'get': 'task_status'}), name='task-status'),
    
    # Default redirect
    path('', RedirectView.as_view(url='auth/login/', permanent=False)),
]

# Add media URL patterns for file uploads
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    