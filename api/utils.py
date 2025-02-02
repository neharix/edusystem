from string import ascii_uppercase
from typing import List

from openpyxl.styles import Alignment, Border, Color, Font, PatternFill, Side
from openpyxl.utils import quote_sheetname
from openpyxl.workbook import Workbook
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.worksheet import Worksheet
from pandas.core.series import Series

from .models import *


def create_example(row_count: int, high_school: HighSchool) -> Workbook:
    wb = Workbook()
    wb.remove(wb.worksheets[0])

    font = Font(name="Times New Roman", size=11, color="000000")
    alignment = Alignment(
        horizontal="center", vertical="center", wrap_text=True, wrapText=True
    )
    bold_font = Font(name="Times New Roman", size=11, color="000000", bold=True)
    border = Border(
        left=Side(style="thin"),
        right=Side(style="thin"),
        top=Side(style="thin"),
        bottom=Side(style="thin"),
    )

    ws: Worksheet = wb.create_sheet("Maglumat")

    column_headers = [
        "T/B",
        "F.A.Aa",
        "Doglan senesi",
        "Jynsy",
        "Welaýaty",
        "Milleti",
        "Ýurdy",
        "Fakulteti",
        "Kafedrasy",
        "Hünari",
        "Kursy",
        "Töleg görnüşi",
        "Maşgala ýagdaýy",
        "Ýazgyda duran salgysy",
        "Öý, iş, mobil telefony",
        "Pasport seriýasy, belgisi",
        "Harby borç",
        "Okuwa giren senesi",
        "Bellikler",
    ]
    column_index = 0

    for column_id in ascii_uppercase[:19]:
        ws[f"{column_id}1"].value = column_headers[column_index]
        column_index += 1
        ws.column_dimensions[column_id].width = 20
        for row_id in range(1, row_count + 2):
            ws[f"{column_id}{row_id}"].border = border
            ws[f"{column_id}{row_id}"].alignment = alignment
            ws[f"{column_id}{row_id}"].font = bold_font if row_id == 1 else font
            ws.row_dimensions[row_id].height = 50

    ws.column_dimensions["A"].width = 5
    ws.column_dimensions["B"].width = 20

    # Faculty validation values
    index = 1
    faculty_ws: Worksheet = wb.create_sheet("Fakultetler")
    for faculty in high_school.faculties.all():
        faculty_ws[f"A{index}"].value = faculty.name
        index += 1

    # Department validation values
    index = 1
    department_ws: Worksheet = wb.create_sheet("Kafedralar")
    for department in high_school.departments.all():
        department_ws[f"A{index}"].value = department.name
        index += 1

    # Specialization validation values
    index = 1
    specialization_ws: Worksheet = wb.create_sheet("Hünarler")
    for specialization in high_school.specializations.all():
        specialization_ws[f"A{index}"].value = specialization.name
        index += 1

    # Country validation values
    index = 1
    country_ws: Worksheet = wb.create_sheet("Ýurtlar")
    for country in Country.objects.all():
        country_ws[f"A{index}"].value = country.name
        index += 1

    # Nationality validation values
    index = 1
    nationality_ws: Worksheet = wb.create_sheet("Milletler")
    for nationality in Nationality.objects.all():
        nationality_ws[f"A{index}"].value = nationality.name
        index += 1

    # Region validation values
    index = 1
    region_ws: Worksheet = wb.create_sheet("Welaýatlar")
    for region in Region.objects.all():
        region_ws[f"A{index}"].value = region.name
        index += 1

    # Gender validation values
    gender_ws: Worksheet = wb.create_sheet("Jynslar")
    gender_ws["A1"].value = "Oglan"
    gender_ws["A2"].value = "Gyz"

    # Family status validation values
    family_status_ws: Worksheet = wb.create_sheet("Maşgala ýagdaýlary")
    family_status_ws["A1"].value = "Hossarly"
    family_status_ws["A2"].value = "Ýarym ýetim"
    family_status_ws["A3"].value = "Doly ýetim"
    family_status_ws["A4"].value = "Ýetimler öýünde ösen"

    # Payment type validation values
    payment_type_ws: Worksheet = wb.create_sheet("Töleg görnüşleri")
    payment_type_ws["A1"].value = "Tölegli"
    payment_type_ws["A2"].value = "Býudjet"

    faculty_data_val = DataValidation(
        type="list",
        formula1=f"={quote_sheetname('Fakultetler')}!$A:$A",
    )
    department_data_val = DataValidation(
        type="list",
        formula1=f"={quote_sheetname('Kafedralar')}!$A:$A",
    )
    specialization_data_val = DataValidation(
        type="list",
        formula1=f"={quote_sheetname('Hünarler')}!$A:$A",
    )
    country_data_val = DataValidation(
        type="list",
        formula1=f"={quote_sheetname('Ýurtlar')}!$A:$A",
    )
    nationality_data_val = DataValidation(
        type="list",
        formula1=f"={quote_sheetname('Milletler')}!$A:$A",
    )
    region_data_val = DataValidation(
        type="list",
        formula1=f"={quote_sheetname('Welaýatlar')}!$A:$A",
    )
    gender_data_val = DataValidation(
        type="list",
        formula1=f"={quote_sheetname('Jynslar')}!$A:$A",
    )
    family_status_data_val = DataValidation(
        type="list",
        formula1=f"={quote_sheetname('Maşgala ýagdaýlary')}!$A:$A",
    )
    payment_type_data_val = DataValidation(
        type="list",
        formula1=f"={quote_sheetname('Töleg görnüşleri')}!$A:$A",
    )

    ws.add_data_validation(faculty_data_val)
    ws.add_data_validation(department_data_val)
    ws.add_data_validation(specialization_data_val)
    ws.add_data_validation(country_data_val)
    ws.add_data_validation(nationality_data_val)
    ws.add_data_validation(region_data_val)
    ws.add_data_validation(gender_data_val)
    ws.add_data_validation(family_status_data_val)
    ws.add_data_validation(payment_type_data_val)
    for row_index in range(2, row_count + 2):
        ws[f"A{row_index}"].value = row_index - 1
        faculty_data_val.add(ws[f"H{row_index}"])
        department_data_val.add(ws[f"I{row_index}"])
        specialization_data_val.add(ws[f"J{row_index}"])
        country_data_val.add(ws[f"G{row_index}"])
        region_data_val.add(ws[f"E{row_index}"])
        gender_data_val.add(ws[f"D{row_index}"])
        family_status_data_val.add(ws[f"M{row_index}"])
        nationality_data_val.add(ws[f"F{row_index}"])
        payment_type_data_val.add(ws[f"L{row_index}"])

    return wb


def validate_not_null_field(row: Series, excepted_fields: List[str]):
    not_valid_fields = []

    for key in row.keys():
        if row.isnull()[key]:
            if not key in excepted_fields:
                not_valid_fields.append(key)

    return (False, not_valid_fields) if len(not_valid_fields) > 0 else (True, [])
