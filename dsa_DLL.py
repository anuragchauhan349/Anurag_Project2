import streamlit as st

class Node:
    def __init__(self, station_name):
        self.station_name = station_name
        self.next = None
        self.prev = None

class TrainRoute:
    def __init__(self):
        self.head = None
        self.tail = None

    def view_route(self):
        route = []
        current = self.head
        while current:
            route.append(current.station_name)
            current = current.next
        return " <=> ".join(route) if route else "No stations in the route."

    def insert_station(self, station_name):
        new_station = Node(station_name)
        if not self.head:
            self.head = self.tail = new_station
        else:
            self.tail.next = new_station
            new_station.prev = self.tail
            self.tail = new_station

    def delete_station(self, station_name):
        current = self.head
        while current:
            if current.station_name == station_name:
                if current.prev:
                    current.prev.next = current.next
                if current.next:
                    current.next.prev = current.prev
                if current == self.head:
                    self.head = current.next
                if current == self.tail:
                    self.tail = current.prev
                return f"Station {station_name} deleted."
            current = current.next
        return f"Station {station_name} not found."

    def search_station(self, station_name):
        current = self.head
        index = 1
        while current:
            if current.station_name == station_name:
                return f"Station {station_name} found at position {index}."
            current = current.next
            index += 1
        return f"Station {station_name} not found."

    def show_adjacent_stations(self, station_name):
        current = self.head
        while current:
            if current.station_name == station_name:
                prev_station = current.prev.station_name if current.prev else "None"
                next_station = current.next.station_name if current.next else "None"
                return f"Previous: {prev_station}, Next: {next_station}"
            current = current.next
        return f"Station {station_name} not found."


# Initialize TrainRoute in session state
if "train_route" not in st.session_state:
    st.session_state.train_route = TrainRoute()

st.title("🚆 Train Route Management")

station_input = st.text_input("Enter station name:")

col1, col2 = st.columns(2)

with col1:
    if st.button("➕ Add Station"):
        if station_input:
            st.session_state.train_route.insert_station(station_input)
            st.success(f"Added station: {station_input}")

    if st.button("❌ Delete Station"):
        if station_input:
            result = st.session_state.train_route.delete_station(station_input)
            st.write(result)

with col2:
    if st.button("🔍 Search Station"):
        if station_input:
            result = st.session_state.train_route.search_station(station_input)  
            st.write(result)

    if st.button("🔄 Show Adjacent Stations"):
        if station_input:
            result = st.session_state.train_route.show_adjacent_stations(station_input)
            st.write(result)

if st.button("📍 View Route"):
    st.write(st.session_state.train_route.view_route())
