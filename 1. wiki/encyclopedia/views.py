from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import EditForm, NewPageForm, SearchForm
from random import choice
from markdown2 import markdown

from . import util


search_form = SearchForm()


def index(request):
    '''Get start page of wiki'''

    params = {"form": search_form, "entries": util.list_entries()}
    return render(request, "encyclopedia/index.html", params)


def get_entry_page(request, title):
    '''Get page of single entry'''
    
    # Get content of page
    entry = util.get_entry(title)
  
    # If page exists
    if entry:
        # Convert content from markdown to HTML
        html_entry = markdown(entry)

        # Show the content of the page
        params = {"form": search_form, "text": html_entry, "title": title}
        return render(request, "encyclopedia/entry.html", params)
    
    else:
        # Show error page
        params = {"form": search_form, "error_message": "Page not found"}
        return render(request, "encyclopedia/error_page.html", params)
    

def search_page(request):
    '''Search wiki entry by its name'''

    # Get input
    search = SearchForm(request.POST)

    # Check if submitted form is valid
    if search.is_valid():

        # Handle the search query
        query = search.cleaned_data["query"].lower()

        all_entries = util.list_entries()

        # Get all possible titles
        possible_entries = list()
        for entry in all_entries:
            if query in entry.lower():
                possible_entries.append(entry)

        # Redirect to entry page, if quary was accurate
        if len(possible_entries) == 1 and query == possible_entries[0].lower():

            title = possible_entries[0]

            link = reverse("wiki:entry", args=[title])
            return redirect(link)
        
        # If there is no results, show error message
        elif len(possible_entries) == 0:

            params = {"form": search_form, "error_message": "No pages found"}
            return render(request, "encyclopedia/search_results.html", params)
        
        # If there are multiple results, show them all
        else:
            # If one of results is the right one, redirect user to its page
            for entry in possible_entries:
                if entry.lower() == query:
                    return get_entry_page(request, entry)

            params = {"form": search_form, "results": possible_entries}
            
            return render(request, "encyclopedia/search_results.html", params)
        
    else:
        return index(request)


def create_new_page(request):
    '''Create new entry page'''

    submitted_form = NewPageForm(request.POST or None)

    if request.method == "POST" and submitted_form.is_valid():
       
        # Get input form the submitted form
        title = submitted_form.cleaned_data["title"]
        content = submitted_form.cleaned_data["content"]

        all_entries = util.list_entries()
        
        # If an entry with given title already exists
        if title in all_entries:
            # Redirect user to the error page
            params = {"form": search_form, "error_message": "Entry with this name already exists"}
            return render(request, "encyclopedia/error_page.html", params)
        
        # Save the new entry to the disk
        else:
            util.save_entry(title, content)

            # Redirect user to the new entry page
            return get_entry_page(request, title)

    params = {"form": search_form, "new_page_form": NewPageForm}
    return render(request, "encyclopedia/new_page.html", params)


def edit_page(request):
    '''Edit an existing entry page'''

    # Get content of the page by its title
    title = request.POST.get("title")
    content = util.get_entry(title)

    # Pre-populate form with page content
    edit_form = EditForm(initial={"title": title, "content": content})

    # Redirect user to the editing page
    params = {"form": search_form, "edit_form": edit_form}
    return render(request, "encyclopedia/edit_page.html", params)


def save_edited_page(request):
    '''Save changes on an existing entry page'''

    # Get input from user
    submitted_form = EditForm(request.POST or None)

    if submitted_form.is_valid():

        title = submitted_form.cleaned_data["title"]
        content = submitted_form.cleaned_data["content"]

        # Save new page content
        util.save_entry(title, content)

        # Redirect user back to the editted entry
        return get_entry_page(request, title)
    
    # Redirect user back to the editing page if form is not valid
    else:
        params = {"form": search_form, "edit_form": submitted_form}
        return render(request, "encyclopedia/edit_page.html", params)
    

def get_random_page(request):
    '''Get random entry page'''

    # Get random entry title
    random_title = choice(util.list_entries())

    # Get link to that entry
    link = reverse("wiki:entry", args=[random_title])
    
    return redirect(link)
