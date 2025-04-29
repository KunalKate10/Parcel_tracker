import hashlib
import streamlit as st
import json
from datetime import datetime

class Block:
    def __init__(self, timestamp, data, previous_hash):
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(str(self.timestamp).encode('utf-8') + 
                   str(self.data).encode('utf-8') + 
                   str(self.previous_hash).encode('utf-8'))
        return sha.hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = self.load_chain()

    def create_genesis_block(self):
        return Block("01/01/2023", "Genesis Block", "0")

    def load_chain(self):
        try:
            with open('blockchain_data.json', 'r') as f:
                data = json.load(f)
                chain = [Block(b['Timestamp'], b['Data'], b['Previous Hash']) for b in data]
            return chain
        except (FileNotFoundError, json.JSONDecodeError):
            # If file doesn't exist, create genesis block
            return [self.create_genesis_block()]

    def save_chain(self):
        with open('blockchain_data.json', 'w') as f:
            data = [{
                'Timestamp': block.timestamp,
                'Data': block.data,
                'Hash': block.hash,
                'Previous Hash': block.previous_hash
            } for block in self.chain]
            json.dump(data, f, indent=4)

    def add_block(self, data):
        previous_block = self.chain[-1]
        new_block = Block(str(datetime.now()), data, previous_block.hash)
        self.chain.append(new_block)
        self.save_chain()

# Create a blockchain instance
blockchain = Blockchain()

# Streamlit App Interface
st.title("Blockchain Parcel Tracking System")

# Display current blockchain
st.subheader("Current Blockchain")
for block in blockchain.chain:
    st.write(f"Timestamp: {block.timestamp}")
    st.write(f"Data: {block.data}")
    st.write(f"Hash: {block.hash}")
    st.write(f"Previous Hash: {block.previous_hash}")
    st.write("\n")

# Add parcel data
new_data = st.text_input("Add Parcel Tracking Info:")
if st.button("Add Block"):
    if new_data:
        blockchain.add_block(new_data)
        st.success(f"Block with data '{new_data}' added successfully.")
    else:
        st.warning("Please enter parcel tracking data.")
