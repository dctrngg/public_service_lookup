# feedback/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction
from .models import Feedback, FeedbackImage, Category
from .forms import FeedbackForm

def submit_feedback(request):
    """View để gửi phản ánh"""
    if request.method == 'POST':
        form = FeedbackForm(request.POST, request.FILES)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Lưu feedback
                    feedback = form.save()
                    
                    # Lưu hình ảnh
                    images = request.FILES.getlist('images')
                    for image in images:
                        FeedbackImage.objects.create(
                            feedback=feedback,
                            image=image
                        )
                    
                    # Gửi email thông báo cho admin
                    send_notification_to_admin(feedback)
                    
                    # Hiển thị thông báo thành công
                    messages.success(
                        request,
                        f'Phản ánh của bạn đã được gửi thành công! '
                        f'Mã theo dõi: <strong>{feedback.tracking_code}</strong>. '
                        f'Vui lòng lưu lại mã này để tra cứu.'
                    )
                    
                    return redirect('feedback_success', tracking_code=feedback.tracking_code)
            
            except Exception as e:
                messages.error(request, f'Có lỗi xảy ra: {str(e)}')
        else:
            messages.error(request, 'Vui lòng kiểm tra lại thông tin đã nhập.')
    else:
        form = FeedbackForm()
    
    return render(request, 'feedback/submit_feedback.html', {
        'form': form,
        'categories': Category.objects.all()
    })


def feedback_success(request, tracking_code):
    """Trang thông báo gửi thành công"""
    feedback = get_object_or_404(Feedback, tracking_code=tracking_code)
    return render(request, 'feedback/success.html', {
        'feedback': feedback
    })


def track_feedback(request):
    """Tra cứu phản ánh theo mã tracking"""
    tracking_code = request.GET.get('tracking_code', '').strip().upper()
    feedback = None
    
    if tracking_code:
        try:
            feedback = Feedback.objects.prefetch_related('images').get(
                tracking_code=tracking_code
            )
        except Feedback.DoesNotExist:
            messages.error(request, 'Không tìm thấy phản ánh với mã này.')
    
    return render(request, 'feedback/track.html', {
        'feedback': feedback,
        'tracking_code': tracking_code
    })


def send_notification_to_admin(feedback):
    """Gửi email thông báo cho admin"""
    try:
        subject = f'[Phản ánh mới] {feedback.get_priority_display()} - {feedback.title}'
        
        message = f"""
Có phản ánh mới từ hệ thống:

Mã theo dõi: {feedback.tracking_code}
Người gửi: {feedback.get_display_name()}
Số điện thoại: {feedback.phone}
Email: {feedback.email or 'Không có'}

Danh mục: {feedback.category.name if feedback.category else 'Không xác định'}
Mức độ: {feedback.get_priority_display()}

Tiêu đề: {feedback.title}
Nội dung:
{feedback.content}

Địa chỉ: {feedback.address or 'Không có'}

Số hình ảnh đính kèm: {feedback.images.count()}

Thời gian: {feedback.created_at.strftime('%d/%m/%Y %H:%M')}

---
Vui lòng đăng nhập vào hệ thống để xem chi tiết và xử lý.
        """
        
        # Lấy danh sách email admin từ settings
        admin_emails = getattr(settings, 'ADMIN_EMAILS', [])
        
        if admin_emails:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=admin_emails,
                fail_silently=False,
            )
    except Exception as e:
        # Log lỗi nhưng không raise exception để không ảnh hưởng đến việc gửi form
        print(f"Error sending email: {e}")


def feedback_list(request):
    """Danh sách tất cả phản ánh (cho admin hoặc công khai)"""
    feedbacks = Feedback.objects.select_related('category').prefetch_related('images')
    
    # Lọc theo danh mục
    category_id = request.GET.get('category')
    if category_id:
        feedbacks = feedbacks.filter(category_id=category_id)
    
    # Lọc theo trạng thái
    status = request.GET.get('status')
    if status:
        feedbacks = feedbacks.filter(status=status)
    
    # Lọc theo mức độ ưu tiên
    priority = request.GET.get('priority')
    if priority:
        feedbacks = feedbacks.filter(priority=priority)
    
    return render(request, 'feedback/list.html', {
        'feedbacks': feedbacks,
        'categories': Category.objects.all(),
        'status_choices': Feedback.STATUS_CHOICES,
        'priority_choices': Feedback.PRIORITY_CHOICES,
    })