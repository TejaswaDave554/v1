import streamlit as st
from src.auth.auth_utils import hash_password, validate_email, validate_phone, login_user
from src.auth.password_validator import validate_password_strength, get_password_requirements_text
from config.database import db

def render_register_form():
    st.subheader("Create Your Account")

    account_type = st.selectbox("Account Type", ["Customer", "Driver"])

    col1, col2 = st.columns(2)

    with col1:
        full_name = st.text_input("Full Name*", placeholder="Enter your full name")
        if full_name and len(full_name) < 2:
            st.error("Name must be at least 2 characters")

        username = st.text_input("Username*", placeholder="Choose a username")
        if username:
            if len(username) < 3:
                st.error("Username must be at least 3 characters")
            elif db.get_user_by_username(username):
                st.error("Username already taken")
            else:
                st.success("Username available")

        email = st.text_input("Email*", placeholder="your.email@example.com")
        if email and not validate_email(email):
            st.error("Invalid email format")
        elif email:
            st.success("Valid email")

    with col2:
        phone = st.text_input("Phone*", placeholder="+1234567890")
        if phone and not validate_phone(phone):
            st.error("Phone must be at least 10 digits")
        elif phone:
            st.success("Valid phone")

        password = st.text_input("Password*", type="password", placeholder="Choose a strong password")
        if password:
            pwd_check = validate_password_strength(password)
            if pwd_check['strength'] == 'weak':
                st.error(f"Weak password ({pwd_check['passed_count']}/5 criteria)")
            elif pwd_check['strength'] == 'medium':
                st.warning(f"Medium password ({pwd_check['passed_count']}/5 criteria)")
            else:
                st.success(f"Strong password ({pwd_check['passed_count']}/5 criteria)")

            with st.expander("Password Requirements"):
                st.text(get_password_requirements_text(pwd_check['criteria']))

        confirm_password = st.text_input("Confirm Password*", type="password", placeholder="Confirm your password")
        if confirm_password:
            if password != confirm_password:
                st.error("Passwords do not match")
            else:
                st.success("Passwords match")

    if account_type == "Driver":
        st.markdown("### Driver Information")
        col3, col4 = st.columns(2)

        with col3:
            license_number = st.text_input("License Number*", placeholder="DL1234567890")
            if license_number and len(license_number) < 5:
                st.error("Invalid license number")

            license_expiry = st.date_input("License Expiry*")
            experience_years = st.number_input("Experience (Years)*", min_value=0, max_value=50, value=1)

        with col4:
            vehicle_types = st.multiselect("Vehicle Types*", ["sedan", "suv", "hatchback", "luxury", "van"], default=["sedan"])
            city = st.text_input("City*", placeholder="Mumbai")
            area = st.text_input("Area*", placeholder="Bandra West")

    terms_accepted = st.checkbox("I accept the Terms and Conditions*")

    col1, col2 = st.columns(2)
    with col1:
        register_btn = st.button("Register", use_container_width=True, type="primary")
    with col2:
        login_btn = st.button("Login Instead", use_container_width=True)

    if register_btn:
        errors = validate_registration_form(locals())

        if not errors:
            try:

                role = 'driver' if account_type == 'Driver' else 'customer'
                user_data = {
                    'username': username,
                    'email': email,
                    'password_hash': hash_password(password),
                    'phone': phone,
                    'role': role,
                    'full_name': full_name
                }

                user_id = db.create_user(user_data)

                if account_type == 'Driver':
                    driver_data = {
                        'user_id': user_id,
                        'license_number': license_number,
                        'license_expiry': license_expiry.isoformat(),
                        'experience_years': experience_years
                    }
                    db.create_driver(driver_data)

                user_data['id'] = user_id
                login_user(user_data)

                st.success("Registration successful!")
                st.balloons()

                if role == 'driver':
                    st.switch_page("pages/Driver_Dashboard.py")
                else:
                    st.switch_page("pages/User_Dashboard.py")

            except Exception as e:
                st.error(f"Registration failed: {str(e)}")
        else:
            for error in errors:
                st.error(error)

    if login_btn:
        st.switch_page("pages/Login.py")

def validate_registration_form(form_data):
    errors = []

    if not form_data.get('full_name') or len(form_data.get('full_name', '')) < 2:
        errors.append("Full name is required (min 2 characters)")

    if not form_data.get('username') or len(form_data.get('username', '')) < 3:
        errors.append("Username is required (min 3 characters)")

    if not validate_email(form_data.get('email', '')):
        errors.append("Valid email is required")

    if not validate_phone(form_data.get('phone', '')):
        errors.append("Valid phone number is required")

    if not form_data.get('password'):
        errors.append("Password is required")
    else:
        pwd_check = validate_password_strength(form_data.get('password'))
        if not pwd_check['valid']:
            errors.append("Password is too weak. Must meet at least 3 criteria.")

    if form_data.get('password') != form_data.get('confirm_password'):
        errors.append("Passwords do not match")

    if not form_data.get('terms_accepted'):
        errors.append("You must accept the terms and conditions")

    if db.get_user_by_username(form_data.get('username', '')):
        errors.append("Username already exists")

    if form_data.get('account_type') == 'Driver':
        if not form_data.get('license_number') or len(form_data.get('license_number', '')) < 5:
            errors.append("Valid license number is required")
        if not form_data.get('city'):
            errors.append("City is required")
        if not form_data.get('area'):
            errors.append("Area is required")

    return errors
