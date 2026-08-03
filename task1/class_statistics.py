from pathlib import Path
import argparse
import logging


from common import (
    collect_all_images,
    count_classes,
    get_xml_files,
)


def print_class_statistics(xml_directory: Path) -> None:
    """
    Выводит статистику по классам.
    """
    xml_files = get_xml_files(xml_directory)

    if not xml_files:
        logging.info("XML-файлы не найдены.")
        return

    images = collect_all_images(xml_files)
    class_counter = count_classes(images)

    logging.info("=" * 50)
    logging.info("СТАТИСТИКА ПО КЛАССАМ")
    logging.info("=" * 50)

    for label, count in sorted(class_counter.items()):
        logging.info(f"{label}: {count}")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Статистика по классам."
    )

    parser.add_argument(
        "xml_directory",
        type=Path,
        help="Папка с XML-файлами",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_arguments()
    print_class_statistics(args.xml_directory)


if __name__ == "__main__":
    main()
