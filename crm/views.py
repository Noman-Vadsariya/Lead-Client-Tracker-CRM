from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count
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
