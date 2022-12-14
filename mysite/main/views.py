from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import ToDoList, Item
from .forms import CreateNewList, AddItem
# http requests, and business logic goes here

def list(response, id):
    ls = ToDoList.objects.get(id=id)
    if response.method == 'POST':
        if response.POST.get("save"):
            for item in ls.item_set.all():
                if response.POST.get(f'c{item.id}') == "clicked":
                    item.complete = True
                else:
                    item.complete = False
                item.save()
        elif response.POST.get("newItem"):
            txt = response.POST.get("new")
            if len(txt) > 2:
                print(f'Item Set Type: {type(ls.item_set)}')
                ls.item_set.create(text=txt, complete=False)
            else:
                print(f'Invalid item: {txt}')

    #items = ls.item_set.all()
    return render(response, "main/list.html", {"ls":ls}) # used to pass in variables

def home(response):
    return render(response, "main/home.html", {})

def create(response):
    if response.method == 'POST':
        form = CreateNewList(response.POST) # dictionary of data attributes and values passed in
        if form.is_valid():
            name = form.cleaned_data["name"]
            t = ToDoList(name=name)
            t.save()

        return HttpResponseRedirect(f"/{t.id}") # redirect to newly created to do list
    else:
        form = CreateNewList()
    return render(response, "main/create.html", {"form":form})