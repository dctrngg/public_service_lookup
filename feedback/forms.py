# feedback/forms.py
from django import forms
from .models import Feedback, FeedbackImage

class FeedbackForm(forms.ModelForm):
    """Form để gửi phản ánh"""
    
    # Field cho nhiều hình ảnh
    images = forms.FileField(
        widget=forms.ClearableFileInput(attrs={
            # 'multiple': True,
            'accept': 'image/*',
            'class': 'form-control'
        }),
        required=False,
        label='Hình ảnh đính kèm',
        help_text='Có thể chọn nhiều hình ảnh (tối đa 10 ảnh, mỗi ảnh < 5MB)'
    )
    
    class Meta:
        model = Feedback
        fields = [
            'name', 
            'is_anonymous', 
            'phone', 
            'email',
            'category',
            'priority',
            'title',
            'content',
            'address',
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập họ tên của bạn'
            }),
            'is_anonymous': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'anonymousCheck'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '0987654321',
                'pattern': '[0-9]{10,11}',
                'title': 'Vui lòng nhập số điện thoại hợp lệ (10-11 số)'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@example.com (không bắt buộc)'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tóm tắt vấn đề của bạn'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Mô tả chi tiết vấn đề bạn muốn phản ánh...'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Địa chỉ xảy ra sự việc (không bắt buộc)'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Đặt label và help text
        self.fields['name'].label = 'Họ và tên'
        self.fields['is_anonymous'].label = 'Gửi ẩn danh'
        self.fields['phone'].label = 'Số điện thoại liên lạc'
        self.fields['email'].label = 'Email (không bắt buộc)'
        self.fields['category'].label = 'Danh mục'
        self.fields['priority'].label = 'Mức độ ưu tiên'
        self.fields['title'].label = 'Tiêu đề'
        self.fields['content'].label = 'Nội dung phản ánh'
        self.fields['address'].label = 'Địa chỉ'
        
        # Set required fields
        self.fields['name'].required = False
        self.fields['email'].required = False
        self.fields['address'].required = False
    
    def clean_images(self):
        """Validate hình ảnh"""
        images = self.files.getlist('images')
        
        if len(images) > 10:
            raise forms.ValidationError('Bạn chỉ có thể tải lên tối đa 10 hình ảnh.')
        
        for image in images:
            # Kiểm tra kích thước file (5MB)
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError(f'File {image.name} quá lớn. Kích thước tối đa là 5MB.')
            
            # Kiểm tra định dạng file
            if not image.content_type.startswith('image/'):
                raise forms.ValidationError(f'File {image.name} không phải là hình ảnh hợp lệ.')
        
        return images
    
    def clean(self):
        cleaned_data = super().clean()
        is_anonymous = cleaned_data.get('is_anonymous')
        name = cleaned_data.get('name')
        
        # Nếu không ẩn danh thì bắt buộc nhập tên
        if not is_anonymous and not name:
            self.add_error('name', 'Vui lòng nhập họ tên hoặc chọn gửi ẩn danh.')
        
        return cleaned_data