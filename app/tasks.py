import os
from celery import shared_task, current_task
from django.conf import settings
from .utils import is_valid_email


@shared_task(bind=True)
def validate_emails_task(self, email_list):
    total = len(email_list)
    valid_emails = []
    
    # Use concurrent.futures for parallel execution
    import concurrent.futures

    # Determine number of workers - be careful not to trigger rate limits/blocks
    # 20-50 is usually a safe range for this kind of lightweight checking
    max_workers = 50 
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_email = {executor.submit(is_valid_email, email): email for email in email_list}
        
        completed_count = 0
        for future in concurrent.futures.as_completed(future_to_email):
            email = future_to_email[future]
            completed_count += 1
            
            try:
                result = future.result()
                if result:
                    valid_emails.append(result)
            except Exception as exc:
                # Log error or ignore
                pass
            
            # Update progress every 50 completed items or at the end
            if completed_count % 50 == 0 or completed_count == total:
                process_percent = int((completed_count / total) * 100)
                # Keep tracking count of valid found so far
                self.update_state(state='PROGRESS', meta={
                    'current': process_percent,
                    'percent': process_percent,
                    'total': total,
                    'processed': completed_count,
                    'valid_count': len(valid_emails)
                })

    # Save to file
    filename = f"validated_emails_{self.request.id}.txt"
    filepath = os.path.join(settings.MEDIA_ROOT, filename)
    
    if not os.path.exists(settings.MEDIA_ROOT):
        os.makedirs(settings.MEDIA_ROOT)
        
    with open(filepath, 'w') as f:
        f.write("\n".join(valid_emails))
    
    return {
        'file_url': f"{settings.MEDIA_URL}{filename}",
        'count': len(valid_emails)
    }
