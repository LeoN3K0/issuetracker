from .forms import TicketEditForm


def close_form_processor(request):
     edit_form = TicketEditForm
     return {'edit_form': edit_form}