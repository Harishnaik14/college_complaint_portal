import csv
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .forms import AnnouncementForm, ComplaintForm
from .models import Announcement, Complaint


def home(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')
    return redirect('submit_complaint')


def submit_complaint(request):
    announcements = Announcement.objects.all()[:5]

    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            if complaint.anonymous:
                complaint.name = ''
                complaint.email = ''
            complaint.save()
            messages.success(request, 'Your complaint or suggestion has been submitted successfully.')
            return redirect('submit_complaint')
    else:
        form = ComplaintForm()

    return render(request, 'submit.html', {
        'form': form,
        'announcements': announcements,
    })


def notice_board(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('submit_complaint')

    query = request.GET.get('q', '')
    complaints = Complaint.objects.filter(status='Resolved')
    if query:
        complaints = complaints.filter(
            Q(subject__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query)
        )

    announcements = Announcement.objects.all()

    return render(request, 'notice_board.html', {
        'announcements': announcements,
        'complaints': complaints,
        'query': query,
    })


def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            messages.success(request, 'Welcome back, admin.')
            return redirect('admin_dashboard')
        messages.error(request, 'Invalid admin credentials.')

    return render(request, 'admin_login.html')


@login_required
def admin_dashboard(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    status = request.GET.get('status', '')

    complaints = Complaint.objects.all()
    if query:
        complaints = complaints.filter(
            Q(subject__icontains=query) |
            Q(description__icontains=query) |
            Q(name__icontains=query) |
            Q(email__icontains=query)
        )
    if category:
        complaints = complaints.filter(category=category)
    if status:
        complaints = complaints.filter(status=status)

    category_counts = Complaint.objects.values('category').annotate(count=Count('id')).order_by('-count')
    stats = {
        'total': Complaint.objects.count(),
        'pending': Complaint.objects.filter(status='Pending').count(),
        'in_progress': Complaint.objects.filter(status='In Progress').count(),
        'resolved': Complaint.objects.filter(status='Resolved').count(),
    }

    return render(request, 'dashboard.html', {
        'complaints': complaints,
        'query': query,
        'category': category,
        'status': status,
        'stats': stats,
        'category_counts': category_counts,
        'complaint_categories': [choice[0] for choice in Complaint.CATEGORY_CHOICES],
        'complaint_statuses': Complaint.STATUS_CHOICES,
    })


@login_required
def update_status(request, complaint_id):
    if request.method == 'POST':
        complaint = get_object_or_404(Complaint, id=complaint_id)
        new_status = request.POST.get('status')
        if new_status in dict(Complaint.STATUS_CHOICES):
            complaint.status = new_status
            complaint.save()
            messages.success(request, f"Complaint #{complaint.id} status updated.")
    return redirect('admin_dashboard')


@login_required
def delete_complaint(request, complaint_id):
    if request.method == 'POST':
        complaint = get_object_or_404(Complaint, id=complaint_id)
        complaint.delete()
        messages.success(request, f"Complaint #{complaint_id} deleted.")
    return redirect('admin_dashboard')


@login_required
def export_complaints(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="complaints_export.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID', 'Name', 'Email', 'Category', 'Subject', 'Status', 'Anonymous', 'Created At'])
    for complaint in Complaint.objects.all():
        writer.writerow([
            complaint.id,
            complaint.display_name,
            complaint.email or '',
            complaint.category,
            complaint.subject,
            complaint.status,
            'Yes' if complaint.anonymous else 'No',
            complaint.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])
    return response


@login_required
def admin_management(request):
    form = AnnouncementForm()
    announcements = Announcement.objects.all()
    return render(request, 'admin_management.html', {
        'form': form,
        'announcements': announcements,
    })


@login_required
def add_announcement(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            Announcement.objects.create(
                title=form.cleaned_data['title'],
                message=form.cleaned_data['message']
            )
            messages.success(request, 'Announcement added successfully.')
            return redirect('admin_management')
    return redirect('admin_management')


@login_required
def delete_announcement(request, announcement_id):
    if request.method == 'POST':
        announcement = get_object_or_404(Announcement, id=announcement_id)
        announcement.delete()
        messages.success(request, 'Announcement deleted successfully.')
    return redirect('admin_management')


def admin_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')
