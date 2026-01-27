from django import forms
from .models import Spot, Review

class SpotForm(forms.ModelForm):
    class Meta:
        model = Spot
        fields = ["name", "address", "image","language", "mood", "purpose", "start_at", "end_at",]
        widgets = {
            "start_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]

class WordSearchForm(forms.Form):
    mood = forms.CharField(required=False, label="気分",widget=forms.TextInput(attrs={"placeholder": "例：癒し、ワクワク",}),)
    purpose = forms.CharField(required=False, label="目的",widget=forms.TextInput(attrs={"placeholder": "例：温泉、食べ歩き",}),)
    language = forms.CharField(required=False, label="言語",widget=forms.TextInput(attrs={"placeholder": "例：日本語、英語",}),)

    start_at = forms.DateTimeField(
        required=False,
        label="開始時間",
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
        input_formats=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"],

    )
    end_at = forms.DateTimeField(
        required=False,
        label="終了時間",
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
        input_formats=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"],
    )