import streamlit as st
from admin import Admin
from customer import Customer
from staff import Staff
from order import Order
from menu import Menu

# Initialize menu
menu = Menu()

# Initialize session states
if 'order' not in st.session_state:
    st.session_state.order = Order()
if 'user' not in st.session_state:
    st.session_state.user = None
if 'orders' not in st.session_state:
    st.session_state.orders = []  # This stores all customer orders

# Streamlit App
def app():
    st.set_page_config(page_title="Dummies Resto and Bar", layout="wide")
    st.title("Welcome to Dummies Resto and Bar")
    st.subheader("Hungry? Grab the Dummies!")
    st.subheader("Dive into our menu and treat yourself!")

    # Sidebar for User Login
    st.sidebar.header("User Login")
    user_type = st.sidebar.selectbox("Select User Type", ["Admin", "Customer", "Staff"])
    username = st.sidebar.text_input("Enter your name")

    if st.sidebar.button("Login"):
        if username:
            if user_type == "Admin":
                st.session_state.user = Admin(username, menu)
            elif user_type == "Customer":
                st.session_state.user = Customer(username)
            elif user_type == "Staff":
                st.session_state.user = Staff(username)

            st.success(f"{user_type} {username} logged in.")
        else:
            st.error("Please enter your name.")

    # Check if user is logged in
    if st.session_state.user is not None:
        # Display Menu
        st.subheader("Menu")
        menu.display_menu()  # Display the current menu

        # Customer Functionality
        if isinstance(st.session_state.user, Customer):
            st.subheader("Place Your Order")
            item_selected = st.selectbox("Select an item to order", list(menu.menu_data.keys()), key="order_item")
            
            if st.button("Add to Order"):
                st.session_state.order.add_item(item_selected)
                st.success(f"Added {item_selected} to your order.")
            
            if st.button("Show Order"):
                current_order = st.session_state.order.get_order()
                st.write("Current Order:", current_order)
                if current_order:
                    total_cost = st.session_state.order.total_cost(menu.menu_data)
                    st.write("Total Cost: ₹", total_cost)
                else:
                    st.warning("Your order is empty.")
            
            if st.button("Clear Order"):
                st.session_state.order = Order()  # Reset the order
                st.success("Order cleared.")

            # After placing the order, store it
            if st.button("Place Order"):
                current_order = st.session_state.order.get_order()
                if current_order:
                    st.session_state.orders.append(current_order)
                    st.success("Order placed successfully!")
                    st.session_state.order = Order()  # Clear the order after placing
                else:
                    st.warning("Your order is empty, cannot place an empty order.")

        # Staff Functionality
        elif isinstance(st.session_state.user, Staff):
            st.session_state.user.view_orders(st.session_state.orders)
            st.session_state.user.mark_order_completed(st.session_state.orders)

        # Admin functionalities
        elif isinstance(st.session_state.user, Admin):
            st.session_state.user.manage_menu()  # Admin can manage the menu

if __name__ == '__main__':
    app()
