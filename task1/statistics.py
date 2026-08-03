from pathlib import Path
import logging
import argparse

from common import (
    collect_all_images,
    count_all_shapes,
    find_largest_images,
    find_smallest_images,
    get_image_size,
    get_xml_files,
    image_has_shapes,
    print_image_info,
)


def print_statistics(xml_directory: Path) -> None:
    """
    Выводит общую статистику по всем XML-файлам.
    """
    xml_files = get_xml_files(xml_directory)

    if not xml_files:
        logging.info("XML-файлы не найдены.")
        return

    images = collect_all_images(xml_files)

    if not images:
        logging.info("Изображения не найдены.")
        return
    total_images = len(images)
    annotated_images = sum(image_has_shapes(image) for image in images)
    empty_images = total_images - annotated_images
    total_shapes = count_all_shapes(images)

    largest_images, _ = find_largest_images(images)
    smallest_images, _ = find_smallest_images(images)

    logging.info("=" * 50)
    logging.info("ОБЩАЯ СТАТИСТИКА")
    logging.info("=" * 50)

    logging.info(f"Всего изображений: {total_images}")
    logging.info(f"Размеченных изображений: {annotated_images}")
    logging.info(f"Неразмеченных изображений: {empty_images}")
    logging.info(f"Всего фигур: {total_shapes}\n")

    print_image_info("Самое большое изображение", largest_images)
    print_image_info("Самое маленькое изображение", smallest_images)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Общая статистика по XML-аннотациям."
    )

    parser.add_argument(
        "xml_directory",
        type=Path,
        help="Папка с XML-файлами",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_arguments()
    print_statistics(args.xml_directory)


if __name__ == "__main__":
    main()
