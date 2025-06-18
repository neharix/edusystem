import os
import shutil
import tempfile
import zipfile

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Загружает данные из zip-архива и копирует медиафайлы"

    def add_arguments(self, parser):
        parser.add_argument("zip_path", type=str, help="Путь к архиву .zip")
        parser.add_argument(
            "--app",
            type=str,
            default="all",
            help="Имя приложения (например bmdu или mmu), либо all",
        )

    def handle(self, *args, **options):
        zip_path = options["zip_path"]
        app_name = options["app"]

        if not os.path.exists(zip_path):
            self.stderr.write(self.style.ERROR(f"Файл {zip_path} не найден."))
            return

        with tempfile.TemporaryDirectory() as tmpdir:
            with zipfile.ZipFile(zip_path, "r") as archive:
                archive.extractall(tmpdir)
                self.stdout.write(self.style.SUCCESS("Архив распакован"))

            media_archive_path = os.path.join(tmpdir, "media_files.zip")

            # Всегда лоадим auth_user и main_profile
            priority_files = ["auth_user.json", "main_profile.json"]
            loaded_files = set()

            for filename in priority_files:
                filepath = os.path.join(tmpdir, filename)
                if os.path.exists(filepath):
                    call_command("loaddata", filepath)
                    self.stdout.write(self.style.SUCCESS(f"Загружено: {filename}"))
                    loaded_files.add(filename)

            # Загружаем остальные, если соответствуют выбранному приложению
            match app_name:
                case "all":
                    load_quene = (
                        "main_country.json",
                        "main_nationality.json",
                        "main_region.json",
                        "bmdu_api_classificator.json",
                        "bmdu_api_degree.json",
                        "bmdu_api_highschool.json",
                        "bmdu_api_faculty.json",
                        "bmdu_api_department.json",
                        "bmdu_api_specialization.json",
                        "bmdu_api_highschoolfaculty.json",
                        "bmdu_api_facultydepartment.json",
                        "bmdu_api_departmentspecialization.json",
                        "bmdu_api_student.json",
                        "bmdu_api_diplomareport.json",
                        "bmdu_api_diplomarequest.json",
                        "bmdu_api_diplomarequestaction.json",
                        "bmdu_api_expulsionreason.json",
                        "bmdu_api_expulsionrequest.json",
                        "bmdu_api_reinstaterequest.json",
                        "bmdu_api_teacherstatement.json",
                        "bmdu_api_annualupdatereport.json",
                        # FIXME
                        "mmu_api_region.json",
                        "mmu_api_country.json",
                        "mmu_api_achievement.json",
                        "mmu_api_actionlog.json",
                        "mmu_api_certificate.json",
                        "mmu_api_course.json",
                        "mmu_api_direction.json",
                        "mmu_api_educationcenter.json",
                        "mmu_api_file.json",
                        "mmu_api_nationality.json",
                        "mmu_api_parent.json",
                        "mmu_api_specialization.json",
                        "mmu_api_staff.json",
                        "mmu_api_student.json",
                    )
                case "bmdu":
                    load_quene = (
                        "main_country.json",
                        "main_nationality.json",
                        "main_region.json",
                        "bmdu_api_classificator.json",
                        "bmdu_api_degree.json",
                        "bmdu_api_highschool.json",
                        "bmdu_api_faculty.json",
                        "bmdu_api_department.json",
                        "bmdu_api_specialization.json",
                        "bmdu_api_highschoolfaculty.json",
                        "bmdu_api_facultydepartment.json",
                        "bmdu_api_departmentspecialization.json",
                        "bmdu_api_student.json",
                        "bmdu_api_diplomareport.json",
                        "bmdu_api_diplomarequest.json",
                        "bmdu_api_diplomarequestaction.json",
                        "bmdu_api_expulsionreason.json",
                        "bmdu_api_expulsionrequest.json",
                        "bmdu_api_reinstaterequest.json",
                        "bmdu_api_teacherstatement.json",
                        "bmdu_api_annualupdatereport.json",
                    )
                case "mmu":
                    load_quene = (
                        "mmu_api_region.json",
                        "mmu_api_country.json",
                        "mmu_api_achievement.json",
                        "mmu_api_actionlog.json",
                        "mmu_api_certificate.json",
                        "mmu_api_course.json",
                        "mmu_api_direction.json",
                        "mmu_api_educationcenter.json",
                        "mmu_api_file.json",
                        "mmu_api_nationality.json",
                        "mmu_api_parent.json",
                        "mmu_api_specialization.json",
                        "mmu_api_staff.json",
                        "mmu_api_student.json",
                    )

            for filename in load_quene:
                if filename in loaded_files:
                    continue  # Уже загружен

                app_prefix = filename.split("_")[0]

                if app_name == "all" or app_name == app_prefix:
                    filepath = os.path.join(tmpdir, filename)
                    try:
                        call_command("loaddata", filepath)
                        self.stdout.write(self.style.SUCCESS(f"Загружено: {filename}"))
                    except Exception as e:
                        self.stderr.write(
                            self.style.ERROR(f"Ошибка при загрузке {filename}: {e}")
                        )

            # FIXME
            if os.path.exists(media_archive_path):
                self.stdout.write("Начинается распаковка медиафайлов...")
                with zipfile.ZipFile(media_archive_path, "r") as media_zip:
                    for file_info in media_zip.infolist():
                        target_path = os.path.join(
                            settings.MEDIA_ROOT, file_info.filename
                        )

                        # Пропуск если файл уже есть
                        if os.path.exists(target_path):
                            self.stdout.write(
                                self.style.WARNING(
                                    f"Файл уже существует и будет пропущен: {file_info.filename}"
                                )
                            )
                            continue

                        # Создать директории, если нужно
                        os.makedirs(os.path.dirname(target_path), exist_ok=True)

                        # Скопировать файл
                        with (
                            media_zip.open(file_info) as source,
                            open(target_path, "wb") as target,
                        ):
                            shutil.copyfileobj(source, target)

                    self.stdout.write(
                        self.style.SUCCESS("Медиафайлы успешно извлечены.")
                    )
            else:
                self.stdout.write(
                    self.style.WARNING("В архиве не найден файл media_backup.zip")
                )

        self.stdout.write(self.style.SUCCESS("Команда завершена."))
