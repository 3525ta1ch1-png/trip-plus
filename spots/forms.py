from django import forms
from .models import Spot, Review

SEP = "/"

STAR_CHOICES = [
    (5, "★★★★★"),
    (4, "★★★★☆"),
    (3, "★★★☆☆"),
    (2, "★★☆☆☆"),
    (1, "★☆☆☆☆"),
]


class SpotForm(forms.ModelForm):

    business_days = forms.MultipleChoiceField(
        choices=Spot.BUSINESS_DAY_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    mood_2 = forms.CharField(required=False, widget=forms.TextInput(attrs={"class":"form-input"}))
    mood_3 = forms.CharField(required=False, widget=forms.TextInput(attrs={"class":"form-input"}))

    purpose_2 = forms.CharField(required=False, widget=forms.TextInput(attrs={"class":"form-input"}))
    purpose_3 = forms.CharField(required=False, widget=forms.TextInput(attrs={"class":"form-input"}))

    time_axis_2 = forms.CharField(required=False, widget=forms.TextInput(attrs={"class":"form-input"}))
    time_axis_3 = forms.CharField(required=False, widget=forms.TextInput(attrs={"class":"form-input"}))

    language_2 = forms.CharField(required=False, widget=forms.TextInput(attrs={"class":"form-input"}))
    language_3 = forms.CharField(required=False, widget=forms.TextInput(attrs={"class":"form-input"}))

    class Meta:
        model = Spot
        fields = [
            "name",
            "address",
            "phone",
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
        
        if self.instance and self.instance.pk:
            def split3(val):
                parts = [p.strip() for p in (val or "").split(SEP) if p.strip()]
                parts += ["", "", ""]
                return parts[:3]

            m1,m2,m3 = split3(self.instance.mood)
            p1,p2,p3 = split3(self.instance.purpose)
            t1,t2,t3 = split3(self.instance.time_axis)
            l1,l2,l3 = split3(self.instance.language)
            self.fields["mood"].initial = m1
            self.fields["mood_2"].initial = m2
            self.fields["mood_3"].initial = m3

            self.fields["purpose"].initial = p1
            self.fields["purpose_2"].initial = p2
            self.fields["purpose_3"].initial = p3

            self.fields["time_axis"].initial = t1
            self.fields["time_axis_2"].initial = t2
            self.fields["time_axis_3"].initial = t3

            self.fields["language"].initial = l1
            self.fields["language_2"].initial = l2
            self.fields["language_3"].initial = l3
    def _join3(self, a, b, c):
        parts = [x.strip() for x in [a, b, c] if x and x.strip()]
        return SEP.join(parts)

    def clean(self):
        cleaned = super().clean()

        cleaned["mood"] = self._join3(cleaned.get("mood"), cleaned.get("mood_2"), cleaned.get("mood_3"))
        cleaned["purpose"] = self._join3(cleaned.get("purpose"), cleaned.get("purpose_2"), cleaned.get("purpose_3"))
        cleaned["time_axis"] = self._join3(cleaned.get("time_axis"), cleaned.get("time_axis_2"), cleaned.get("time_axis_3"))
        cleaned["language"] = self._join3(cleaned.get("language"), cleaned.get("language_2"), cleaned.get("language_3"))

        return cleaned

    def clean_business_days(self):
        return self.cleaned_data.get("business_days") or []


class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        label="評価",
        choices=STAR_CHOICES
    )

    class Meta:
        model = Review
        fields = ["rating", "comment"]


class WordSearchForm(forms.Form):
    mood = forms.CharField(
        required=False,
        label="気分",
        widget=forms.TextInput(attrs={"placeholder": "例：癒し、ワクワク"})
    )
    purpose = forms.CharField(
        required=False,
        label="目的",
        widget=forms.TextInput(attrs={"placeholder": "例：温泉、食べ歩き"})
    )
    time_axis = forms.CharField(
        required=False,
        label="時間軸",
        widget=forms.TextInput(attrs={"placeholder": "例：日帰り、朝活"})
    )
    language = forms.CharField(
        required=False,
        label="ワード",
        widget=forms.TextInput(attrs={"placeholder": "単語でフリーで入力"})
    )
