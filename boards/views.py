
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.db import models
from django.db.models import Case, F, When
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from boards.forms import BoardForm, ListForm, ListMoveForm, TaskDescForm, TaskForm, TaskMoveForm, RegisterForm
from boards.models import Board, List, Task
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Q

@login_required
def boards(request):
    query = request.GET.get("q")
    fill = request.GET.get("f")
    boards = Board.objects.all()
    if query:
        boards  = Board.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    return render(request, "boards/boards.html", {"boards": boards})

@login_required
def create_board(request):
    form = BoardForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        board = form.save()
        board.create_default_lists()
        return HttpResponse(
            status=204, headers={"HX-Redirect": board.get_absolute_url()}
        )

    return render(request, "boards/board_form.html", {"form": form})

@login_required
def board(request, board_uuid, partial=False):
    board = get_object_or_404(
        Board.objects.all().prefetch_related("lists__tasks"), uuid=board_uuid
    )
    template = "boards/_board.html" if partial else "boards/board.html"
    response = render(request, template, {"board": board})
    response["HX-Retarget"] = "#board"
    return response

@login_required
def delete_board(request, board_uuid):
    board = get_object_or_404(Board, uuid=board_uuid)
    print(f"delete_board {board.name}")

    if request.method == "POST":
        board.delete()
        response = boards(request)
        response.headers["HX-Refresh"] = "true"

    return response



@login_required
def create_list(request, board_uuid):
    board_ = get_object_or_404(Board, uuid=board_uuid)
    form = ListForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.instance.board = board_
        form.save()
        return board(request, board_uuid, partial=True)

    return render(request, "boards/board_form.html", {"form": form})

@login_required
def delete_list(request, board_uuid, list_uuid):
    list = get_object_or_404(List, uuid=list_uuid)

    if request.method == "POST":
        list.delete()

    return board(request, board_uuid, partial=True)




@login_required
def create_task(request, board_uuid, list_uuid):
    list = get_object_or_404(List, uuid=list_uuid)
    form = TaskForm(request.POST or None)
    print(form.is_valid())
    print(form.errors)
    if request.method == "POST" and form.is_valid():
        form.instance.list = list
        task = form.save()
        return board(request, board_uuid, partial=True)

    return render(request, "boards/board_form.html", {"form": form})

@login_required
def edit_task(request, board_uuid, task_uuid):
    task = get_object_or_404(Task, uuid=task_uuid)
    form = TaskForm(request.POST or None, instance=task)

    if request.method == "POST" and form.is_valid():
        task = form.save()
        return board(request, board_uuid, partial=True)

    return render(request, "boards/board_form.html", {"form": form})





@login_required

def preserve_order(uuids):
    return Case(
        *[When(uuid=uuid, then=o) for o, uuid in enumerate(uuids)],
        default=F("order"),
        output_field=models.IntegerField()
    )

@login_required
@require_POST
def list_move(request, board_uuid):
    form = ListMoveForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(str(form.errors))

    list_uuids = form.cleaned_data["list_uuids"]
    List.objects.filter(uuid__in=list_uuids).update(order=preserve_order(list_uuids))
    return board(request, board_uuid, partial=True)



@login_required
@require_POST
def task_move(request, board_uuid):
    form = TaskMoveForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(str(form.errors))

    from_list = form.cleaned_data["from_list"]
    to_list = form.cleaned_data["to_list"]
    task_uuids = form.cleaned_data["task_uuids"]
    item_uuid = form.cleaned_data["item"]

    if to_list == from_list:
        Task.objects.filter(uuid__in=task_uuids).update(
            order=preserve_order(task_uuids)
        )
    else:
        Task.objects.filter(uuid__in=task_uuids).update(
            order=preserve_order(task_uuids),
            list_id=List.objects.filter(uuid=to_list).order_by().values("id"),
        )

    return board(request, board_uuid, partial=True)



@login_required
def task_modal(request, task_uuid):
    task = get_object_or_404(Task.objects.select_related("list"), uuid=task_uuid)
    users = User.objects.all()
    form = TaskForm(request.POST or None, instance=task)
    is_manager = request.user.groups.filter(name="Manager").exists() 
    if request.method == "POST":
        if is_manager :
            form = TaskForm(request.POST, instance=task)
        else:
            form  = TaskDescForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save()
            print(task.time_estimate)
        return HttpResponse(status=204, headers={"HX-Refresh": "true"})


    if request.method =="DELETE":
        task.delete()
        return HttpResponse(status=204, headers={"HX-Refresh": "true"})
    return render(request, "boards/task_modal.html", {"task": task, "form": form, "users": users, })
    

def signup(request):
    # get user creation form and render it
    form = RegisterForm()
    if request.method == 'POST':
        # get the form with the data
        form = RegisterForm(request.POST)
        print(form.errors)
        # check if the form is valid
        if form.is_valid():
            # save the form
            print(form.cleaned_data)
            user = form.save()
            print(user)
            # login the user
            login(request, user)
            return redirect('boards:boards')
    return render(request, 'boards/signup.html', {'form': form})


@require_POST
def delete_task(request, task_uuid):
    task = get_object_or_404(Task, uuid=task_uuid)
    board_uuid = task.list.board.uuid

    if request.method == "POST":
        task.delete()

    refresh_url = reverse("boards:board", kwargs={"board_uuid": board_uuid})
    return HttpResponse(status=204, headers={"HX-Redirect": refresh_url})