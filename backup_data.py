import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'public_service_project.settings')
django.setup()

from django.core.management import call_command

# Export với UTF-8
print("Đang backup dữ liệu...")
with open('data_backup.json', 'w', encoding='utf-8') as f:
    call_command(
        'dumpdata',
        exclude=['auth.permission', 'contenttypes', 'sessions'],
        indent=2,
        stdout=f
    )

print("✓ Backup thành công: data_backup.json")