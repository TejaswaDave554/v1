from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime
from decimal import Decimal

@dataclass
class Booking:

    id: str
    customer_id: str
    driver_id: Optional[str]
    pickup_location: str
    dropoff_location: str
    pickup_datetime: datetime
    service_type: str
    vehicle_type: str = 'sedan'
    status: str = 'pending'
    estimated_fare: Decimal = Decimal('0.00')
    actual_fare: Optional[Decimal] = None
    special_instructions: Optional[str] = None
    rating: Optional[int] = None
    feedback: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Booking':

        return cls(
            id=data['id'],
            customer_id=data['customer_id'],
            driver_id=data.get('driver_id'),
            pickup_location=data['pickup_location'],
            dropoff_location=data['dropoff_location'],
            pickup_datetime=data['pickup_datetime'],
            service_type=data['service_type'],
            vehicle_type=data.get('vehicle_type', 'sedan'),
            status=data.get('status', 'pending'),
            estimated_fare=Decimal(str(data.get('estimated_fare', 0))),
            actual_fare=Decimal(str(data['actual_fare'])) if data.get('actual_fare') else None,
            special_instructions=data.get('special_instructions'),
            rating=data.get('rating'),
            feedback=data.get('feedback'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
