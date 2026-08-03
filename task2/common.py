from collections import defaultdict
from pathlib import Path
from typing import Any
import json
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
)


def load_coco(annotation_path: Path) -> dict[str, Any]:
    """
    Загружает COCO-аннотации.
    """
    with annotation_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_coco(data: dict, output_path: Path) -> None:
    """
    Сохраняет COCO-аннотации.
    """
    with output_path.open("w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4,
        )


def get_categories(coco: dict) -> dict[int, str]:
    """
    Возвращает словарь:
    category_id -> category_name
    """
    return {
        category["id"]: category["name"]
        for category in coco["categories"]
    }


def get_images(coco: dict) -> list[dict]:
    """
    Возвращает список изображений.
    """
    return coco["images"]


def get_annotations(coco: dict) -> list[dict]:
    """
    Возвращает список аннотаций.
    """
    return coco["annotations"]


def get_image_annotations(coco: dict) -> dict[int, list[dict]]:
    """
    Группирует аннотации по image_id.
    """
    image_annotations = defaultdict(list)

    for annotation in coco["annotations"]:
        image_annotations[annotation["image_id"]].append(annotation)

    return image_annotations


def get_image_classes(coco: dict) -> dict[int, list[str]]:
    """
    Возвращает список классов для каждого изображения.
    """
    categories = get_categories(coco)
    image_annotations = get_image_annotations(coco)

    image_classes = {}

    for image_id, annotations in image_annotations.items():
        classes = {
            categories[annotation["category_id"]]
            for annotation in annotations
        }

        image_classes[image_id] = sorted(classes)

    return image_classes


def build_directory_name(classes: list[str]) -> str:
    """
    Формирует имя директории по классам.
    """
    if not classes:
        return "empty"

    return "_".join(classes)


def create_directory(path: Path) -> None:
    """
    Создает директорию.
    """
    path.mkdir(
        parents=True,
        exist_ok=True,
    )


def find_image_path(images_root: Path, file_name: str) -> Path:
    """
    Ищет изображение рекурсивно.
    """
    image_name = Path(file_name).name

    for path in images_root.rglob(image_name):
        return path

    return images_root / image_name
