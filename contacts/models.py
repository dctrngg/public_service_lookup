# contacts/models.py

from django.db import models

class Department(models.Model):
    """Model cho Phòng ban/Đơn vị"""
    
    DEPARTMENT_TYPES = [
        ('hanh_chinh', 'Hành chính - Tổng hợp'),
        ('tai_chinh', 'Tài chính - Kế toán'),
        ('tu_phap', 'Tư pháp - Hộ tịch'),
        ('xay_dung', 'Xây dựng - Đô thị'),
        ('kinh_te', 'Kinh tế'),
        ('van_hoa', 'Văn hóa - Xã hội'),
        ('dan_so', 'Dân số - KHHGĐ'),
        ('lao_dong', 'Lao động - Thương binh'),
        ('cong_an', 'Công an'),
        ('y_te', 'Y tế'),
        ('giao_duc', 'Giáo dục'),
        ('khac', 'Khác'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="Tên phòng ban")
    department_type = models.CharField(
        max_length=50, 
        choices=DEPARTMENT_TYPES,
        default='hanh_chinh',
        verbose_name="Loại phòng ban"
    )
    description = models.TextField(blank=True, verbose_name="Mô tả")
    address = models.CharField(max_length=300, verbose_name="Địa chỉ")
    phone = models.CharField(max_length=20, verbose_name="Số điện thoại")
    hotline = models.CharField(max_length=20, blank=True, verbose_name="Đường dây nóng")
    email = models.EmailField(blank=True, verbose_name="Email")
    fax = models.CharField(max_length=20, blank=True, verbose_name="Fax")
    
    # Thời gian làm việc
    working_hours = models.CharField(
        max_length=200, 
        default="Thứ 2 - Thứ 6: 7h30 - 11h30, 13h30 - 17h30",
        verbose_name="Giờ làm việc"
    )
    
    # Thông tin bổ sung
    website = models.URLField(blank=True, verbose_name="Website")
    map_embed = models.TextField(blank=True, verbose_name="Google Maps Embed Code")
    
    # Thứ tự hiển thị
    display_order = models.IntegerField(default=0, verbose_name="Thứ tự hiển thị")
    is_active = models.BooleanField(default=True, verbose_name="Đang hoạt động")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Cập nhật lần cuối")
    
    class Meta:
        verbose_name = "Phòng ban"
        verbose_name_plural = "Các phòng ban"
        ordering = ['display_order', 'name']
    
    def __str__(self):
        return self.name


class ContactPerson(models.Model):
    """Model cho Người liên hệ"""
    
    POSITION_CHOICES = [
        ('truong_phong', 'Trưởng phòng'),
        ('pho_phong', 'Phó phòng'),
        ('chuyen_vien', 'Chuyên viên'),
        ('nhan_vien', 'Nhân viên'),
        ('khac', 'Khác'),
    ]
    
    department = models.ForeignKey(
        Department, 
        on_delete=models.CASCADE,
        related_name='contacts',
        verbose_name="Phòng ban"
    )
    full_name = models.CharField(max_length=100, verbose_name="Họ và tên")
    position = models.CharField(
        max_length=50,
        choices=POSITION_CHOICES,
        verbose_name="Chức vụ"
    )
    position_custom = models.CharField(
        max_length=100, 
        blank=True,
        verbose_name="Chức vụ khác (nếu có)"
    )
    phone = models.CharField(max_length=20, verbose_name="Số điện thoại")
    mobile = models.CharField(max_length=20, blank=True, verbose_name="Di động")
    email = models.EmailField(blank=True, verbose_name="Email")
    
    display_order = models.IntegerField(default=0, verbose_name="Thứ tự hiển thị")
    is_active = models.BooleanField(default=True, verbose_name="Đang hoạt động")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Cập nhật lần cuối")
    
    class Meta:
        verbose_name = "Người liên hệ"
        verbose_name_plural = "Danh sách người liên hệ"
        ordering = ['display_order', 'full_name']
    
    def __str__(self):
        return f"{self.full_name} - {self.get_position_display()}"
    
    def get_full_position(self):
        """Trả về chức vụ đầy đủ"""
        if self.position == 'khac' and self.position_custom:
            return self.position_custom
        return self.get_position_display()


class EmergencyContact(models.Model):
    """Model cho Đường dây nóng/Liên hệ khẩn cấp"""
    
    EMERGENCY_TYPES = [
        ('canh_sat', 'Công an/Cảnh sát'),
        ('cuu_hoa', 'Cứu hỏa'),
        ('y_te', 'Y tế cấp cứu'),
        ('dien_nuoc', 'Điện nước'),
        ('hanh_chinh', 'Hành chính khẩn cấp'),
        ('khac', 'Khác'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="Tên đường dây")
    emergency_type = models.CharField(
        max_length=50,
        choices=EMERGENCY_TYPES,
        verbose_name="Loại"
    )
    phone = models.CharField(max_length=20, verbose_name="Số điện thoại")
    description = models.TextField(blank=True, verbose_name="Mô tả")
    
    display_order = models.IntegerField(default=0, verbose_name="Thứ tự hiển thị")
    is_active = models.BooleanField(default=True, verbose_name="Đang hoạt động")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Cập nhật lần cuối")
    
    class Meta:
        verbose_name = "Đường dây khẩn cấp"
        verbose_name_plural = "Các đường dây khẩn cấp"
        ordering = ['display_order', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.phone}"