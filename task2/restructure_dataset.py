import argparse
import shutil
import logging
from pathlib import Path

from tqdm import tqdm

from common import (
    build_directory_name,
    create_directory,
    find_image_path,
    get_image_classes,
    get_images,
    load_coco,
    save_coco,
)


def move_image(source, destination):

    if destination.exists():
        return

    create_directory(destination.parent)

    shutil.move(source, destination)


def update_image_path(image: dict, directory_name: str) -> None:
    """
    Обновляет file_name в COCO.
    """
    file_name = Path(image["file_name"]).name
    image["file_name"] = str(Path("images") / directory_name / file_name)


def restructure_dataset(
    images_directory: Path,
    annotation_path: Path,
    output_annotation_path: Path,
) -> None:
    """
    Перестраивает структуру датасета.
    """
    coco = load_coco(annotation_path)

    image_classes = get_image_classes(coco)

    images = get_images(coco)

    for image in tqdm(images, desc="Processing images"):
        image_id = image["id"]

        classes = image_classes.get(image_id, [])

        directory_name = build_directory_name(classes)

        source_path = find_image_path(
            images_directory,
            image["file_name"],
        )

        destination_directory = (
            images_directory / directory_name
        )

        destination_path = (
            destination_directory / source_path.name
        )

        if not source_path.exists():
            logging.info(f"Не найден файл {source_path}")
            continue
        move_image(source_path, destination_path)

        update_image_path(image, directory_name)

    save_coco(coco, output_annotation_path)

    logging.info("\nDataset successfully restructured.")
    logging.info("Updated annotation saved to:")
    logging.info(output_annotation_path)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="COCO dataset restructuring."
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
        help="COCO annotation file.",
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/annotations/updated_annotations.json"),
        help="Output annotation file.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_arguments()

    restructure_dataset(
        images_directory=args.images,
        annotation_path=args.annotations,
        output_annotation_path=args.output,
    )


if __name__ == "__main__":
    main()
