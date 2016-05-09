from .forms import ContactForm


def add_contact_form(request):
    return {
        'contact_form': ContactForm()
    }
