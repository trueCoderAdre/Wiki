from django.core.files import utils
from django.shortcuts import render
from django.http.response import Http404, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
import random
import markdown2


from . import util
from .forms import CreateNewPageForm as CNPF
from encyclopedia import forms


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def article(request, title):
    art = util.get_entry(title)

    if art is None:
        return HttpResponseNotFound(render(request, "encyclopedia/error404.html",{
        "title": "Not found 404",
        "error404": "Page not found"
    }))

    return render(request, "encyclopedia/article.html", {
        "title": title,
        "article": markdown2.markdown(art)
    })

def search(request):
    names = util.list_entries()

    for name in names:
        if request.GET["q"].lower() == name.lower():
            return HttpResponseRedirect(reverse("encyclopedia:article", args=[name]))

    name_articles = []

    for name in names:
        if ((name.lower()).find(request.GET["q"].lower()) != -1):
            name_articles.append(name)
    
    return render(request, "encyclopedia/search.html", {
        "req": request.GET["q"],
        "name_articles": name_articles
    })

def create_new_page(request):
    if request.method == "POST":
        request.encoding = 'utf-8'
        cnpf = CNPF(request.POST)

        if cnpf.is_valid():
            titles_articles = util.list_entries()

            for title in titles_articles:
                if cnpf.cleaned_data["name_page"] == title:
                    return render(request, "encyclopedia/error_page.html", {
                        "title": cnpf.cleaned_data["name_page"],
                        "error_title": "Error Create New Page",
                        "error_head": "Error Create New Page",
                        "error": f"{cnpf.cleaned_data['name_page']} article already exist"
                    })

            util.save_entry(cnpf.cleaned_data["name_page"], cnpf.cleaned_data["content"])
            return HttpResponseRedirect(reverse("encyclopedia:article", args=[cnpf.cleaned_data["name_page"]]))

    return render(request, "encyclopedia/createnewpage.html", {
        "form": CNPF()
    })

def edit(request):
    if request.method == 'POST':
        title = request.POST["title"]

        form = forms.EditArticle(initial={'content': util.get_entry(title), 'title': title})
        # form.fields['content'].initial = util.get_entry(title)
        # form.initial['content'] = util.get_entry(title)

        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "form": form
        })

    return render(request, "encyclopedia/error_page.html", {
        "title": "Edit Page Error",
        "error_title": "Error Edit Page",
        "error_head": "Error Edit Page",
        "error": "Edit Page Error"
    })

def save_edit(request):
    if request.method == "POST":
        form = forms.EditArticle(request.POST)

        if form.is_valid():
            util.save_entry(form.cleaned_data['title'], form.cleaned_data['content'])
            return HttpResponseRedirect(reverse('encyclopedia:article', args=[form.cleaned_data['title']]))

    return render(request, "encyclopedia/error_page.html", {
        "title": "Save Edit Error",
        "error_title": "Error Save Edit Page",
        "error_head": "Error Save Edit Page",
        "error": "Save Edit error"
    })

def rand(request):
    names = util.list_entries()
    name = names[random.randint(0, len(names) - 1)]
    return HttpResponseRedirect(reverse('encyclopedia:article', args=[name]))


def pageNotFound(request, exception):
    return HttpResponseNotFound(render(request, "encyclopedia/error404.html",{
        "title": "Not found 404",
        "error404": "Page not found"
    }))
