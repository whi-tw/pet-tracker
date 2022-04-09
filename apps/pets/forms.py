from django import forms
from django.urls import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from crispy_forms.bootstrap import FormActions, Accordion, AccordionGroup

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
            Accordion(
                AccordionGroup(
                    "Basic Information",
                    "name",
                    "date_of_birth",
                    "picture",
                ),
                AccordionGroup(
                    "Shouldn't really need to be changed!", "species", "breed", "sex"
                ),
            ),
            FormActions(Submit("submit", "Submit", css_class="btn btn-danger")),
        )

    class Meta:
        model = Pet
        fields = ["name", "date_of_birth", "picture", "species", "breed", "sex"]
        widgets = {"date_of_birth": forms.DateInput(attrs={"type": "date"})}
