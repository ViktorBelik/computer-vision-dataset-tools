# Инструменты для работы с данными в области CV

## Структура проекта

```bash
computer-vision-dataset-tools/
│
├── README.md
├── requirements.txt
│
├── task1/
│   ├── data/
│   ├── common.py
│   ├── statistics.py
│   ├── class_statistics.py
│   ├── shape_statistics.py
│   └── modify_xml.py
│
└── task2/
    ├── data/
    ├── common.py
    ├── restructure_dataset.py
    ├── validate_dataset.py
    └── coco_to_yolo.py
```

---

## Установка

Создать виртуальное окружение:

```bash
python -m venv venv
```

Windows

```bash
venv\Scripts\activate
```

Linux/macOS

```bash
source venv/bin/activate
```

Установить зависимости

```bash
pip install -r requirements.txt
```

---

## Task 1

Работа с XML-аннотациями.

---

### statistics.py

Выводит:

- общее количество изображений;
- количество размеченных изображений;
- количество неразмеченных изображений;
- количество фигур;
- информацию о самом большом и самом маленьком изображении.

Запуск

```bash
python task1/statistics.py task1/data/
```

---

### class_statistics.py

Выводит количество фигур каждого класса.

Запуск

```bash
python task1/class_statistics.py task1/data/
```

---

### shape_statistics.py

Выводит статистику по типам фигур.

Запуск

```bash
python task1/shape_statistics.py task1/data/
```

---

### modify_xml.py

Для каждого XML:

- переворачивает id изображений;
- оставляет только имя файла;
- меняет расширение на `.png`;
- сохраняет новый XML с суффиксом `_modified.xml`.

Запуск

```bash
python task1/modify_xml.py task1/data/
```

---

## Task 2

Работа с COCO.

---

### restructure_dataset.py

Создает новую структуру директорий

```bash
images/
    cat/
    dog/
    cat_dog/
...
```

Обновляет поле `file_name` и сохраняет

```bash
task2/data/annotations/updated_annotations.json
```

Запуск

```bash
python task2/restructure_dataset.py \
    --images task2/data/images \
    --annotations task2/data/annotations/instances_train.json
```

---

### validate_dataset.py

Проверяет:

- существование изображений;
- корректность image_id;
- корректность category_id;
- пустые изображения.

Создает файл

```bash
task2/data/report/dataset_report.json
```

Запуск

```bash
python task2/validate_dataset.py \
    --images task2/data/images \
    --annotations task2/data/annotations/updated_annotations.json
```

---

### coco_to_yolo.py

Преобразует COCO в формат YOLO.

Для каждого изображения создается txt-файл.

Запуск

```bash
python task2/coco_to_yolo.py \
    --images task2/data/ \
    --annotations task2/data/annotations/updated_annotations.json
```

---

## Выходные файлы

Task 1

```bash
annotations_modified.xml
annotations-2_modified.xml
annotations-3_modified.xml
```

Task 2

```bash
updated_annotations.json

dataset_report.json

images/ *.txt
```

---

## Используемые библиотеки

- pathlib
- json
- shutil
- collections
- argparse
- xml.etree.ElementTree
- tqdm
- Pillow
