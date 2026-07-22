from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import admin
from apps.crm.models import Proposal, Contract, Invoice

@staff_member_required
def proposal_pdf_view(request, proposal_id):
    proposal = get_object_or_404(Proposal, id=proposal_id)
    services_list = [s.strip() for s in proposal.services.split('\n') if s.strip()]
    milestones_list = [m.strip() for m in proposal.milestones.split('\n') if m.strip()]
    
    context = {
        'proposal': proposal,
        'services_list': services_list,
        'milestones_list': milestones_list,
    }
    return render(request, 'crm/proposal_pdf.html', context)

@staff_member_required
def contract_pdf_view(request, contract_id):
    contract = get_object_or_404(Contract, id=contract_id)
    context = {
        'contract': contract,
    }
    return render(request, 'crm/contract_pdf.html', context)

@staff_member_required
def invoice_pdf_view(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    context = {
        'invoice': invoice,
    }
    return render(request, 'crm/invoice_pdf.html', context)


import json
from django.http import JsonResponse
from apps.contact.models import ContactRequest
from django.views.decorators.csrf import csrf_exempt

@staff_member_required
def crm_kanban_view(request):
    """
    Renders the Kanban CRM Board for Leads.
    """
    leads = ContactRequest.objects.all().order_by('-created_at')
    stages = ['New', 'Contacted', 'Qualified', 'Proposal Sent', 'Won', 'Lost']
    
    context = {
        'title': 'Kanban CRM Board',
        'leads': leads,
        'stages': stages,
    }
    context.update(admin.site.each_context(request))
    return render(request, 'admin/crm/kanban.html', context)

@csrf_exempt
@staff_member_required
def update_lead_status_api(request, lead_id):
    """
    API endpoint updating lead status on drag-and-drop.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_status = data.get('status')
            lead = get_object_or_404(ContactRequest, id=lead_id)
            if new_status in ['New', 'Contacted', 'Qualified', 'Proposal Sent', 'Won', 'Lost']:
                lead.status = new_status
                lead.save()
                return JsonResponse({'success': True})
            return JsonResponse({'success': False, 'message': 'Invalid status'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    return JsonResponse({'success': False, 'message': 'POST required'}, status=405)


from apps.crm.models import CalendarEvent

@staff_member_required
def workspace_calendar_view(request):
    """
    Renders the custom FullCalendar workspace schedule view.
    """
    events = CalendarEvent.objects.all()
    events_data = [{
        'title': e.title,
        'start': e.start_time.isoformat(),
        'end': e.end_time.isoformat(),
        'type': e.event_type,
        'description': e.description or ''
    } for e in events]
    
    context = {
        'title': 'Workspace Calendar & Schedule',
        'events_json': json.dumps(events_data)
    }
    context.update(admin.site.each_context(request))
    return render(request, 'admin/crm/calendar.html', context)


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def client_portal_login_view(request):
    if request.user.is_authenticated:
        return redirect('client-portal')
        
    error_msg = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('client-portal')
        else:
            error_msg = "Invalid username or password."
            
    return render(request, 'crm/portal_login.html', {'error': error_msg})

def client_portal_logout_view(request):
    logout(request)
    return redirect('client-portal-login')

@login_required(login_url='/portal/login/')
def client_portal_view(request):
    from apps.crm.models import Client, Proposal, Contract, Invoice
    client_profile = Client.objects.filter(email=request.user.email).first()
    
    context = {
        'title': 'Client Progress Cockpit',
        'client': client_profile,
        'projects': client_profile.projects.all() if client_profile else [],
        'proposals': Proposal.objects.filter(client=client_profile) if client_profile else [],
        'contracts': Contract.objects.filter(client=client_profile) if client_profile else [],
        'invoices': Invoice.objects.filter(client=client_profile) if client_profile else [],
    }
    return render(request, 'crm/portal_cockpit.html', context)



