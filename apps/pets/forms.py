from django import forms
from django.urls import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field

from .models import Pet


class PetUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-sm-2"
        self.helper.form_action = reverse(
            "pet_overview", kwargs={"pet_id": self.instance.id}
        )
        self.helper.layout = Layout(
            Fieldset("Basic Information", "name", "date_of_birth"),
            Fieldset(
                "Picture",
                "picture",
            ),
            ButtonHolder(Submit("submit", "Submit", css_class="btn btn-danger")),
        )

    date_of_birth = forms.DateField(
        widget=forms.TextInput(attrs={"type": "date"}), required=False
    )

    class Meta:
        model = Pet
        fields = ["name", "date_of_birth", "picture"]

    # class PetUpdateForm(forms.Form):
