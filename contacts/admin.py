# contacts/admin.py

from django.contrib import admin
from .models import Department, ContactPerson, EmergencyContact


class ContactPersonInline(admin.TabularInline):
    model = ContactPerson
    extra = 1
    fields = ('full_name', 'position', 'phone', 'mobile', 'email', 'display_order', 'is_active')


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'department_type', 'phone', 'email', 'display_order', 'is_active', 'updated_at')
    list_filter = ('department_type', 'is_active', 'created_at')
    search_fields = ('name', 'phone', 'email', 'address')
    list_editable = ('display_order', 'is_active')
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('name', 'department_type', 'description')
        }),
        ('Thông tin liên hệ', {
            'fields': ('address', 'phone', 'hotline', 'email', 'fax')
        }),
        ('Thời gian làm việc', {
            'fields': ('working_hours',)
        }),
        ('Thông tin bổ sung', {
            'fields': ('website', 'map_embed'),
            'classes': ('collapse',)
        }),
        ('Cài đặt hiển thị', {
            'fields': ('display_order', 'is_active')
        }),
    )
    
    inlines = [ContactPersonInline]
    
    class Meta:
        model = Department


@admin.register(ContactPerson)
class ContactPersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'department', 'get_full_position', 'phone', 'mobile', 'is_active', 'display_order')
    list_filter = ('position', 'department', 'is_active')
    search_fields = ('full_name', 'phone', 'mobile', 'email')
    list_editable = ('display_order', 'is_active')
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('department', 'full_name', 'position', 'position_custom')
        }),
        ('Thông tin liên hệ', {
            'fields': ('phone', 'mobile', 'email')
        }),
        ('Cài đặt hiển thị', {
            'fields': ('display_order', 'is_active')
        }),
    )
    
    def get_full_position(self, obj):
        return obj.get_full_position()
    get_full_position.short_description = 'Chức vụ'


@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'emergency_type', 'phone', 'display_order', 'is_active')
    list_filter = ('emergency_type', 'is_active')
    search_fields = ('name', 'phone', 'description')
    list_editable = ('display_order', 'is_active')
    
    fieldsets = (
        ('Thông tin', {
            'fields': ('name', 'emergency_type', 'phone', 'description')
        }),
        ('Cài đặt', {
            'fields': ('display_order', 'is_active')
        }),
    )