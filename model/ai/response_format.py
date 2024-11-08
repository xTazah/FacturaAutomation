from pydantic import BaseModel
from enum import Enum
from typing import Optional, List, Dict

# categories inside google sheets
class Category(str, Enum):
    TennisRaquetsRental = "Tennis Raquets rental"
    Kiosk = "Kiosk"
    TennisCourtRental = "Tennis Court rental"
    TennisShopRaquets = "Tennis Shop- Raquets"
    TennisShopClothesAccessories = "Tennis Shop- Clothes & Accesories"
    Gym = "Gym"
    Minigolf = "Minigolf"

class PaymentType(str, Enum):
    Efectivo = "Bargeld/Cash"
    CreditHabt = "Zimmerrechnung"
    Tarjeta = "Kreditkarte/Card"

# represents table entry
class TableEntry(BaseModel):
    category: Category
    total: str  # "13 €"
    details: List[str]  # article descriptions ["2x Raquets", "1x Balls"]

# customer info
class CustomerInfo(BaseModel):
    Fecha: str
    Nombre: Optional[str] = None
    NrHabt: Optional[str] = None
    Hotel: Optional[str] = None
    Apellido: Optional[str] = None

# factura
class Factura(BaseModel):
    InvoiceNumber: str
    Payment: PaymentType
    CustomerInfo: CustomerInfo
    TableSummary: List[TableEntry]
