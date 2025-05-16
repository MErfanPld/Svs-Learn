from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .twilio_utils import send_whatsapp_message

@csrf_exempt
def whatsapp_webhook(request):
    if request.method == 'POST':
        body = request.POST.get('Body', '').strip().lower()
        sender = request.POST.get('From', '')

        if 'ثبت نام' in body:
            send_whatsapp_message(sender, '✅ شما با موفقیت ثبت‌نام شدید.')

        return HttpResponse('ok')
    return HttpResponse('invalid method', status=405)
