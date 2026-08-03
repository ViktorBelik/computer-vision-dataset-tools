import argparse
import logging
from collections import defaultdict
from pathlib import Path

from tqdm import tqdm

from common import load_coco


def group_annotations_by_image(coco: dict) -> dict[int, list[dict]]:
    """
    Группирует аннотации по image_id.
    """
    grouped = defaultdict(list)

    for annotation in coco["annotations"]:
        grouped[annotation["image_id"]].append(annotation)

    return grouped


def get_category_mapping(coco: dict) -> dict[int, int]:
    """
    Преобразует category_id в индекс YOLO.
    """
    categories = sorted(
        coco["categories"],
        key=lambda category: category["id"],
    )

    return {
        category["id"]: index
        for index, category in enumerate(categories)
    }


def coco_bbox_to_yolo(
    bbox: list[float],
    image_width: int,
    image_height: int,
) -> tuple[float, float, float, float]:
    """
    Преобразует COCO bbox в YOLO.
    """
    x, y, width, height = bbox

    x_center = (x + width / 2) / image_width
    y_center = (y + height / 2) / image_height

    width /= image_width
    height /= image_height

    return (
        x_center,
        y_center,
        width,
        height,
    )


def save_yolo_annotation(
    output_path: Path,
    annotations: list[dict],
    category_mapping: dict[int, int],
    image_width: int,
    image_height: int,
) -> None:
    """
    Сохраняет YOLO-аннотацию.
    """
    with output_path.open("w", encoding="utf-8") as file:
        for annotation in annotations:
            class_id = category_mapping[
                annotation["category_id"]
            ]

            x, y, w, h = coco_bbox_to_yolo(
                annotation["bbox"],
                image_width,
                image_height,
            )

            file.write(
                f"{class_id} "
                f"{x:.6f} "
                f"{y:.6f} "
                f"{w:.6f} "
                f"{h:.6f}\n"
            )


def convert_dataset(
    images_directory: Path,
    annotation_path: Path,
) -> None:
    """
    Конвертирует COCO в YOLO.
    """
    coco = load_coco(annotation_path)

    grouped_annotations = group_annotations_by_image(coco)

    category_mapping = get_category_mapping(coco)

    for image in tqdm(coco["images"], desc="Converting"):
        annotation_path = (
            images_directory /
            Path(image["file_name"]).with_suffix(".txt")
        )

        save_yolo_annotation(
            annotation_path,
            grouped_annotations.get(image["id"], []),
            category_mapping,
            image["width"],
            image["height"],
        )

    logging.info("YOLO annotations created.")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert COCO to YOLO."
    )

    parser.add_argument(
        "--images",
        type=Path,
        required=True,
    )

    parser.add_argument(
        "--annotations",
        type=Path,
        required=True,
    )

    return parser.parse_args()


def main() -> None:
    args = parse_arguments()

    convert_dataset(
        args.images,
        args.annotations,
    )


if __name__ == "__main__":
    main()
