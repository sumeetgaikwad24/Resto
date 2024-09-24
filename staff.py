import streamlit as st
class Staff:
    def __init__(self, username):
        self.username = username

    def view_orders(self, orders):
        """Function to view all current orders."""
        st.subheader("Pending Orders")
        if orders:
            for idx, order in enumerate(orders):
                st.write(f"Order {idx + 1}: {order}")
        else:
            st.write("No pending orders at the moment.")

    def mark_order_completed(self, orders):
        """Function to mark an order as completed."""
        if orders:
            order_to_complete = st.selectbox("Select an order to complete", [f"Order {idx + 1}" for idx, _ in enumerate(orders)])
            if st.button("Mark as Completed"):
                order_index = int(order_to_complete.split()[-1]) - 1
                del orders[order_index]  # Remove the completed order
                st.success(f"{order_to_complete} has been marked as completed.")
        else:
            st.write("No orders to complete.")
