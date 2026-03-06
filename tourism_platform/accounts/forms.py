from django import forms
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(
        label="كلمة المرور",
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label="تأكيد كلمة المرور",
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ("username", "email")

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")

        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("كلمتا المرور غير متطابقتين")

        return cleaned_data


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label="الاسم",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اسمك'})
    )
    email = forms.EmailField(
        label="البريد الإلكتروني",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'بريدك الإلكتروني'})
    )
    subject = forms.CharField(
        max_length=200,
        label="الموضوع",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'الموضوع'})
    )
    message = forms.CharField(
        label="الرسالة",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'رسالتك'})
    )
    
    def send_email(self):
        """Send contact email"""
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        subject = self.cleaned_data['subject']
        message = self.cleaned_data['message']
        
        full_message = f"من: {name} ({email})\n\n{message}"
        
        try:
            send_mail(
                f"تواصل: {subject}",
                full_message,
                email,
                [settings.DEFAULT_FROM_EMAIL or 'admin@tourism.local'],
                fail_silently=False,
            )
            return True
        except Exception as e:
            print(f"Email error: {e}")
            return False