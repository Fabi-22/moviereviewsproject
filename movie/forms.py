from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["content", "watch_again"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 4}),
        }
