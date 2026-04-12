# import uuid
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Product:
    name: str
    description: str
    category: str
    price: float
    brand: str
    quantity: int
    id: Optional[str] = None