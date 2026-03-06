from django import forms
from .models import DestinationReview


class DestinationReviewForm(forms.ModelForm):
    class Meta:
        model = DestinationReview
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.NumberInput(attrs={"min": 1, "max": 5, "class": "form-control"}),
            "comment": forms.Textarea(
                attrs={"rows": 3, "class": "form-control", "placeholder": "اكتب تعليقك (اختياري)"}
            ),
        }
