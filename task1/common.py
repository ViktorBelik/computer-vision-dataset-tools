import logging
from collections import Counter
from pathlib import Path
import xml.etree.ElementTree as ET


SHAPE_TYPES = ("box", "polygon", "points")


logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
)


def get_xml_files(directory: Path) -> list[Path]:
    """
    Возвращает список всех XML-файлов в директории.
    """
    return sorted(directory.glob("*.xml"))


def load_xml(xml_path: Path) -> ET.ElementTree:
    """
    Загружает XML-файл.
    """
    return ET.parse(xml_path)


def get_images(root: ET.Element) -> list[ET.Element]:
    """
    Возвращает список всех изображений.
    """
    return root.findall("image")


def get_shapes(image: ET.Element) -> list[ET.Element]:
    """
    Возвращает все фигуры изображения.
    """
    shapes = []

    for shape_type in SHAPE_TYPES:
        shapes.extend(image.findall(shape_type))

    return shapes


def image_has_shapes(image: ET.Element) -> bool:
    """
    Проверяет, содержит ли изображение хотя бы одну фигуру.
    """
    return len(get_shapes(image)) > 0


def count_all_shapes(images: list[ET.Element]) -> int:
    """
    Считает общее количество фигур.
    """
    total = 0

    for image in images:
        total += len(get_shapes(image))

    return total


def count_classes(images: list[ET.Element]) -> Counter:
    """
    Возвращает количество фигур каждого класса.
    """
    counter = Counter()

    for image in images:
        for shape in get_shapes(image):
            label = shape.get("label")

            if label:
                counter[label] += 1

    return counter


def count_shape_types(images: list[ET.Element]) -> Counter:
    """
    Возвращает количество фигур каждого типа.
    """
    counter = Counter()

    for image in images:
        for shape in get_shapes(image):
            counter[shape.tag] += 1

    return counter


def get_image_size(image: ET.Element) -> tuple[int, int]:
    """
    Возвращает размеры изображения.
    """
    width = int(image.get("width"))
    height = int(image.get("height"))

    return width, height


def get_image_area(image: ET.Element) -> int:
    """
    Возвращает площадь изображения.
    """
    width, height = get_image_size(image)
    return width * height


def get_image_name(image: ET.Element) -> str:
    """
    Возвращает имя изображения.
    """
    return image.get("name", "")


def collect_all_images(xml_files: list[Path]) -> list[ET.Element]:
    """
    Загружает изображения из всех XML-файлов.
    """
    images = []

    for xml_file in xml_files:
        tree = load_xml(xml_file)
        root = tree.getroot()
        images.extend(get_images(root))

    return images


def find_largest_images(images: list[ET.Element]) -> tuple[list[ET.Element], int]:
    """
    Возвращает список самых больших изображений.
    """
    if not images:
        return [], 0

    largest_images = []
    max_area = -1

    for image in images:
        area = get_image_area(image)

        if area > max_area:
            max_area = area
            largest_images = [image]
        elif area == max_area:
            largest_images.append(image)

    return largest_images, max_area


def find_smallest_images(images: list[ET.Element]) -> tuple[list[ET.Element], int]:
    """
    Возвращает список самых маленьких изображений.
    """
    if not images:
        return [], 0

    smallest_images = []
    min_area = float("inf")

    for image in images:
        area = get_image_area(image)

        if area < min_area:
            min_area = area
            smallest_images = [image]
        elif area == min_area:
            smallest_images.append(image)

    return smallest_images, min_area


def print_image_info(title: str, images: list[ET.Element]) -> None:
    """
    Печатает информацию об изображении.
    """
    image = images[0]

    width, height = get_image_size(image)

    logging.info(title)
    logging.info(f"Количество: {len(images)}")
    logging.info(f"Название: {Path(get_image_name(image)).name}")
    logging.info(f"Размер: {width} x {height}\n")
