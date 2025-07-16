# Jobs/signals.py

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse
from .models import Application, Notification

@receiver(pre_save, sender=Application)
def notify_status_change(sender, instance, **kwargs):
    # لو أول مرة يتسجل (مش تعديل)
    if not instance.pk:
        return

    try:
        previous = Application.objects.get(pk=instance.pk)
    except Application.DoesNotExist:
        return

    # لو الحالة اتغيرت
    if previous.status != instance.status and instance.user:
        message = f"Your Application Status Has Changed '{instance.job.title}' To: {instance.get_status_display()}"

        # بناء رابط صفحة الوظيفة (تأكد إن عندك URL اسمه job_detail)
        job_detail_url = reverse('job_detail', kwargs={'job_id': instance.job.id})

        # إنشاء الإشعار
        Notification.objects.create(
            user=instance.user,
            message=message,
            link=job_detail_url
        )
