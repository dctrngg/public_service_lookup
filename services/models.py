from django.db import models

class PublicService(models.Model):
    """
    Model lưu trữ thông tin Dịch vụ Hành chính Công
    """
    SERVICE_LEVEL_CHOICES = [
        (1, 'Mức 1 - Thông tin'),
        (2, 'Mức 2 - Tương tác một chiều'),
        (3, 'Mức 3 - Tương tác hai chiều'),
        (4, 'Mức 4 - Giao dịch điện tử'),
    ]
    
    JURISDICTION_CHOICES = [
        ('cap_tinh', 'Cấp Tỉnh'),
        ('cap_huyen', 'Cấp Huyện'),
        ('cap_xa', 'Cấp Xã'),
        ('trung_uong', 'Trung ương'),
    ]
    
    title = models.CharField(
        max_length=255,
        verbose_name='Tên Thủ tục Hành chính',
        help_text='Ví dụ: Cấp lại Giấy phép lái xe'
    )
    
    public_sector = models.CharField(
        max_length=100,
        verbose_name='Lĩnh vực',
        help_text='Ví dụ: Giao thông Vận tải, Tư pháp'
    )
    
    department = models.CharField(
        max_length=150,
        verbose_name='Cơ quan Thực hiện',
        help_text='Ví dụ: Cục Cảnh sát Giao thông, Sở Tư pháp'
    )
    
    jurisdiction = models.CharField(
        max_length=50,
        choices=JURISDICTION_CHOICES,
        verbose_name='Phạm vi Thực hiện',
        default='cap_tinh'
    )
    
    service_level = models.IntegerField(
        choices=SERVICE_LEVEL_CHOICES,
        verbose_name='Mức độ Dịch vụ Công',
        default=4
    )
    
    description = models.TextField(
        verbose_name='Mô tả',
        help_text='Mô tả tóm tắt hoặc chi tiết về thủ tục',
        blank=True
    )
    
    legal_basis = models.TextField(
        verbose_name='Căn cứ Pháp lý',
        help_text='Các văn bản luật, nghị định',
        blank=True
    )
    
    procedure_steps = models.TextField(
        verbose_name='Trình tự Thực hiện',
        help_text='Các bước thực hiện thủ tục (mỗi bước một dòng)',
        blank=True
    )
    
    processing_time = models.CharField(
        max_length=50,
        verbose_name='Thời hạn Giải quyết',
        help_text='Ví dụ: 05 ngày làm việc',
        blank=True
    )
    
    fee = models.CharField(
        max_length=100,
        verbose_name='Phí và Lệ phí',
        help_text='Ví dụ: 135.000 VNĐ hoặc Miễn phí',
        blank=True
    )
    
    required_documents = models.TextField(
        verbose_name='Thành phần Hồ sơ',
        help_text='Các giấy tờ cần nộp (mỗi loại một dòng)',
        blank=True
    )
    
    contact_info = models.CharField(
        max_length=255,
        verbose_name='Thông tin Liên hệ',
        help_text='Cơ quan hỗ trợ, địa chỉ, số điện thoại, email',
        blank=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')
    
    class Meta:
        verbose_name = 'Dịch vụ Hành chính Công'
        verbose_name_plural = 'Dịch vụ Hành chính Công'
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title
    
    def get_service_level_display_short(self):
        """Trả về mức độ dịch vụ dạng ngắn gọn"""
        return f"Mức {self.service_level}"
    
    def get_jurisdiction_display_name(self):
        """Trả về tên phạm vi thực hiện"""
        return dict(self.JURISDICTION_CHOICES).get(self.jurisdiction, self.jurisdiction)