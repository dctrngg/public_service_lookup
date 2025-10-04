from django.contrib import admin
from .models import PublicService

@admin.register(PublicService)
class PublicServiceAdmin(admin.ModelAdmin):
    """
    Cấu hình Admin cho model PublicService
    """
    list_display = [
        'title', 
        'public_sector', 
        'department', 
        'service_level', 
        'jurisdiction',
        'processing_time',
        'created_at'
    ]
    
    list_filter = [
        'service_level', 
        'jurisdiction', 
        'public_sector',
        'created_at'
    ]
    
    search_fields = [
        'title', 
        'public_sector', 
        'department', 
        'description'
    ]
    
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('title', 'public_sector', 'department', 'jurisdiction', 'service_level')
        }),
        ('Mô tả', {
            'fields': ('description',)
        }),
        ('Thông tin thủ tục', {
            'fields': ('legal_basis', 'procedure_steps', 'processing_time', 'fee', 'required_documents')
        }),
        ('Liên hệ', {
            'fields': ('contact_info',)
        }),
        ('Thông tin hệ thống', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ['-created_at']
    
    date_hierarchy = 'created_at'
    
    list_per_page = 20
    
    def get_queryset(self, request):
        """
        Tối ưu queryset
        """
        queryset = super().get_queryset(request)
        return queryset.select_related()
    
    actions = ['mark_as_level_4']
    
    def mark_as_level_4(self, request, queryset):
        """
        Action đánh dấu các dịch vụ là mức 4
        """
        updated = queryset.update(service_level=4)
        self.message_user(request, f'{updated} dịch vụ đã được cập nhật lên mức 4.')
    
    mark_as_level_4.short_description = 'Đánh dấu là Mức 4 (Giao dịch điện tử)'