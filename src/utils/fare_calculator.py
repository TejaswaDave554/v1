BASE_FARE = {
    'sedan': 50,
    'suv': 80,
    'hatchback': 40,
    'luxury': 150,
    'van': 100
}

PER_KM_RATE = {
    'sedan': 12,
    'suv': 18,
    'hatchback': 10,
    'luxury': 30,
    'van': 15
}

SERVICE_MULTIPLIER = {
    'airport_transfer': 1.2,
    'corporate': 1.1,
    'wedding': 1.5,
    'hourly': 1.0,
    'outstation': 1.3
}

def calculate_fare(distance_km: float, vehicle_type: str, service_type: str, duration_hours: float = 0) -> dict:

    vehicle_type = vehicle_type.lower()
    service_type = service_type.lower().replace(' ', '_')

    base = BASE_FARE.get(vehicle_type, 50)
    per_km = PER_KM_RATE.get(vehicle_type, 12)
    multiplier = SERVICE_MULTIPLIER.get(service_type, 1.0)

    distance_fare = distance_km * per_km
    total = (base + distance_fare) * multiplier

    if service_type == 'hourly' and duration_hours > 0:
        total = base * duration_hours * multiplier

    return {
        'base_fare': round(base, 2),
        'distance_fare': round(distance_fare, 2),
        'service_charge': round((base + distance_fare) * (multiplier - 1), 2),
        'total_fare': round(total, 2),
        'breakdown': f"Base: ₹{base} + Distance ({distance_km}km): ₹{distance_fare:.2f} × {multiplier} = ₹{total:.2f}"
    }

def estimate_distance(pickup: str, dropoff: str) -> float:
    import random
    return round(random.uniform(5, 50), 2)
