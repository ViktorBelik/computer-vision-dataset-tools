from pathlib import Path
import logging
import argparse

from common import (
    collect_all_images,
    count_shape_types,
    get_xml_files,
)


def print_shape_statistics(xml_directory: Path) -> None:
    """
    Выводит статистику по типам фигур.
    """
    xml_files = get_xml_files(xml_directory)

    if not xml_files:
        logging.info("XML-файлы не найдены.")
        return

    images = collect_all_images(xml_files)
    shape_counter = count_shape_types(images)

    logging.info("=" * 50)
    logging.info("СТАТИСТИКА ПО ТИПАМ ФИГУР")
    logging.info("=" * 50)

    for shape_type, count in sorted(shape_counter.items()):
        logging.info(f"{shape_type}: {count}")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Статистика по типам фигур."
    )

    parser.add_argument(
        "xml_directory",
        type=Path,
        help="Папка с XML-файлами",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_arguments()
    print_shape_statistics(args.xml_directory)


if __name__ == "__main__":
    main()
