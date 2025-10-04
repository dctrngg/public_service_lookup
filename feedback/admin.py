# feedback/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Feedback, FeedbackImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'priority_level', 'created_at']
    list_filter = ['priority_level']
    search_fields = ['name', 'description']


class FeedbackImageInline(admin.TabularInline):
    model = FeedbackImage
    extra = 0
    readonly_fields = ['image_preview', 'uploaded_at']
    fields = ['image_preview', 'image', 'caption', 'uploaded_at']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 200px;" />',
                obj.image.url
            )
        return "No image"
    image_preview.short_description = 'Xem trước'


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = [
        'tracking_code', 
        'get_display_name', 
        'phone', 
        'category',
        'priority_badge',
        'status_badge',
        'created_at'
    ]
    list_filter = ['status', 'priority', 'category', 'is_anonymous', 'created_at']
    search_fields = ['tracking_code', 'name', 'phone', 'title', 'content']
    readonly_fields = ['tracking_code', 'created_at', 'updated_at', 'resolved_at']
    inlines = [FeedbackImageInline]
    
    fieldsets = (
        ('Thông tin tracking', {
            'fields': ('tracking_code', 'status', 'priority')
        }),
        ('Thông tin người gửi', {
            'fields': ('name', 'is_anonymous', 'phone', 'email')
        }),
        ('Nội dung phản ánh', {
            'fields': ('category', 'title', 'content', 'address', 'latitude', 'longitude')
        }),
        ('Xử lý', {
            'fields': ('admin_note',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'resolved_at'),
            'classes': ('collapse',)
        }),
    )
    
    def priority_badge(self, obj):
        colors = {
            1: '#6c757d',  # gray
            2: '#0dcaf0',  # cyan
            3: '#ffc107',  # yellow
            4: '#dc3545',  # red
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            colors.get(obj.priority, '#6c757d'),
            obj.get_priority_display()
        )
    priority_badge.short_description = 'Mức độ'
    
    def status_badge(self, obj):
        colors = {
            'pending': '#ffc107',     # yellow
            'processing': '#0dcaf0',  # cyan
            'resolved': '#198754',    # green
            'rejected': '#dc3545',    # red
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            colors.get(obj.status, '#6c757d'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Trạng thái'
    
    actions = ['mark_as_processing', 'mark_as_resolved']
    
    def mark_as_processing(self, request, queryset):
        updated = queryset.update(status='processing')
        self.message_user(request, f'{updated} phản ánh đã được đánh dấu đang xử lý.')
    mark_as_processing.short_description = 'Đánh dấu đang xử lý'
    
    def mark_as_resolved(self, request, queryset):
        from django.utils import timezone
        updated = queryset.filter(status__in=['pending', 'processing']).update(
            status='resolved',
            resolved_at=timezone.now()
        )
        self.message_user(request, f'{updated} phản ánh đã được đánh dấu đã giải quyết.')
    mark_as_resolved.short_description = 'Đánh dấu đã giải quyết'


@admin.register(FeedbackImage)
class FeedbackImageAdmin(admin.ModelAdmin):
    list_display = ['feedback', 'image_preview', 'uploaded_at']
    list_filter = ['uploaded_at']
    readonly_fields = ['image_preview', 'uploaded_at']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 200px;" />',
                obj.image.url
            )
        return "No image"
    image_preview.short_description = 'Xem trước'