from django import forms
from .models import Event,EventCategory,Category

class EventForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'category-checkbox'}),
        required=False,
        label='Categories',
    )

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['categories'].widget.choices = [(category.category_id, category.name) for category in Category.objects.all()]

    class Meta:
        model = Event
        fields = ['name', 'description','start_datetime' ,'end_datetime' ,'quantity_left', 'location', 'image']

    def clean_quantity_left(self):
        quantity_left = self.cleaned_data.get('quantity_left')
        if quantity_left and quantity_left < 0:
            raise forms.ValidationError("Quantity left must be a non-negative value.")
        return quantity_left

    def clean_end_date(self):
        start_datetime = self.cleaned_data.get('start_datetime')
        end_datetime = self.cleaned_data.get('end_datetime')
        if start_datetime and end_datetime and start_datetime >= end_datetime:
            raise forms.ValidationError("End date must be later than the start date.")
        return end_datetime
