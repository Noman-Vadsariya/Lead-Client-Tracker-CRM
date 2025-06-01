from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count, Q
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from .models import Lead, Client, Note, FollowUp


@login_required
def dashboard(request):
    # Get the date filter from request
    date_str = request.GET.get('date')
    if date_str:
        try:
            selected_date = timezone.datetime.strptime(
                date_str, '%Y-%m-%d').date()
        except ValueError:
            selected_date = timezone.now().date()
    else:
        selected_date = timezone.now().date()

    # Get today's follow-ups
    today_followups = FollowUp.objects.filter(
        scheduled_date__date=selected_date,
        status='pending'
    ).select_related('lead', 'client', 'assigned_to')

    # Get lead pipeline statistics
    lead_stats = Lead.objects.values('status').annotate(
        count=Count('id')
    ).order_by('status')

    # Get recent notes
    recent_notes = Note.objects.select_related(
        'lead', 'client', 'created_by'
    ).order_by('-created_at')[:10]

    context = {
        'today': selected_date,
        'today_followups': today_followups,
        'lead_stats': {stat['status']: stat['count'] for stat in lead_stats},
        'recent_notes': recent_notes,
    }

    return render(request, 'crm/dashboard.html', context)


@login_required
def lead_list(request):
    # Get filter parameters
    status = request.GET.get('status')
    search = request.GET.get('search')
    assigned_to = request.GET.get('assigned_to')

    # Start with base queryset
    leads = Lead.objects.all()

    # Apply filters
    if not request.user.is_staff:
        leads = leads.filter(assigned_to=request.user)

    if status:
        leads = leads.filter(status=status)

    if search:
        leads = leads.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(company__icontains=search) |
            Q(notes__icontains=search)
        )

    if assigned_to:
        leads = leads.filter(assigned_to_id=assigned_to)

    # Order by created_at
    leads = leads.order_by('-created_at')

    # Pagination
    paginator = Paginator(leads, 10)  # Show 10 leads per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get all users for the assigned_to filter
    users = User.objects.filter(is_active=True)

    context = {
        'leads': page_obj,
        'users': users,
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj,
    }

    return render(request, 'crm/lead_list.html', context)
