import uuid
import streamlit as st
from datetime import datetime, date, time
from config.database import db

def render_booking_form():
    st.subheader("Book Your Ride")

    if not st.session_state.get("logged_in", False):
        st.warning("Please login to book a ride")
        if st.button("Login"):
            st.switch_page("pages/🔐_Login.py")
        return

    def create_booking(booking_data: dict) -> str | None:
        booking_id = str(uuid.uuid4())
        now = datetime.now().isoformat(timespec="seconds")

        rows = db.execute(
            ,
            (
                booking_id,
                booking_data["customer_id"],
                booking_data.get("driver_id"),
                booking_data["pickup_location"],
                booking_data["dropoff_location"],
                booking_data["pickup_datetime"],
                booking_data["service_type"],
                booking_data.get("vehicle_type", "sedan"),
                booking_data.get("status", "pending"),
                float(booking_data.get("estimated_fare", 0)),
                booking_data.get("actual_fare"),
                booking_data.get("special_instructions", ""),
                now,
                now,
            ),
        )
        return booking_id if rows else None

    with st.form("booking_form"):
        col1, col2 = st.columns(2)

        with col1:
            pickup_location = st.text_input("Pickup Location", placeholder="Enter pickup address")
            pickup_date = st.date_input("Pickup Date", min_value=date.today())
            service_type = st.selectbox(
                "Service Type",
                ["airport_transfer", "corporate", "wedding", "hourly", "outstation"],
                format_func=lambda x: x.replace("_", " ").title(),
            )

        with col2:
            dropoff_location = st.text_input("Dropoff Location", placeholder="Enter destination")
            pickup_time = st.time_input("Pickup Time", value=time(9, 0))
            vehicle_type = st.selectbox(
                "Vehicle Type",
                ["sedan", "suv", "hatchback", "luxury", "van"],
                format_func=lambda x: x.title(),
            )

        special_instructions = st.text_area(
            "Special Instructions",
            placeholder="Any special requirements...",
        )

        fare_rates = {
            "sedan": {"airport_transfer": 150, "corporate": 120, "wedding": 200, "hourly": 100, "outstation": 8},
            "suv": {"airport_transfer": 200, "corporate": 160, "wedding": 250, "hourly": 130, "outstation": 10},
            "luxury": {"airport_transfer": 300, "corporate": 250, "wedding": 400, "hourly": 200, "outstation": 15},
            "hatchback": {"airport_transfer": 130, "corporate": 110, "wedding": 180, "hourly": 90, "outstation": 7},
            "van": {"airport_transfer": 220, "corporate": 180, "wedding": 280, "hourly": 150, "outstation": 12},
        }

        base_rate = fare_rates.get(vehicle_type.lower(), fare_rates["sedan"]).get(service_type, 150)

        min_fare = 100
        if service_type == "hourly":
            hours = st.number_input("Hours needed", min_value=1, max_value=12, value=4)
            default_est = max(int(base_rate * hours), min_fare)
        else:
            default_est = max(int(base_rate), min_fare)

        estimated_fare = st.number_input(
            "Estimated Fare",
            value=default_est,
            min_value=min_fare,
            help=f"Base rate: {base_rate}",
        )

        submitted = st.form_submit_button("Book Ride", type="primary", use_container_width=True)

    if not submitted:
        return

    if not pickup_location or not dropoff_location:
        st.error("Please fill in pickup and dropoff locations.")
        return

    try:
        pickup_datetime = datetime.combine(pickup_date, pickup_time).isoformat(timespec="minutes")

        booking_data = {
            "customer_id": st.session_state["user_id"],
            "pickup_location": pickup_location,
            "dropoff_location": dropoff_location,
            "pickup_datetime": pickup_datetime,
            "service_type": service_type,
            "vehicle_type": vehicle_type.lower(),
            "estimated_fare": float(estimated_fare),
            "special_instructions": special_instructions,
            "status": "pending",
        }

        with st.spinner("Booking your ride..."):
            booking_id = create_booking(booking_data)

        if booking_id:
            st.success(f"Ride booked successfully! Booking ID: {booking_id[:8]}...")
            st.balloons()

            with st.expander("Booking Details", expanded=True):
                c1, c2 = st.columns(2)
                with c1:
                    st.write(f"From: {pickup_location}")
                    st.write(f"To: {dropoff_location}")
                    st.write(f"Date & Time: {pickup_date} at {pickup_time}")
                with c2:
                    st.write(f"Service: {service_type.replace('_', ' ').title()}")
                    st.write(f"Vehicle: {vehicle_type.title()}")
                    st.write(f"Fare: {estimated_fare}")

            st.info("We'll notify you once a driver accepts your booking!")
        else:
            st.error("Booking failed. Please try again.")

    except Exception as e:
        st.error(f"Booking failed: {e}")
