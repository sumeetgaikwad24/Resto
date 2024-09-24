import streamlit as st
from menu import Menu

class Admin:
    def __init__(self, username, menu):
        self.username = username
        self.menu = menu

    def manage_menu(self):
        st.subheader("Manage Menu")
        action = st.radio("Select Action", ["Add Item", "Update Item"], key="menu_action")
        
        # Input fields for item name and price
        item_name = st.text_input("Enter item name", key="admin_item_name")
        item_price = st.number_input("Enter price for item (in Rupees)", min_value=0.0, key="admin_item_price")

        # Add Item Action
        if action == "Add Item":
            if st.button("Add to Menu"):
                if item_name:
                    self.menu.update_item(item_name, item_price)
                    st.success(f"{item_name} added/updated to menu at ₹{item_price}.")
                    # No need for rerun, simply display the updated menu below

        # Update Item Action
        elif action == "Update Item":
            if st.button("Update Menu Item"):
                if item_name:
                    self.menu.update_item(item_name, item_price)
                    st.success(f"{item_name} updated to ₹{item_price}.")
                    # Again, no need for rerun
