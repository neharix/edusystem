import datetime
import io
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

from ...utils import get_global_models

MODELS = get_global_models()

class Command(BaseCommand):

    help = "Выгружает данные в zip-архив и архивирует медиафайлы"

    def handle(self, *args, **options):
        try:
            outputs = []
            env = os.environ.copy()
            env["PYTHONUTF8"] = "1"
            for model in MODELS:
                outputs.append(
                    subprocess.check_output(
                        [
                            sys.executable,
                            "manage.py",
                            "dumpdata",
                            model,
                            "--natural-foreign",
                            "--natural-primary",
                            "--indent",
                            "2",
                        ],
                        stderr=subprocess.STDOUT,
                        text=True,
                        encoding="utf-8",
                        env=env,
                    )
                    .encode("utf-8", "ignore")
                    .decode("utf-8")
                )

            buffer = io.BytesIO()

            with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                for i, data in enumerate(outputs):
                    filename = f"{MODELS[i].replace('.', '_').lower()}.json"
                    zip_file.writestr(filename, data)

                media_buffer = io.BytesIO()
                with zipfile.ZipFile(
                    media_buffer, "w", zipfile.ZIP_DEFLATED
                ) as media_zip:
                    media_root = settings.MEDIA_ROOT
                    for root, dirs, files in os.walk(media_root):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, media_root)
                            media_zip.write(file_path, arcname)

                media_buffer.seek(0)
                zip_file.writestr("media_backup.zip", media_buffer.read())

            buffer.seek(0)
            with open(f"edusystem-dump-{datetime.datetime.now().strftime('%d-%m-%Y-%H%M%S')}.zip", "wb") as output_file:
                output_file.write(buffer.read())
    
            self.stdout.write(self.style.SUCCESS("Команда завершена."))


        except subprocess.CalledProcessError as e:
            self.stdout.write(self.style.ERROR(f"Ошибка выполнения: {e.output}"))


