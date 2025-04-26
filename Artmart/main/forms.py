from django import forms

class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=400, widget=forms.TextInput(attrs={
        'placeholder': 'Mr. Harry',
        'class': 'wpcf7-form-control wpcf7-text wpcf7-validates-as-required',
    }))
    email = forms.EmailField(max_length=400, widget=forms.EmailInput(attrs={
        'placeholder': 'info@example.com',
        'class': 'wpcf7-form-control wpcf7-email wpcf7-validates-as-required wpcf7-validates-as-email',
    }))
    message = forms.CharField(max_length=2000, widget=forms.Textarea(attrs={
        'placeholder': 'Write your message',
        'class': 'wpcf7-form-control wpcf7-textarea',
    }))
