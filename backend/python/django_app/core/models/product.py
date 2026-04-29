# import uuid
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Product:
    name: str
    description: str
    price: float
    brand: str
    quantity: int
    category: Optional[str] = None
    id: Optional[str] = None
    category_id: Optional[str] = None