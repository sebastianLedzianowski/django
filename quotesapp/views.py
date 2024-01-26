from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Tag, Author, Quote
from .forms import TagForm, AuthorForm, QuoteForm
from django.contrib import messages

@login_required
def add_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You added a tag.')
            return redirect('home')
    else:
        form = TagForm()

    return render(request, 'quotesapp/tag_form.html', {'form': form})


def tag_detail(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    quotes_with_tag = tag.quote_set.all()
    context = {'tag': tag, 'quotes': quotes_with_tag}
    return render(request, 'quotesapp/tag_detail.html', context)

def top_tags(request):
    top_tags = Tag.objects.all().order_by('-quote__count')[:10]
    return render(request, {'top_tags': top_tags})


@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, 'You added a author.')
            return redirect('home')
    else:
        form = AuthorForm()

    return render(request, 'quotesapp/author_form.html', {'form': form})

def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    return render(request, 'quotesapp/author_detail.html', {'author': author})


@login_required
def add_quote(request):
    tags = Tag.objects.all()
    authors = Author.objects.all()

    if request.method == 'POST':
        form = QuoteForm(request.POST)

        if form.is_valid():
            new_quote = form.save()

            tag_id = request.POST.getlist('tags')
            author_id = request.POST.getlist('author')

            choice_tags = Tag.objects.filter(id__in=tag_id)
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)

            choice_authors = Author.objects.filter(id__in=author_id)
            new_quote.author = choice_authors[0]

            new_quote.save()

            messages.success(request, 'You added a quote.')
            return redirect('home')
    else:
        form = QuoteForm()

    return render(request, 'quotesapp/quote_form.html', {'form': form, 'tags': tags, 'authors': authors})




class QuoteDelete(LoginRequiredMixin, DeleteView):
    model = Quote
    template_name = 'quotesapp/quote_delete.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request, "The quote was deleted successfully.")
        return super(QuoteDelete, self).form_valid(form)

class QuoteUpdate(LoginRequiredMixin, UpdateView):
    model = Quote
    fields = ['author', 'tags', 'content']
    template_name = 'quotesapp/quote_update.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request, "The quote was updated successfully.")
        return super(QuoteUpdate, self).form_valid(form)

def home(request):
    quotes_list = Quote.objects.all()
    paginator = Paginator(quotes_list, 9)
    top_tags = Tag.objects.annotate(quote_count=Count('quote')).order_by('-quote_count')[:10]

    page = request.GET.get('page')
    try:
        quotes = paginator.page(page)
    except PageNotAnInteger:
        quotes = paginator.page(1)
    except EmptyPage:
        quotes = paginator.page(paginator.num_pages)

    return render(request, 'home.html', {'quotes': quotes, 'top_tags': top_tags})