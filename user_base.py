import streamlit as st
import sqlite3

# Database functions
def init_db():
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS menu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            price REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_item(name, price):
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO menu (name, price) VALUES (?, ?)', (name, price))
    conn.commit()
    conn.close()

def remove_item(name):
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM menu WHERE name = ?', (name,))
    conn.commit()
    conn.close()

def get_menu():
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, price FROM menu')
    items = cursor.fetchall()
    conn.close()
    return {name: price for name, price in items}

# Base Class for User
class User:
    def __init__(self, username):
        self.username = username

    def place_order(self):
        raise NotImplementedError("This method should be overridden by subclasses.")

# Admin, Customer, and Staff inherit from User
class Admin(User):
    def place_order(self):
        return f"Admin {self.username} is managing orders."

    def manage_menu(self):
        st.subheader("Manage Menu")
        action = st.radio("Select Action", ["Add Item", "Remove Item"], key="menu_action")
        
        # Input fields for item name and price
        item_name = st.text_input("Enter item name", key="admin_item_name")
        item_price = st.number_input("Enter price for item (in Rupees)", min_value=0.0, key="admin_item_price")

        # Add Item Action
        if action == "Add Item":
            if st.button("Add to Menu"):
                if item_name and item_price > 0:
                    try:
                        add_item(item_name, item_price)
                        st.success(f"{item_name} added to menu at ₹{item_price:.2f}.")
                        st.experimental_rerun()  # Refresh to show updated menu
                    except sqlite3.IntegrityError:
                        st.error("Item already exists. Please enter a different item.")
                else:
                    st.error("Please enter a valid item name and price.")

        # Remove Item Action
        elif action == "Remove Item":
            if st.button("Remove from Menu"):
                if item_name:
                    remove_item(item_name)
                    st.success(f"{item_name} removed from menu.")
                    st.experimental_rerun()  # Refresh to show updated menu
                else:
                    st.error("Please enter a valid item name.")

class Customer(User):
    def place_order(self):
        return f"Customer {self.username} is placing an order."

class Staff(User):
    def place_order(self):
        return f"Staff {self.username} is processing an order."

# Encapsulated Order class
class Order:
    def __init__(self):
        self.__order_list = []

    def add_item(self, item):
        self.__order_list.append(item)

    def remove_item(self, item):
        if item in self.__order_list:
            self.__order_list.remove(item)

    def get_order(self):
        return self.__order_list

    def total_cost(self):
        total = 0
        menu = get_menu()
        for item in self.__order_list:
            if item in menu:
                total += menu[item]
        return total

# Streamlit App
def app():
    st.set_page_config(page_title="Dummies Resto and Bar", layout="wide")
    st.title("Welcome to Dummies Resto and Bar")

    # Initialize the database
    init_db()

    # Initialize session states
    if 'order' not in st.session_state:
        st.session_state.order = Order()
    if 'user' not in st.session_state:
        st.session_state.user = None

    # Sidebar for User Login
    st.sidebar.header("User Login")
    user_type = st.sidebar.selectbox("Select User Type", ["Admin", "Customer", "Staff"])
    username = st.sidebar.text_input("Enter your name")

    if st.sidebar.button("Login"):
        if username:
            if user_type == "Admin":
                st.session_state.user = Admin(username)
            elif user_type == "Customer":
                st.session_state.user = Customer(username)
            elif user_type == "Staff":
                st.session_state.user = Staff(username)
            
            st.success(f"{user_type} {username} logged in.")
            st.write(st.session_state.user.place_order())
        else:
            st.error("Please enter your name.")

    # Check if user is logged in
    if st.session_state.user is not None:
        # Menu Display
        st.subheader("Menu")
        items = get_menu()
        for item, price in items.items():
            st.write(f"{item}: ₹{price:.2f}")

        # Allow Customer to place an order
        if isinstance(st.session_state.user, Customer):
            st.subheader("Place Your Order")
            item_selected = st.selectbox("Select an item to order", list(items.keys()), key="order_item")
            if st.button("Add to Order"):
                st.session_state.order.add_item(item_selected)
                st.success(f"Added {item_selected} to your order.")
            
            if st.button("Show Order"):
                current_order = st.session_state.order.get_order()
                st.write("Current Order:", current_order)
                if current_order:
                    st.write("Total Cost: ₹", st.session_state.order.total_cost())
                else:
                    st.warning("Your order is empty.")
            
            if st.button("Clear Order"):
                st.session_state.order = Order()  # Reset the order
                st.success("Order cleared.")
        
        # Staff to process orders
        elif isinstance(st.session_state.user, Staff):
            st.subheader("Staff Functionality")
            st.write("Staff functionality to manage orders will go here.")
            # Future features can be added here

        # Admin to manage system
        elif isinstance(st.session_state.user, Admin):
            st.session_state.user.manage_menu()

    st.sidebar.markdown("### Contact Us")
    st.sidebar.markdown("For any inquiries, please reach out to us at info@dummiesresto.com")

    # Add some footer information
    st.markdown("---")
    st.markdown("### Thank you for visiting Dummies Resto and Bar!")

if __name__ == '__main__':
    app()
