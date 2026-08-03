import argparse
import logging
import json
from pathlib import Path

from common import (
    find_image_path,
    get_annotations,
    get_categories,
    get_images,
    load_coco,
)


def validate_image_paths(images_directory: Path, images: list[dict]) -> list[str]:
    """
    Проверяет существование файлов изображений.
    """
    errors = []

    for image in images:
        image_path = find_image_path(
            images_directory,
            image["file_name"],
        )

        if not image_path.exists():
            errors.append(f"Image not found: {image['file_name']}")

    return errors


def validate_image_ids(images: list[dict], annotations: list[dict]) -> list[str]:
    """
    Проверяет существование image_id.
    """
    errors = []

    image_ids = {image["id"] for image in images}

    for annotation in annotations:
        if annotation["image_id"] not in image_ids:
            errors.append(
                f"Unknown image_id: {annotation['image_id']}"
            )

    return errors


def validate_category_ids(
    categories: dict[int, str],
    annotations: list[dict],
) -> list[str]:
    """
    Проверяет существование category_id.
    """
    errors = []

    category_ids = set(categories.keys())

    for annotation in annotations:
        if annotation["category_id"] not in category_ids:
            errors.append(
                f"Unknown category_id: {annotation['category_id']}"
            )

    return errors


def count_empty_images(
    images: list[dict],
    annotations: list[dict],
) -> int:
    """
    Подсчитывает количество изображений без аннотаций.
    """
    annotated_images = {
        annotation["image_id"]
        for annotation in annotations
    }

    return sum(
        image["id"] not in annotated_images
        for image in images
    )


def create_report(
    images: list[dict],
    annotations: list[dict],
    categories: dict[int, str],
    errors: list[str],
) -> dict:
    """
    Создает отчет.
    """
    return {
        "images": len(images),
        "annotations": len(annotations),
        "categories": len(categories),
        "empty_images": count_empty_images(images, annotations),
        "errors_count": len(errors),
        "errors": errors,
    }


def save_report(report: dict, output_path: Path) -> None:
    """
    Сохраняет отчет.
    """
    with output_path.open("w", encoding="utf-8") as file:
        json.dump(
            report,
            file,
            ensure_ascii=False,
            indent=4,
        )


def validate_dataset(
    images_directory: Path,
    annotation_path: Path,
    report_path: Path,
) -> None:
    """
    Проверяет целостность датасета.
    """
    coco = load_coco(annotation_path)

    images = get_images(coco)
    annotations = get_annotations(coco)
    categories = get_categories(coco)

    errors = []

    errors.extend(
        validate_image_paths(images_directory, images)
    )

    errors.extend(
        validate_image_ids(images, annotations)
    )

    errors.extend(
        validate_category_ids(categories, annotations)
    )

    report = create_report(
        images,
        annotations,
        categories,
        errors,
    )

    save_report(report, report_path)

    logging.info("=" * 50)
    logging.info("DATASET REPORT")
    logging.info("=" * 50)

    logging.info(f"Images: {report['images']}")
    logging.info(f"Annotations: {report['annotations']}")
    logging.info(f"Categories: {report['categories']}")
    logging.info(f"Empty images: {report['empty_images']}")
    logging.info(f"Errors: {report['errors_count']}\n")

    logging.info(f"Report saved to {report_path}")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Dataset validation."
    )

    parser.add_argument(
        "--images",
        type=Path,
        required=True,
        help="Directory with images.",
    )

    parser.add_argument(
        "--annotations",
        type=Path,
        required=True,
        help="Updated COCO annotation.",
    )

    parser.add_argument(
        "--report",
        type=Path,
        default=Path("data/report/dataset_report.json"),
        help="Report file.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_arguments()

    validate_dataset(
        images_directory=args.images,
        annotation_path=args.annotations,
        report_path=args.report,
    )


if __name__ == "__main__":
    main()
