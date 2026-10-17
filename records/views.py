from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from xml.sax.saxutils import escape
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import MedicalRecord


@login_required
def record_list(request):

    records = MedicalRecord.objects.filter(
        user=request.user
    ).order_by("-record_date")

    search_query = request.GET.get("search", "").strip()

    if search_query:
        records = records.filter(
            title__icontains=search_query
        )

    return render(
        request,
        "records/record_list.html",
        {
            "records": records,
            "search_query": search_query,
        }
    )


@login_required
def add_record(request):
    if request.method == "POST":
        MedicalRecord.objects.create(
            user=request.user,
            title=request.POST["title"],
            record_date=request.POST["record_date"],
            description=request.POST["description"],
        )

        return redirect("record_list")

    return render(request, "records/add_record.html")


@login_required
def edit_record(request, id):
    record = get_object_or_404(
        MedicalRecord,
        id=id,
        user=request.user
    )

    if request.method == "POST":
        record.title = request.POST["title"]
        record.record_date = request.POST["record_date"]
        record.description = request.POST["description"]

        record.save()

        return redirect("record_list")

    return render(
        request,
        "records/edit_record.html",
        {"record": record}
    )


@login_required
def delete_record(request, id):
    record = get_object_or_404(
        MedicalRecord,
        id=id,
        user=request.user
    )

    if request.method == "POST":
        record.delete()
        return redirect("record_list")

    return render(
        request,
        "records/delete_record.html",
        {"record": record}
    )

@login_required
def download_records_pdf(request):

    records = MedicalRecord.objects.filter(
        user=request.user
    ).order_by("-record_date")

    response = HttpResponse(
        content_type="application/pdf"
    )

    response["Content-Disposition"] = (
        'attachment; filename="MediSync_Medical_Records.pdf"'
    )

    pdf = SimpleDocTemplate(
        response,
        pagesize=A4
    )

    styles = getSampleStyleSheet()
    content = []

    content.append(
        Paragraph("MediSync - Medical Records", styles["Title"])
    )

    content.append(Spacer(1, 20))

    if records.exists():

        for record in records:

            content.append(
                Paragraph(
                    escape(record.title),
                    styles["Heading2"]
                )
            )

            content.append(
                Paragraph(
                    f"Date: {escape(str(record.record_date))}",
                    styles["Normal"]
                )
            )

            description = record.description or "No description provided."

            content.append(
                Paragraph(
                    f"Description: {escape(description)}",
                    styles["Normal"]
                )
            )

            content.append(Spacer(1, 15))

    else:

        content.append(
            Paragraph(
                "No medical records available.",
                styles["Normal"]
            )
        )

    pdf.build(content)

    return response