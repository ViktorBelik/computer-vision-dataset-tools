from pathlib import Path
import logging
import argparse
import xml.etree.ElementTree as ET

from common import get_xml_files, get_images


def reverse_image_ids(images: list[ET.Element]) -> None:
    """
    Меняет id изображений на обратные.
    """
    image_ids = [image.get("id") for image in images]

    reversed_ids = list(reversed(image_ids))

    for image, new_id in zip(images, reversed_ids):
        image.set("id", new_id)


def update_image_names(images: list[ET.Element]) -> None:
    """
    Оставляет только имя файла и меняет расширение на .png.
    """
    for image in images:
        image_name = Path(image.get("name", ""))

        new_name = image_name.stem + ".png"

        image.set("name", new_name)


def save_modified_xml(tree: ET.ElementTree, xml_path: Path) -> None:
    """
    Сохраняет измененный XML.
    """
    output_path = xml_path.with_name(
        f"{xml_path.stem}_modified.xml"
    )

    ET.indent(tree, space="    ")
    tree.write(
        output_path,
        encoding="utf-8",
        xml_declaration=True,
    )

    logging.info(f"Сохранен: {output_path.name}")


def modify_xml(xml_path: Path) -> None:
    """
    Изменяет один XML-файл.
    """
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()

        images = get_images(root)

        reverse_image_ids(images)
        update_image_names(images)

        save_modified_xml(tree, xml_path)
    except ET.ParseError:
        logging.info(f"Ошибка чтения {xml_path}")
        return


def process_directory(xml_directory: Path) -> None:
    """
    Обрабатывает все XML-файлы в директории.
    """
    xml_files = get_xml_files(xml_directory)

    if not xml_files:
        logging.info("XML-файлы не найдены.")
        return

    for xml_file in xml_files:
        modify_xml(xml_file)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Модификация XML-аннотаций."
    )

    parser.add_argument(
        "xml_directory",
        type=Path,
        help="Папка с XML-файлами",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_arguments()
    process_directory(args.xml_directory)


if __name__ == "__main__":
    main()
