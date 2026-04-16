from dataclasses import dataclass
from typing import Optional

@dataclass
class ProductCategory:
    title: str
    description: str
    id: Optional[str] = None