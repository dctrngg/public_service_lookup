# contacts/views.py

from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Department, EmergencyContact


def contact_list(request):
    """Hiển thị danh sách tất cả phòng ban"""
    
    # Lấy tham số tìm kiếm và filter
    search_query = request.GET.get('search', '')
    department_type = request.GET.get('type', '')
    
    # Query departments
    departments = Department.objects.filter(is_active=True)
    
    # Tìm kiếm
    if search_query:
        departments = departments.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(address__icontains=search_query)
        )
    
    # Filter theo loại phòng ban
    if department_type:
        departments = departments.filter(department_type=department_type)
    
    # Lấy danh sách người liên hệ cho mỗi phòng ban
    departments = departments.prefetch_related('contacts')
    
    # Lấy danh sách đường dây khẩn cấp
    emergency_contacts = EmergencyContact.objects.filter(is_active=True)
    
    # Lấy danh sách loại phòng ban để làm filter
    department_types = Department.DEPARTMENT_TYPES
    
    context = {
        'departments': departments,
        'emergency_contacts': emergency_contacts,
        'department_types': department_types,
        'search_query': search_query,
        'selected_type': department_type,
    }
    
    return render(request, 'contacts/contact_list.html', context)


def department_detail(request, pk):
    """Hiển thị chi tiết một phòng ban"""
    
    department = get_object_or_404(Department, pk=pk, is_active=True)
    contact_persons = department.contacts.filter(is_active=True)
    
    context = {
        'department': department,
        'contact_persons': contact_persons,
    }
    
    return render(request, 'contacts/department_detail.html', context)


def emergency_list(request):
    """Hiển thị danh sách đường dây khẩn cấp"""
    
    emergency_contacts = EmergencyContact.objects.filter(is_active=True)
    
    # Group theo loại
    grouped_contacts = {}
    for contact in emergency_contacts:
        type_name = contact.get_emergency_type_display()
        if type_name not in grouped_contacts:
            grouped_contacts[type_name] = []
        grouped_contacts[type_name].append(contact)
    
    context = {
        'grouped_contacts': grouped_contacts,
    }
    
    return render(request, 'contacts/emergency_list.html', context)