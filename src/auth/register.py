"""
Registration Form Component  
"""

import streamlit as st
from src.utils.validators import validate_registration

def render_register_form():
    """Render registration form"""
    with st.form("register_form"):
        st.subheader("📝 Create New Account")
        
        col_reg1, col_reg2 = st.columns(2)
        
        with col_reg1:
            first_name = st.text_input("First Name", placeholder="Enter first name")
            email = st.text_input("Email", placeholder="Enter your email")  
            password = st.text_input("Password", type="password", placeholder="Create password")
        
        with col_reg2:
            last_name = st.text_input("Last Name", placeholder="Enter last name")
            phone = st.text_input("Phone", placeholder="Enter phone number")
            confirm_password = st.text_input("Confirm Password", type="password", 
                                           placeholder="Confirm password")
        
        terms = st.checkbox("I agree to the Terms of Service and Privacy Policy")
        
        register_submit = st.form_submit_button("🎉 Create Account", use_container_width=True)
        
        if register_submit:
            handle_registration(first_name, last_name, email, phone, password, 
                              confirm_password, terms)

def handle_registration(first_name: str, last_name: str, email: str, phone: str,
                       password: str, confirm_password: str, terms_accepted: bool):
    """Handle registration submission"""
    
    validation_result = validate_registration(
        first_name, last_name, email, phone, password, confirm_password, terms_accepted
    )
    
    if not validation_result["valid"]:
        st.error(f"❌ {validation_result['message']}")
        return
    
    # TODO: Implement user registration in database
    # success = register_user_in_database(first_name, last_name, email, phone, password)
    # if success:
    st.success("✅ Account created successfully! Please login.")
    st.balloons()
    # else:
    #     st.error("❌ Registration failed. Please try again.")

def register_user_in_database(first_name: str, last_name: str, email: str, 
                            phone: str, password: str) -> bool:
    """Register user in database (future implementation)"""
    # TODO: Implement database user creation
    # from config.database import db_manager
    # from src.models.user import User
    # return User.create(first_name, last_name, email, phone, password)
    pass
