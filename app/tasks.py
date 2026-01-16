import os
import asyncio
import aiodns
from celery import shared_task
from django.conf import settings

from .utils import async_validate_email


@shared_task(bind=True)
def validate_emails_task(self, email_list):

    total = len(email_list)
    valid_emails = []
    
    # High concurrency limit
    CONCURRENCY_LIMIT = 1000
    
    async def process_batch():
        # Initialize resolver inside the loop
        resolver = aiodns.DNSResolver()
        
        semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)
        processed_count = 0
        
        async def limited_check(email):
            nonlocal processed_count
            async with semaphore:
                result = await async_validate_email(email, resolver=resolver)
                processed_count += 1
                
                # Update progress roughly every 100 items or 1%
                if processed_count % 100 == 0:
                    process_percent = int((processed_count / total) * 100)
                    # We can't call self.update_state directly from async loop easily unless using sync_to_async wrapper
                    # But since this is running in asyncio.run inside the sync task, we actually CAN call the sync method?
                    # No, self.update_state is thread-safe but maybe not async-safe if using async backend?
                    # Standard Celery with Redis is fine to call from main thread.
                    # Since asyncio.run blocks the main thread, we can only update state if we bubble up or call sync code.
                    # Actually, we can just call the sync update_state, it's just a redis call.
                    pass 
                
                return result

        tasks = [limited_check(email) for email in email_list]
        
        # We need to manually track progress because asyncio.gather waits for all.
        # Alternatively use as_completed
        exclude_none = []
        for f in asyncio.as_completed(tasks):
            result = await f
            if result:
                exclude_none.append(result)
            
            # Progress Update
            # Get current count from the nonlocal variable which is safe in single-threaded async loop
            if processed_count % 200 == 0 or processed_count == total:
                 self.update_state(state='PROGRESS', meta={
                    'current': int((processed_count / total) * 100),
                    'total': total,
                    'processed': processed_count,
                    'valid_count': len(exclude_none)
                })
        
        return exclude_none

    # Run the async loop
    valid_emails = asyncio.run(process_batch())

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
