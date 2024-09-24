import json
import streamlit as st

class Menu:
    def __init__(self):
        self.menu_data = self.load_menu()

    def load_menu(self):
        try:
            with open('menu_data.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "Burger": 150.0,
                "Pizza": 300.0,
                "Pasta": 200.0,
                "Salad": 100.0,
            }

    def save_menu(self):
        with open('menu_data.json', 'w') as f:
            json.dump(self.menu_data, f)

    def display_menu(self):
        for item, price in self.menu_data.items():
            st.write(f"{item}: ₹{price}")

    def update_item(self, name, price):
        self.menu_data[name] = price  # Update or add item with new price
        self.save_menu()  # Save changes to the JSON file
