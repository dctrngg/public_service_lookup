# feedback/models.py
from django.db import models
from django.utils import timezone
import uuid

class Category(models.Model):
    """Danh mục phản ánh"""
    name = models.CharField(max_length=100, verbose_name="Tên danh mục")
    description = models.TextField(blank=True, verbose_name="Mô tả")
    priority_level = models.IntegerField(
        default=1,
        choices=[
            (1, 'Thấp'),
            (2, 'Trung bình'),
            (3, 'Cao'),
            (4, 'Khẩn cấp')
        ],
        verbose_name="Mức độ ưu tiên"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Danh mục"
        verbose_name_plural = "Danh mục"
        ordering = ['-priority_level', 'name']
    
    def __str__(self):
        return self.name


class Feedback(models.Model):
    """Model chính cho phản ánh"""
    STATUS_CHOICES = [
        ('pending', 'Đang chờ xử lý'),
        ('processing', 'Đang xử lý'),
        ('resolved', 'Đã giải quyết'),
        ('rejected', 'Từ chối'),
    ]
    
    PRIORITY_CHOICES = [
        (1, 'Thấp'),
        (2, 'Trung bình'),
        (3, 'Cao'),
        (4, 'Khẩn cấp'),
    ]
    
    # Mã tracking duy nhất
    tracking_code = models.CharField(max_length=12, unique=True, editable=False)
    
    # Thông tin người phản ánh
    name = models.CharField(
        max_length=200, 
        blank=True, 
        default="Ẩn danh",
        verbose_name="Tên người phản ánh"
    )
    is_anonymous = models.BooleanField(default=False, verbose_name="Ẩn danh")
    phone = models.CharField(max_length=15, verbose_name="Số điện thoại")
    email = models.EmailField(blank=True, null=True, verbose_name="Email (tùy chọn)")
    
    # Nội dung phản ánh
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True,
        verbose_name="Danh mục"
    )
    priority = models.IntegerField(
        choices=PRIORITY_CHOICES,
        default=2,
        verbose_name="Mức độ ưu tiên"
    )
    title = models.CharField(max_length=200, verbose_name="Tiêu đề")
    content = models.TextField(verbose_name="Nội dung phản ánh")
    
    # Trạng thái
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Trạng thái"
    )
    
    # Thông tin vị trí (tùy chọn)
    address = models.CharField(max_length=500, blank=True, verbose_name="Địa chỉ")
    latitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True,
        verbose_name="Vĩ độ"
    )
    longitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True,
        verbose_name="Kinh độ"
    )
    
    # Phản hồi từ admin
    admin_note = models.TextField(blank=True, verbose_name="Ghi chú của admin")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày gửi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Cập nhật lần cuối")
    resolved_at = models.DateTimeField(null=True, blank=True, verbose_name="Ngày giải quyết")
    
    class Meta:
        verbose_name = "Phản ánh"
        verbose_name_plural = "Phản ánh"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['tracking_code']),
            models.Index(fields=['status']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.tracking_code:
            self.tracking_code = self.generate_tracking_code()
        
        # Tự động set tên là "Ẩn danh" nếu checkbox được chọn
        if self.is_anonymous:
            self.name = "Ẩn danh"
        
        # Tự động cập nhật resolved_at khi status = resolved
        if self.status == 'resolved' and not self.resolved_at:
            self.resolved_at = timezone.now()
        
        super().save(*args, **kwargs)
    
    def generate_tracking_code(self):
        """Tạo mã tracking duy nhất"""
        return uuid.uuid4().hex[:12].upper()
    
    def get_display_name(self):
        """Trả về tên hiển thị"""
        return "Ẩn danh" if self.is_anonymous else self.name
    
    def __str__(self):
        return f"{self.tracking_code} - {self.title[:50]}"


class FeedbackImage(models.Model):
    """Model cho hình ảnh đính kèm"""
    feedback = models.ForeignKey(
        Feedback,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name="Phản ánh"
    )
    image = models.ImageField(
        upload_to='feedback_images/%Y/%m/%d/',
        verbose_name="Hình ảnh"
    )
    caption = models.CharField(max_length=200, blank=True, verbose_name="Chú thích")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Thời gian tải lên")
    
    class Meta:
        verbose_name = "Hình ảnh"
        verbose_name_plural = "Hình ảnh"
        ordering = ['uploaded_at']
    
    def __str__(self):
        return f"Image for {self.feedback.tracking_code}"