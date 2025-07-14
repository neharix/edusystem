import os
import shutil
import tempfile
import zipfile

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.utils import timezone

from ...models import AnnualUpdateReport, Student


class Command(BaseCommand):
    help = "Перевод студентов в следующий курс"


    def handle(self, *args, **options):
        if not AnnualUpdateReport.objects.filter(updated_at__year=timezone.now().year):
            students = Student.objects.filter(is_obsolete=False, is_expelled=False)
            default_students = students.exclude(study_year__contains="DÖB")
            now = timezone.now()
            for idx, student in enumerate(default_students):
                try:
                    if student.study_year.isdigit():
                        if student.specialization.specialization.degree.duration == int(
                            student.study_year
                        ):
                            student.is_obsolete = True
                            student.graduated_in = now
                        else:
                            student.study_year = int(student.study_year) + 1
                    student.save()
                    self.stdout.write(self.style.NOTICE(f"Обновлено {idx + 1} студентов"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Ошибка при обновлении {idx + 1} студента (ID: {student.id}): {e}"))
                    break

            # Обновление курса бакалавров с языковым обучением
            students.filter(study_year__contains="DÖB").update(study_year="1")
            AnnualUpdateReport.objects.create()
            self.stdout.write(self.style.SUCCESS("Команда завершена."))
        else:
            self.stdout.write(self.style.WARNING(f"Уже обновлено в этом году"))
