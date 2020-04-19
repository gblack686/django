from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Comparable, Choice
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import NameForm

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'name.html', {'form': form})


class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'latest_comparable_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Comparable.objects.filter(
            entry_date__lte=timezone.now()
        ).order_by('-entry_date')[:5]


class DetailView(generic.DetailView):
    model = Comparable
    template_name = 'detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Comparable.objects.filter(entry_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Comparable
    template_name = 'results.html'


def vote(request, comparable_id):
    comparable = get_object_or_404(Comparable, pk=comparable_id)
    try:
        selected_choice = comparable.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'detail.html', {
            'comparable': comparable,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('comps:results', args=(comparable.id,)))