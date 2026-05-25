from io import BytesIO
from pathlib import PurePosixPath

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from PIL import Image, ImageOps

from menu.models import Dish


class Command(BaseCommand):
    help = "Generate responsive WebP derivatives for dish images."

    def add_arguments(self, parser):
        parser.add_argument(
            "--widths",
            default="480,768,1200",
            help="Comma-separated output widths.",
        )
        parser.add_argument(
            "--quality",
            type=int,
            default=82,
            help="WebP quality, 1-100.",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Regenerate existing derivatives.",
        )

    def handle(self, *args, **options):
        widths = self._parse_widths(options["widths"])
        quality = max(1, min(options["quality"], 100))
        force = options["force"]
        generated = 0
        skipped = 0

        queryset = Dish.objects.filter(image__isnull=False).exclude(image="")
        for dish in queryset.iterator():
            try:
                result = self._process_dish(dish, widths, quality, force)
            except Exception as exc:
                self.stderr.write(self.style.WARNING(f"{dish.pk}: {exc}"))
                continue
            generated += result["generated"]
            skipped += result["skipped"]

        self.stdout.write(
            self.style.SUCCESS(
                f"Generated {generated} image derivatives; skipped {skipped} existing derivatives."
            )
        )

    def _parse_widths(self, value):
        widths = []
        for item in value.split(","):
            item = item.strip()
            if not item:
                continue
            width = int(item)
            if width <= 0:
                raise ValueError("Widths must be positive integers.")
            widths.append(width)
        return sorted(set(widths))

    def _process_dish(self, dish, widths, quality, force):
        storage = dish.image.storage
        original = PurePosixPath(dish.image.name)
        variant_dir = original.parent / "optimized"

        with dish.image.open("rb") as source:
            image = Image.open(source)
            image = ImageOps.exif_transpose(image)
            image.load()

        if image.mode not in ("RGB", "RGBA"):
            image = image.convert("RGB")

        generated = 0
        skipped = 0

        for width in widths:
            if image.width <= width:
                target = image.copy()
            else:
                ratio = width / image.width
                height = max(1, round(image.height * ratio))
                target = image.resize((width, height), Image.Resampling.LANCZOS)

            variant_name = str(variant_dir / f"{original.stem}-{width}.webp")
            if storage.exists(variant_name) and not force:
                skipped += 1
                target.close()
                continue

            buffer = BytesIO()
            target.save(buffer, format="WEBP", quality=quality, method=6)
            target.close()

            if storage.exists(variant_name) and force:
                storage.delete(variant_name)
            storage.save(variant_name, ContentFile(buffer.getvalue()))
            generated += 1

        image.close()
        return {"generated": generated, "skipped": skipped}
