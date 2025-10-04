from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import PublicService
from .forms import ServiceSearchForm
from django.shortcuts import render


class ServiceListView(ListView):
    """
    View hiển thị danh sách dịch vụ hành chính công với tính năng tìm kiếm và phân trang
    """
    model = PublicService
    template_name = 'services/service_list.html'
    context_object_name = 'services'
    paginate_by = 10  # Phân trang 10 items mỗi trang
    
    def get_queryset(self):
        """
        Lọc danh sách dịch vụ dựa trên các tham số tìm kiếm
        """
        queryset = super().get_queryset()
        
        # Lấy các tham số tìm kiếm từ GET request
        title = self.request.GET.get('title', '').strip()
        public_sector = self.request.GET.get('public_sector', '').strip()
        department = self.request.GET.get('department', '').strip()
        service_level = self.request.GET.get('service_level', '').strip()
        jurisdiction = self.request.GET.get('jurisdiction', '').strip()
        
        # Áp dụng các bộ lọc
        if title:
            queryset = queryset.filter(
                Q(title__icontains=title) | 
                Q(description__icontains=title)
            )
        
        if public_sector:
            queryset = queryset.filter(public_sector__icontains=public_sector)
        
        if department:
            queryset = queryset.filter(department__icontains=department)
        
        if service_level:
            queryset = queryset.filter(service_level=service_level)
        
        if jurisdiction:
            queryset = queryset.filter(jurisdiction=jurisdiction)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        """
        Thêm form tìm kiếm và các thông tin bổ sung vào context
        """
        context = super().get_context_data(**kwargs)
        
        # Khởi tạo form với dữ liệu từ GET request
        context['search_form'] = ServiceSearchForm(self.request.GET or None)
        
        # Thêm thông tin về số lượng kết quả
        context['total_services'] = self.get_queryset().count()
        
        # Giữ các tham số tìm kiếm cho phân trang
        query_params = self.request.GET.copy()
        if 'page' in query_params:
            query_params.pop('page')
        context['query_string'] = query_params.urlencode()
        
        # Kiểm tra xem có đang tìm kiếm không
        context['is_searching'] = any([
            self.request.GET.get('title'),
            self.request.GET.get('public_sector'),
            self.request.GET.get('department'),
            self.request.GET.get('service_level'),
            self.request.GET.get('jurisdiction'),
        ])
        
        return context


class ServiceDetailView(DetailView):
    """
    View hiển thị chi tiết một dịch vụ hành chính công
    """
    model = PublicService
    template_name = 'services/service_detail.html'
    context_object_name = 'service'
    
    def get_context_data(self, **kwargs):
        """
        Thêm các thông tin bổ sung vào context
        """
        context = super().get_context_data(**kwargs)
        
        # Chuyển đổi procedure_steps và required_documents thành list
        service = self.object
        
        if service.procedure_steps:
            context['procedure_steps_list'] = [
                step.strip() 
                for step in service.procedure_steps.split('\n') 
                if step.strip()
            ]
        else:
            context['procedure_steps_list'] = []
        
        if service.required_documents:
            context['required_documents_list'] = [
                doc.strip() 
                for doc in service.required_documents.split('\n') 
                if doc.strip()
            ]
        else:
            context['required_documents_list'] = []
        
        if service.legal_basis:
            context['legal_basis_list'] = [
                legal.strip() 
                for legal in service.legal_basis.split('\n') 
                if legal.strip()
            ]
        else:
            context['legal_basis_list'] = []
        
        return context
    

    from django.shortcuts import render

def home(request):
    return render(request, "base.html")  # gọi từ thư mục templates chung
