import re

from pydantic import BaseModel, Field, field_validator

_HEX_COLOR_RE = re.compile(r"^#(?:[0-9a-fA-F]{3}){1,2}$")


class ProductImage(BaseModel):
    url: str
    alt: str


class ProductParameter(BaseModel):
    name: str
    options: list[str]


class Product(BaseModel):
    key: str
    name: str
    description: str
    price: int  # in rubles
    images: list[ProductImage] = Field(default_factory=list)
    colors: list[str] = Field(default_factory=list)
    parameters: list[ProductParameter] = Field(default_factory=list)

    @field_validator("colors")
    @classmethod
    def validate_colors(cls, v: list[str]) -> list[str]:
        for color in v:
            if not _HEX_COLOR_RE.match(color):
                raise ValueError(f"Invalid hex color: {color}")
        return v

    @field_validator("price")
    @classmethod
    def validate_price(cls, v: int) -> int:
        if v < 0:
            raise ValueError("price must be non-negative")
        return v


class CatalogResponse(BaseModel):
    products: list[Product]