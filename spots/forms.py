from django import forms
from .models import Spot, Review

class SpotForm(forms.ModelForm):

    business_days = forms.MultipleChoiceField(
        choices=Spot.BUSINESS_DAY_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Spot
        fields = [
            "name",
            "address",
            "phone",

            # 🔽 追加4つ（ここに挿入）
            "mood",
            "purpose",
            "time_axis",
            "language",

            "business_days",
            "open_time",
            "close_time",
            "parking",
            "access",
            "image",
            "website",
            "description",
        ]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-input"}),
            "address": forms.TextInput(attrs={"class": "form-input"}),
            "phone": forms.TextInput(attrs={"class": "form-input"}),

            "mood": forms.TextInput(attrs={"class": "form-input"}),
            "purpose": forms.TextInput(attrs={"class": "form-input"}),
            "time_axis": forms.TextInput(attrs={"class": "form-input"}),
            "language": forms.TextInput(attrs={"class": "form-input"}),

            "open_time": forms.TimeInput(attrs={"type": "time", "class": "form-input"}),
            "close_time": forms.TimeInput(attrs={"type": "time", "class": "form-input"}),
            "parking": forms.Select(attrs={"class": "select"}),

            "access": forms.TextInput(attrs={"class": "form-input"}),
            "website": forms.URLInput(attrs={"class": "form-input"}),
            "description": forms.Textarea(attrs={"class": "form-textarea"}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 既存データ（JSONのlist）をチェックボックスの初期値に
        if self.instance and self.instance.pk:
            self.fields["business_days"].initial = self.instance.business_days or []

    def clean_business_days(self):
        return self.cleaned_data.get("business_days") or []


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]

class WordSearchForm(forms.Form):
    mood = forms.CharField(required=False, label="気分",widget=forms.TextInput(attrs={"placeholder": "例：癒し、ワクワク",}),)
    purpose = forms.CharField(required=False, label="目的",widget=forms.TextInput(attrs={"placeholder": "例：温泉、食べ歩き",}),)
    time_axis = forms.CharField(required=False, label="時間軸",widget=forms.TextInput(attrs={"placeholder": "例：日帰り、朝活",}))
    language = forms.CharField(required=False, label="ワード",widget=forms.TextInput(attrs={"placeholder": "単語でフリーで入力",}),)
