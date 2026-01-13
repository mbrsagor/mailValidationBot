import os
from celery import shared_task, current_task
from django.conf import settings
from .utils import is_valid_email


@shared_task(bind=True)
def validate_emails_task(self, email_list):
    total = len(email_list)
    valid_emails = []
    
    for index, email in enumerate(email_list):
        result = is_valid_email(email)
        if result:
            valid_emails.append(result)
        
        # Update progress every 100 emails to save resources
        if index % 100 == 0 or index == total - 1:
            process_percent = int((index / total) * 100)
            self.update_state(state='PROGRESS', meta={'current': process_percent})

    # Save to file
    filename = f"validated_emails_{self.request.id}.txt"
    filepath = os.path.join(settings.MEDIA_ROOT, filename)
    
    if not os.path.exists(settings.MEDIA_ROOT):
        os.makedirs(settings.MEDIA_ROOT)
        
    with open(filepath, 'w') as f:
        f.write("\n".join(valid_emails))
    
    return {'file_url': f"{settings.MEDIA_URL}{filename}"}
