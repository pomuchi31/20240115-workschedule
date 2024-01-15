from django import forms
from .models import PersonalinfoModel, ShiftAvailability, SurveyCalendar, ForbiddenPair
from .models import DefinitionDate
from django.core.exceptions import ValidationError

class PersonalinfoModelForm(forms.ModelForm):
    class Meta:
        model = PersonalinfoModel
        fields = ["item1", "item2", "item3", "item4","item5","item6","item7","item8"]

        
class ShiftAvailabilityForm(forms.ModelForm):
    class Meta:
        model = ShiftAvailability
        fields = [
            'date',
            'on_call_available',
            'on_call_comments',
            'on_call_external_hospital',
            'on_call_external_hospital_comments',
        ]

class SurveyCalendarForm(forms.ModelForm):
    class Meta:
        model = SurveyCalendar
        fields = ["date", "item1", "item2", "item3", "item4","item5","item6","item7","item8"]




class ForbiddenPairForm(forms.ModelForm):

    class Meta:
        model = ForbiddenPair
        fields = [ "user" ]

    def clean(self):
        if "user" not in self.cleaned_data:
            raise ValidationError("ユーザーが指定されていません")
        
        selected = self.cleaned_data["user"]

        if len(selected) != 2:
            raise ValidationError("2人のユーザーが指定されていません")
        
        print(selected)

        forbidden_pairs = ForbiddenPair.objects.all()

        print("現在記録されているデータ")
        print( forbidden_pairs )

        for s in selected:
            forbidden_pairs = [ forbidden_pair for forbidden_pair in forbidden_pairs if s in forbidden_pair.user.all() ]

        if len(forbidden_pairs) > 0:
            raise ValidationError("この組み合わせはすでに存在します。")
        
        return self.cleaned_data
    
class DateSearchForm(forms.Form):

    start   = forms.DateTimeField()
    end     = forms.DateTimeField()

    
    # Date型に変換。
    def clean(self):
        cleaned_data = super().clean()
        
        # 任意の値を設定
        cleaned_data["start"]   = cleaned_data["start"].date()
        cleaned_data["end"]     = cleaned_data["end"].date()

        return cleaned_data
    
class DefinitionDateForm(forms.ModelForm):
    class Meta:
        model   = DefinitionDate
        fields  = [ "start","end" ]