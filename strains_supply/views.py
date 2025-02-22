from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect, render
from django.core.exceptions import PermissionDenied
from django.contrib import messages

from strains_supply import utils
from strains_supply.models import SupplyContent
from strains_supply import services
from strains_supply import utils

from .forms import (
    ReceiveForm,
    RemarkForm,
    SourceForm,
    DestForm,
    SuggestingDataForm,
    SupplyContentFormSet,
    SupplyForm,
    DeleteSupplyForm,
)


def _redirect_back(request):
    return "back" in request.POST


def supply_main(request):
    supply_list = services.get_newest_supply_for_user(request.user, limit=10)
    return render(
        request,
        "strains_supply/supply_main.html",
        {"supply_list": supply_list},
    )


def choose_sourse(request):
    if request.method == "POST":
        form = SourceForm(request.POST)
        if form.is_valid():
            source = services.choose_supply_source(
                inserted_by=request.user, **form.cleaned_data
            )
            request.session["source_id"] = source.id
            return redirect(reverse("choose_dest"))
    else:
        initial = utils.extract_from_session(request.session, ["source_id"])
        print(initial)
        form = SourceForm(initial=initial)
    return render(request, "strains_supply/supply_new.html", {"form": form, "step": 1})


def choose_dest(request):
    if request.method == "POST":
        form = DestForm(request.POST)
        if form.is_valid():
            dest = services.choose_supply_dest(
                inserted_by=request.user, **form.cleaned_data
            )
            request.session["dest_id"] = dest.id
            if not _redirect_back(request):
                return redirect(reverse("add_suggesting_data"))
        if _redirect_back(request):
            return redirect("choose_source")
    else:
        initial = utils.extract_from_session(request.session, ["dest_id"])
        form = DestForm(initial=initial)
    return render(
            request, "strains_supply/supply_new.html", {"form": form, "step": 2}
        )


def add_suggesting_data(request):
    if request.method == "POST":
        form = SuggestingDataForm(request.POST)
        if form.is_valid():
            suggested_sent_date = form.cleaned_data["suggested_sent_date"]
            if suggested_sent_date:
                suggested_sent_date = suggested_sent_date.isoformat()
            request.session["suggested_sent_date"] = suggested_sent_date
            request.session["suggested_num"] = form.cleaned_data["suggested_num"]
            if not _redirect_back(request):
                return redirect("confirm_supply_creating")
        if _redirect_back(request):
            return redirect("choose_dest")
    else:
        initial = utils.extract_from_session(
            request.session, ["suggested_sent_date", "suggested_num"]
        )
        form = SuggestingDataForm(initial=initial)
        return render(
            request, "strains_supply/supply_new.html", {"form": form, "step": 3}
        )


def confirm_supply_creating(request):
    if request.method == "POST":
        form = SupplyForm(request.POST)
        if form.is_valid():
            services.add_supply(model_form=form, inserted_by=request.user)

            if not _redirect_back(request):
                return redirect("supply_main")
        if _redirect_back(request):
            return redirect("add_suggesting_data")
    else:
        initial = utils.extract_from_session(
            request.session, ["source_id", "dest_id", "suggested_sent_date", "suggested_num"]
        )
        initial["source"] = services.get_source(source_id=initial["source_id"])
        initial["dest"] = services.get_dest(dest_id=initial["dest_id"])
        form = SupplyForm(initial=initial)
        return render(
            request, "strains_supply/supply_new.html", {"form": form, "step": 4}
        )


# def supply_new(request):
#     services.test_fu()
#     step = int(request.GET.get("step", "1"))
#     prev = None
#     if request.method == "POST":
#         if step == 1:
#             form = SourceForm(request.POST)
#             if form.is_valid():
#                 source = services_crud.get_or_create_source(
#                     inserted_by=request.user, **form.cleaned_data
#                 )
#                 return redirect(
#                     f"/strains_supply/new?step={step + 1}&source={source.id}"
#                 )
#         elif step == 2:
#             source_id = request.GET.get("source")
#             form = DestForm(request.POST)
#             if form.is_valid():
#                 dest = services.get_or_create_dest(
#                     inserted_by=request.user, **form.cleaned_data
#                 )
#                 return redirect(
#                     f"/strains_supply/new?step={step + 1}&source={source_id}&dest={dest.id}"
#                 )
#         elif step == 3:
#             params = utils.extract_get_param(request)
#             source_id = params["source"]
#             dest_id = params["dest"]
#             form = DetailForm(request.POST)
#             if form.is_valid():
#                 sent_date = form.cleaned_data["suggested_sent_date"]
#                 num = form.cleaned_data["suggested_num"]
#                 return redirect(
#                     f"/strains_supply/new?step={step + 1}&source={source_id}&dest={dest_id}&suggested_num={num}&suggested_sent_date={sent_date}"
#                 )

#         else:
#             form = SupplyForm(request.POST)
#             if form.is_valid():
#                 services.create_supply(
#                     source=form.cleaned_data["source"],
#                     dest=form.cleaned_data["dest"],
#                     suggested_sent_date=form.cleaned_data["suggested_sent_date"],
#                     suggested_num=form.cleaned_data["suggested_num"],
#                     inserted_by=request.user,
#                 )
#                 return redirect("/strains_supply/")
#     else:
#         if step == 1:
#             fields = {}
#             source = request.GET.get("source")
#             if source:
#                 fields["source_id"] = int(source)
#             form = SourceForm(initial=fields)
#         elif step == 2:
#             fields = {}
#             source = request.GET.get("source")
#             dest = request.GET.get("dest")
#             if dest:
#                 fields["dest_id"] = int(dest)
#             form = DestForm(initial=fields)
#             prev = f"/strains_supply/new?step={step - 1}&source={source}"  # TODO: generate url with function
#         elif step == 3:
#             source = request.GET.get("source")
#             dest = request.GET.get("dest")
#             prev = f"/strains_supply/new?step={step - 1}&source={source}&dest={dest}"  # TODO: generate url with function
#             fields = utils.extract_get_param(request)
#             form = DetailForm(initial=fields)
#         else:
#             step = 4
#             fields = utils.extract_get_param(request)

#             source = fields["source"]
#             dest = fields["dest"]
#             num = fields["suggested_num"]
#             sent_date = fields["suggested_sent_date"]
#             prev = f"/strains_supply/new?step={step - 1}&source={source}&dest={dest}&suggested_num={num}&suggested_sent_date={sent_date}"  # TODO: generate url with function
#             form = SupplyForm(initial=fields)

#     return render(
#         request,
#         "strains_supply/supply_add.html",
#         {"form": form, "step": step, "prev": prev},
#     )


def supply_edit(request, pk, step=1):
    supply = services.get_supply(supply_id=pk)
    if services.permissions.is_moderator(request.user):
        if request.method == "POST":
            form = SupplyForm(request.POST, instance=supply)
            if form.is_valid():
                form.save()  # TODO: move to services
                return redirect("supply_main")
        else:
            form = SupplyForm(instance=supply)
            return render(
                request,
                "strains_supply/supply_edit.html",
                {"supply": supply, "form": form},
            )
    if services.permissions.can_edit_supply_receiving(supply, request.user):
        if step == 1:
            if request.method == "POST":
                form = ReceiveForm(request.POST, instance=supply)
                if form.is_valid():
                    supply = services.receive_supply(
                        model_form=form, received_by=request.user
                    )
                    return redirect("supply_edit", pk=supply.pk, step=step + 1)
            else:
                form = ReceiveForm(instance=supply)
            return render(
                request,
                "strains_supply/receive_supply.html",
                {"supply": supply, "form": form, "step": step, "mode": "edit"},
            )
        elif step == 2:
            supply = services.get_supply(supply_id=pk)
            if request.method == "POST":
                formset = SupplyContentFormSet(request.POST)
                if formset.is_valid():
                    services.edit_supply_content(supply, formset)
                    return redirect("supply_edit", pk=supply.pk, step=step + 1)
            else:
                queryset = SupplyContent.objects.filter(supply=supply).all()
                formset = SupplyContentFormSet(queryset=queryset)
                formset.extra = 0
            return render(
                request,
                "strains_supply/receive_supply.html",
                {
                    "supply": supply,
                    "formset": formset,
                    "step": step,
                    "edit": True,
                    "mode": "edit",
                },
            )
        elif step == 3:
            supply = services.get_supply(supply_id=pk)
            if request.method == "POST":
                form = RemarkForm(request.POST, instance=supply)
                if form.is_valid():
                    services.add_supply_remark(model_form=form, updated_by=request.user)
                    return redirect("supply_main")
            else:
                form = RemarkForm()
            return render(
                request,
                "strains_supply/receive_supply.html",
                {"supply": supply, "form": form, "step": step},
            )
    else:
        raise PermissionDenied()


def supply_detail(request, pk):
    supply = services.get_supply(supply_id=pk)
    return render(request, "strains_supply/supply_detail.html", {"supply": supply})


def receive_supply(request, pk, step):
    supply = services.get_supply(supply_id=pk)
    if step == 1:
        if request.method == "POST":
            form = ReceiveForm(request.POST, instance=supply)
            if form.is_valid():
                supply = services.receive_supply(
                    model_form=form, received_by=request.user
                )
                return redirect("receive_supply", pk=supply.pk, step=step + 1)
        else:
            form = ReceiveForm()
        return render(
            request,
            "strains_supply/receive_supply.html",
            {"supply": supply, "form": form, "step": step},
        )
    elif step == 2:
        supply = services.get_supply(supply_id=pk)
        if request.method == "POST":
            formset = SupplyContentFormSet(request.POST)
            if formset.is_valid():
                # services.update_supplycontent(supply, formset)
                services.unpack_supply(supply, formset)
                return redirect("receive_supply", pk=supply.pk, step=step + 1)
        else:
            extra = SupplyContentFormSet.extra
            queryset = SupplyContent.objects.filter(supply=supply).all()
            formset = SupplyContentFormSet(
                queryset=queryset, initial=[{"supply": supply} for _ in range(extra)]
            )
        return render(
            request,
            "strains_supply/receive_supply.html",
            {
                "supply": supply,
                "formset": formset,
                "step": step,
            },
        )
    elif step == 3:
        supply = services.get_supply(supply_id=pk)
        if request.method == "POST":
            form = RemarkForm(request.POST, instance=supply)
            if form.is_valid():
                services.add_supply_remark(model_form=form, updated_by=request.user)
                return redirect("supply_main")
        else:
            form = RemarkForm()
        return render(
            request,
            "strains_supply/receive_supply.html",
            {"supply": supply, "form": form, "step": step},
        )


def supply_delete(request, pk):
    supply = services.get_supply(supply_id=pk)
    if request.method == "POST":
        form = DeleteSupplyForm(request.POST, instance=supply)
        if form.is_valid():
            services.delete_supply(model_form=form, deleted_by=request.user)
            messages.add_message(
                request, messages.INFO, f"Поставка {supply.pk} успешно удалена."
            )
            return redirect("supply_main")
    else:
        form = DeleteSupplyForm(instance=supply)
    return render(
        request, "strains_supply/supply_delete.html", {"form": form, "supply": supply}
    )
