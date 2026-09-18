from backend.models.product import Product, ProductImage, ProductParameter


def get_catalog() -> list[Product]:
    """Каталог товаров — источник истины для frontend.

    Добавление, удаление или замена изображений не требует изменения HTML:
    список изображений формируется динамически из этого каталога.
    """
    return [
        Product(
            key="tshirt",
            name="Футболка",
            description="Удобная футболка из хлопка с крупным принтом 'САС 101/102'.",
            price=1800,
            images=[
                ProductImage(url="/images/products/tshirt/01.jpg", alt="Футболка — основное фото"),
                ProductImage(url="/images/products/tshirt/02.jpg", alt="Футболка — спина"),
                ProductImage(url="/images/products/tshirt/03.jpg", alt="Футболка — деталь принта"),
            ],
            colors=["#29488B", "#16294A", "#000000", "#BF3930"],
            parameters=[
                ProductParameter(name="Пол", options=["Мужская", "Женская"]),
            ],
        ),
        Product(
            key="mug",
            name="Кружка",
            description="Керамическая кружка объёмом 350 мл с принтом 'САС 101/102'.",
            price=950,
            images=[
                ProductImage(url="/images/products/mug/01.jpg", alt="Кружка — фото спереди"),
                ProductImage(url="/images/products/mug/02.jpg", alt="Кружка — под рукой"),
            ],
            colors=["#FFFFFF", "#000000", "#29488B"],
            parameters=[],
        ),
        Product(
            key="sticker",
            name="Наклейка",
            description="Водостойкая наклейка формата А4 с логотипом курса.",
            price=350,
            images=[
                ProductImage(url="/images/products/sticker/01.jpg", alt="Наклейка — фото"),
            ],
            colors=["#FFD700", "#000000", "#29488B"],
            parameters=[],
        ),
        Product(
            key="notebook",
            name="Ежедневник",
            description="Блокнот формата А5 с мягкой обложкой.",
            price=1200,
            images=[
                ProductImage(url="/images/products/notebook/01.jpg", alt="Ежедневник — фото"),
            ],
            colors=["#16294A", "#87432C", "#653B7A"],
            parameters=[],
        ),
        Product(
            key="badge",
            name="Значок",
            description="Металлический значок с логотипом 'САС 101/102'.",
            price=500,
            images=[
                ProductImage(url="/images/products/badge/01.jpg", alt="Значок — фото"),
            ],
            colors=["#B5975D", "#000000", "#29488B"],
            parameters=[],
        ),
        Product(
            key="pen",
            name="Ручка",
            description="Бюджетная ручка с гравировкой 'САС 101/102'.",
            price=450,
            images=[
                ProductImage(url="/images/products/pen/01.jpg", alt="Ручка — фото"),
            ],
            colors=["#000000", "#B5975D", "#29488B"],
            parameters=[],
        ),
    ]


def get_product_by_key(key: str) -> Product | None:
    """Возвращает товар по ключу или None, если не найден."""
    for product in get_catalog():
        if product.key == key:
            return product
    return None
