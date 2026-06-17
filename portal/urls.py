from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('submit/', views.submit_complaint, name='submit_complaint'),
    path('notice-board/', views.notice_board, name='notice_board'),
    path('portal-admin/login/', views.admin_login, name='admin_login'),
    path('portal-admin/logout/', views.admin_logout, name='admin_logout'),
    path('portal-admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('portal-admin/management/', views.admin_management, name='admin_management'),
    path('portal-admin/add-announcement/', views.add_announcement, name='add_announcement'),
    path('portal-admin/delete-announcement/<int:announcement_id>/', views.delete_announcement, name='delete_announcement'),
    path('portal-admin/update-status/<int:complaint_id>/', views.update_status, name='update_status'),
    path('portal-admin/delete/<int:complaint_id>/', views.delete_complaint, name='delete_complaint'),
    path('portal-admin/export/', views.export_complaints, name='export_complaints'),
]