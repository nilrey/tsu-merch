import random
from datetime import datetime
from typing import Any, Optional

from fastapi import HTTPException

from backend.models.order import OrderItemRequest, OrderRequest
from backend.models.product import Product
from backend.services.catalog import get_product_by_key


class OrderValidationResult:
    """Holds validated items enriched with catalog prices."""

    def __init__(self):
        self.items: list[dict[str, Any]] = []
        self.errors: list[str] = []


class OrderService:
    """Handles order creation, validation, storage, and pricing.

    Backend is the source of truth for:
    - product existence
    - price
    - available colors
    - available parameters and their values
    """

    def validate_order(self, order: OrderRequest) -> OrderValidationResult:
        """Validate every item against the catalog.

        Checks:
        - product_key exists
        - color is allowed for the product
        - each parameter is defined for the product
        - each parameter value is allowed
        """
        result = OrderValidationResult()

        for idx, item in enumerate(order.items):
            product = get_product_by_key(item.product_key)

            if product is None:
                result.errors.append(
                    f"Item {idx + 1}: unknown product_key '{item.product_key}'"
                )
                continue

            # Validate color
            if item.color not in product.colors:
                result.errors.append(
                    f"Item {idx + 1} ({product.name}): "
                    f"color '{item.color}' is not available"
                )

            # Validate parameters
            for param_name, param_value in item.parameters.items():
                param_def = self._find_parameter(product, param_name)
                if param_def is None:
                    result.errors.append(
                        f"Item {idx + 1} ({product.name}): "
                        f"unknown parameter '{param_name}'"
                    )
                    continue

                if param_value not in param_def.options:
                    result.errors.append(
                        f"Item {idx + 1} ({product.name}): "
                        f"invalid value '{param_value}' for parameter '{param_name}'"
                    )

            result.items.append({
                "product": product,
                "color": item.color,
                "parameters": item.parameters,
            })

        return result

    def _find_parameter(self, product: Product, name: str) -> Optional[Any]:
        """Find a parameter definition by name in the product."""
        for param in product.parameters:
            if param.name == name:
                return param
        return None

    def generate_order_number(self) -> str:
        """Generate order number: YYYYMMDD-HHMMSS-XXX"""
        now = datetime.now()
        suffix = random.randint(100, 999)
        return now.strftime(f"%Y%m%d-%H%M%S-{suffix:03d}")

    def generate_order_filename(self) -> str:
        """Generate unique filename: order_YYYY-MM-DD_HH-MM-SS[_N].txt"""
        import os

        now = datetime.now()
        base = now.strftime("order_%Y-%m-%d_%H-%M-%S")
        path = os.path.join("orders", f"{base}.txt")

        counter = 0
        while os.path.exists(path):
            counter += 1
            path = os.path.join("orders", f"{base}_{counter:03d}.txt")

        return path

    def create_order(self, order: OrderRequest) -> tuple[str, str]:
        """
        Create order:
        1. Validate items
        2. Generate order number
        3. Save to file
        4. Return (order_number, filename)
        """
        result = self.validate_order(order)
        if result.errors:
            raise HTTPException(
                status_code=400,
                detail={"errors": result.errors},
            )

        order_number = self.generate_order_number()
        filename = self.generate_order_filename()

        content = self._format_order(order, order_number, filename, result.items)

        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)

        return order_number, filename

    def _format_order(
        self,
        order: OrderRequest,
        order_number: str,
        filename: str,
        validated_items: list[dict[str, Any]],
    ) -> str:
        """Format order data for file storage."""
        now = datetime.now()
        lines = [
            f"Order: {order_number}",
            f"Date: {now.strftime('%Y-%m-%d %H:%M:%S')}",
            f"File: {filename}",
            "",
            "Customer:",
            f"Name: {order.name}",
            f"Email: {order.email}",
            f"Consent: {'yes' if order.consent else 'no'}",
            "",
            "Products:",
        ]

        for idx, item in enumerate(validated_items, 1):
            product: Product = item["product"]
            lines.append("")
            lines.append(f"{idx}. {product.name}")
            lines.append(f"   Price: {product.price}")
            lines.append(f"   Color: {item['color']}")
            lines.append(f"   Parameters:")

            if item["parameters"]:
                for param_name, param_value in item["parameters"].items():
                    lines.append(f"     {param_name}: {param_value}")
            else:
                lines.append("     (none)")

        lines.append("")
        lines.append(f"Total items: {len(validated_items)}")
        lines.append(f"Total price: {sum(item['product'].price for item in validated_items)}")

        return "\n".join(lines) + "\n"
