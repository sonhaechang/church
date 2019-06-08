from main.forms import SearchForm

def default(request):
    form = SearchForm()
    return {
        'search_form': form,
    }
