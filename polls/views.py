from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
            Return the last five published questions (not including those set to be
            published in the future).
            """
        return Question.objects.filter(
            publication_date__lte=timezone.now()
        ).order_by('-publication_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get(self, request, *args, **kwargs):
        try:
            self.object = Question.objects.filter(pk=kwargs['pk'])[0]
        except:
            messages.error(request, f"Poll {kwargs['pk']} does not exist")
            return HttpResponseRedirect(reverse('polls:index'))

        if not self.object.can_vote():
            messages.error(request, f'Voting is not allowed for question "{self.object.question_text}"')
            return HttpResponseRedirect(reverse('polls:index'))

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
