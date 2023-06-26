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
        fields = ['name', 'description','start_datetime' ,'end_datetime' ,'standard','mid','vip','standard_left','mid_left','vip_left','location', 'image']

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
    
class EventUpdateForm(forms.ModelForm):
    name = forms.CharField(required=False)
    description = forms.CharField(required=False, widget=forms.Textarea)
    start_datetime = forms.DateTimeField(required=False)
    end_datetime = forms.DateTimeField(required=False)
    location = forms.CharField(required=False)
    image = forms.ImageField(required=False)
    standard = forms.DecimalField(required=False)
    mid = forms.DecimalField(required=False)
    vip = forms.DecimalField(required=False)
    standard_left = forms.IntegerField(required=False)
    mid_left = forms.IntegerField(required=False)
    vip_left = forms.IntegerField(required=False)
    status_choices = [
        ('finished', 'Finished'),
        ('cancelled', 'Cancelled'),
    ]
    status = forms.TypedChoiceField(choices=status_choices, required=False)
    
    class Meta:
        model = Event
        fields = ['name', 'description', 'start_datetime', 'end_datetime', 'location', 'image', 'standard',
                  'mid', 'vip', 'standard_left', 'mid_left', 'vip_left', 'status']


