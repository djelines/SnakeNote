from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.html import escape
from django.contrib import messages
from django.utils.text import slugify

from tasks.models import Collection, Task


# ----------------------------------------
# View: Display the homepage with collections and tasks
# ----------------------------------------
def index(request):
    """
    Display the homepage with the selected collection and its tasks.

    If a 'collection' slug is provided in the query parameters,
    display its tasks. Otherwise, show the default view.

    :param request: The HTTP request object.
    :return: Rendered HTML page based on the selected theme.
    """
    theme = getattr(request, 'theme', 'classique')  # 'classique' est ton thème de base

    collection_slug = request.GET.get("collection")
    collection = Collection.get_default_collection()

    if collection_slug:
        collection = get_object_or_404(Collection, slug=collection_slug)
        tasks = collection.task_set.order_by('description')
    else:
        collection = None
        tasks = None

    context = {
        'collections': Collection.objects.order_by('slug'),
        'collection': collection,
        'tasks': tasks,
        'theme': theme,
    }

    return render(request, f'tasks/{theme}.html', context=context)

# ----------------------------------------
# View: Add a new collection
# ----------------------------------------
def add(request):
    """
    Create a new collection based on user input.

    If the collection already exists, show a warning message.
    Otherwise, create it and show a success message.

    :param request: The HTTP request object with POST data.
    :return: Redirect to the home page.
    """
    collection_name = escape(request.POST.get('name'))
    collection, created = Collection.objects.get_or_create(name=collection_name, slug=slugify(collection_name))
    if not created:
        messages.warning(request, "La collection existe déjà.")
    else:
        messages.success(request, "Collection ajoutée avec succès.")
    return redirect('home')

# ----------------------------------------
# View: Add a new task to a collection
# ----------------------------------------
def add_task(request):
    """
    Add a new task to the selected collection.

    If no collection slug is provided, use the default collection.

    :param request: The HTTP request object with POST data.
    :return: Redirect to the home page with the selected collection.
    """
    # Récupérer le slug de la collection
    collection_slug = request.POST.get("collection-slug")

    if collection_slug:
        # Trouver la collection avec ce slug
        collection = get_object_or_404(Collection, slug=collection_slug)
    else:
        # Si aucun slug n'est fourni, on utilise la collection par défaut
        collection = Collection.get_default_collection()

    description = escape(request.POST.get("task-description"))

    if description:
        # Créer la tâche dans la collection sélectionnée
        Task.objects.create(collection=collection, description=description)

    # Rediriger vers la même page avec le slug de la collection
    return redirect(f"/?collection={collection.slug}")

# ----------------------------------------
# View: Delete a specific task
# ----------------------------------------
def delete_task(request, task_pk):
    """
    Delete a task by its primary key.

    :param request: The HTTP request object.
    :param task_pk: Primary key of the task to delete.
    :return: Redirect to the collection page.
    """
    task = get_object_or_404(Task, pk=task_pk)
    task.delete()
    return redirect(f"/?collection={task.collection.slug}")

# ----------------------------------------
# View: Delete a specific collection
# ----------------------------------------
def delete_collection(request, collection_pk):
    """
    Delete a collection by its primary key.

    Only allows deletion via POST request for safety.

    :param request: The HTTP request object.
    :param collection_pk: Primary key of the collection to delete.
    :return: Redirect to the home page.
    """
    if request.method == 'POST':
        collection = get_object_or_404(Collection, pk=collection_pk)
        collection.delete()
        return redirect('home')
    return redirect('home')