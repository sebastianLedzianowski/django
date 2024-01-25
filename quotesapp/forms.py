from django.db.models import TextField
from django.forms import ModelForm, ModelChoiceField, CharField, TextInput, ModelMultipleChoiceField
from .models import Quote, Tag, Author


class AuthorForm(ModelForm):
    fullname = CharField(max_length=100,)
    born_date = CharField(required=False, max_length=50)
    born_location = CharField(max_length=100, required=False, widget=TextInput())
    content = TextField()

    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'content']

class QuoteForm(ModelForm):
    content = CharField(required=True)
    author = ModelChoiceField(queryset=Author.objects.all())
    tags = ModelMultipleChoiceField(queryset=Tag.objects.all(), required=True)

    class Meta:
        model = Quote
        fields = ['content', 'author', 'tags']

class TagForm(ModelForm):
    name = CharField(required=True, widget=TextInput())

    class Meta:
        model = Tag
        fields = ['name']
