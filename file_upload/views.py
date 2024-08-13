from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
import pandas as pd
from .forms import UploadFileForm
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            df = pd.read_excel(file) if file.name.endswith('.xlsx') else pd.read_csv(file)
            summary =generate_summary(df)
            send_email(summary)
            
            return render(request, 'file_upload/upload.html', {'form': form, 'summary': summary})
    else:
        form = UploadFileForm()
    return render(request, 'file_upload/upload.html', {'form': form})

def send_email(summary):
    subject = 'Python Assignment - Your Name'
    html_message = render_to_string('file_upload/email_template.html', {'summary': summary})
    plain_message = strip_tags(html_message)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['ananttyagi1902@gmail.com', ]
    
    email = EmailMessage(
        subject=subject,
        body=plain_message,
        from_email=email_from,
        to=recipient_list
    )
    email.content_subtype = 'html'
    email.body = html_message  # Set the email content type to HTML
    email.send()

def generate_summary(df):
    # Modify this function to create the summary as per your requirements
    summary = df.describe().to_string()
    return summary