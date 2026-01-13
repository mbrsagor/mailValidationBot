from django.shortcuts import render
from django.http import JsonResponse
from .tasks import validate_emails_task
from celery.result import AsyncResult


# View to handle email validation requests
def email_tool_view(request):
    if request.method == "POST":
        raw_emails = request.POST.get('emails', '')
        email_list = list(set([e.strip() for e in raw_emails.splitlines() if e.strip()]))
        task = validate_emails_task.delay(email_list)
        return JsonResponse({'task_id': task.id})
    return render(request, 'email_tool.html')


# Endpoint to check task progress
def get_progress(request, task_id):
    # Fetch task result
    result = AsyncResult(task_id)
    response_data = {'state': result.state}
    
    if result.state == 'PROGRESS':
        response_data['percent'] = result.info.get('current', 0)
    elif result.state == 'SUCCESS':
        response_data['percent'] = 100
        response_data['file_url'] = result.info.get('file_url')
        
    return JsonResponse(response_data)
