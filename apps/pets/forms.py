from django import forms
from django.urls import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Button
from crispy_forms.bootstrap import FormActions, Accordion, AccordionGroup

from .models import Pet, HealthEvent, VetAppointment


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


class EventForm(forms.ModelForm):
    helper: FormHelper

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        if not self.helper.layout:
            self.helper.layout = Layout()

    class Meta:
        fields = ("date",)
        widgets = {"date": forms.DateTimeInput(attrs={"type": "datetime-local"})}


class EventUpdateForm(EventForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout.append(
            FormActions(
                Submit("save", "Save", css_class="btn btn-info"),
                Button("close", "Close without saving", css_class="btn btn-default"),
            )
        )


class VetAppointmentUpdateForm(EventUpdateForm):
    class Meta(EventForm.Meta):
        model = VetAppointment
        fields = EventForm.Meta.fields + ("location", "description", "notes")


class HealthEventUpdateForm(EventUpdateForm):
    class Meta(EventForm.Meta):
        model = HealthEvent
