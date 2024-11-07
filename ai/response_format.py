from pydantic import BaseModel
from enum import Enum
from typing import Optional, List, Dict

# categories inside google sheets
class Category(str, Enum):
    TennisRaquetsRental = "Tennis Raquets Rental"
    Kiosk = "Kiosk"
    TennisCourtRental = "Tennis Court Rental"
    TennisShopRaquets = "Tennis Shop - Raquets"
    TennisShopClothesAccessories = "Tennis Shop - Clothes & Accessories"
    Gym = "Gym"
    Minigolf = "Minigolf"

# represents table entry
class TableEntry(BaseModel):
    category: Category
    total: str  # "13 €"
    details: List[str]  # article descriptions ["2x Raquets", "1x Balls"]

# customer info
class CustomerInfo(BaseModel):
    Fecha: str
    Nombre: str
    NrHabt: str
    Hotel: str
    Apellido: Optional[str] = None

# factura
class Factura(BaseModel):
    InvoiceNumber: str
    Payment: str
    CustomerInfo: CustomerInfo
    TableSummary: List[TableEntry]
