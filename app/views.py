import re
from django.shortcuts import render
from django.http import JsonResponse
from .tasks import validate_emails_task
from celery.result import AsyncResult

# View to handle email validation requests
def email_tool_view(request):
    if request.method == "POST":
        raw_input = request.POST.get('emails', '')
        
        # Split by comma, space, or any type of new line
        email_list = re.split(r'[,\s\n\r]+', raw_input)
        
        # Remove empty strings and duplicates
        email_list = list(set([e.strip() for e in email_list if e.strip()]))
        
        if not email_list:
            return JsonResponse({'error': 'No emails found'}, status=400)
            
        task = validate_emails_task.delay(email_list)
        return JsonResponse({'task_id': task.id})
        
    return render(request, 'email_tool.html')


# View to get progress of the email validation task
def get_progress(request, task_id):
    result = AsyncResult(task_id)
    response_data = {'state': result.state}
    
    if result.state == 'PROGRESS':
        response_data['percent'] = result.info.get('percent', 0)
    elif result.state == 'SUCCESS':
        response_data['percent'] = 100
        response_data['file_url'] = result.info.get('file_url')
        response_data['count'] = result.info.get('count')
        
    return JsonResponse(response_data)
