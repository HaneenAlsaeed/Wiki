import random
import markdown2
from django.shortcuts import render, redirect
from . import util 

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "This page does not exist."
        })
    
    lines = content.splitlines()
    if lines and lines[0].startswith("#"):
        content = "\n".join(lines[1:])
    
    html_content = markdown2.markdown(content)
    
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": html_content
    })

def new_page(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        if util.get_entry(title):
            return render(request, "encyclopedia/error.html", {
                "message": "Entry already exists!"
            })
        util.save_entry(title, content)
        return redirect("entry", title=title)
    return render(request, "encyclopedia/new_page.html")

def edit_page(request, title):
    if request.method == "POST":
        content = request.POST.get("content")
        util.save_entry(title, content)
        return redirect("entry", title=title)
    content = util.get_entry(title)
    return render(request, "encyclopedia/edit_page.html", {
        "title": title,
        "content": content
    })

def random_page(request):
    entries = util.list_entries()
    if entries:
        selected_page = random.choice(entries)
        return redirect("entry", title=selected_page)
    return redirect("index")

def search(request):
    query = request.GET.get("q", "")
    entries = util.list_entries()
    if query.lower() in [e.lower() for e in entries]:
        return redirect("entry", title=query)
    results = [e for e in entries if query.lower() in e.lower()]
    return render(request, "encyclopedia/index.html", {
        "entries": results,
        "search": True,
        "query": query
    })