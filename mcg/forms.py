from user.models import Enquiry
from django.forms import ModelForm


class EnquiryForm(ModelForm):
    class Meta:
        model = Enquiry
        fields = '__all__'

