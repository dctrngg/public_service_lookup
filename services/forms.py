from django import forms
from .models import PublicService

class ServiceSearchForm(forms.Form):
    """
    Form tìm kiếm và lọc dịch vụ hành chính công
    """
    title = forms.CharField(
        required=False,
        label='Tên thủ tục',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nhập tên thủ tục cần tìm...'
        })
    )
    
    public_sector = forms.CharField(
        required=False,
        label='Lĩnh vực',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ví dụ: Giao thông, Tư pháp...'
        })
    )
    
    department = forms.CharField(
        required=False,
        label='Cơ quan thực hiện',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nhập tên cơ quan...'
        })
    )
    
    service_level = forms.ChoiceField(
        required=False,
        label='Mức độ dịch vụ',
        choices=[('', 'Tất cả')] + PublicService.SERVICE_LEVEL_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    jurisdiction = forms.ChoiceField(
        required=False,
        label='Phạm vi thực hiện',
        choices=[('', 'Tất cả')] + PublicService.JURISDICTION_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )