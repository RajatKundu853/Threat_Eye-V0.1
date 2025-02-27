import sqlite3
import time
from scapy.all import sniff, IP, get_if_list
from datetime import datetime

# Function to display available network interfaces and get user selection
def get_interface():
    interfaces = get_if_list()  # Get a list of available interfaces
    print("\n[🔍] Available Network Interfaces:")
    for idx, iface in enumerate(interfaces):
        print(f"  [{idx}] {iface}")

    while True:
        try:
            choice = int(input("\n[⚡] Enter the number of the interface to sniff on: "))
            if 0 <= choice < len(interfaces):
                return interfaces[choice]  # Return the selected interface
            else:
                print("[⚠] Invalid selection. Choose a valid number from the list.")
        except ValueError:
            print("[❌] Please enter a valid numeric value.")

# Function to log packets into SQLite with a retry mechanism
def log_packet(packet):
    if packet.haslayer(IP):  # Ensure it's an IP packet
        src_ip = packet[IP].src
        dest_ip = packet[IP].dst
        protocol = packet[IP].proto
        length = len(packet)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Timestamp format

        # Retry up to 5 times if the database is locked
        for attempt in range(5):
            try:
                conn = sqlite3.connect('network_logs.db', check_same_thread=False)
                cursor = conn.cursor()

                # Ensure the table exists
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS network_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        src_ip TEXT,
                        dest_ip TEXT,
                        protocol INTEGER,
                        length INTEGER,
                        timestamp TEXT
                    )
                """)

                # Insert packet data
                cursor.execute("INSERT INTO network_logs (src_ip, dest_ip, protocol, length, timestamp) VALUES (?, ?, ?, ?, ?)",
                               (src_ip, dest_ip, protocol, length, timestamp))
                conn.commit()
                conn.close()

                # Print captured data for debugging
                print(f"Logged: {src_ip} -> {dest_ip} | Protocol: {protocol} | Size: {length} | Timestamp: {timestamp}")
                
                break  # Exit retry loop on success

            except sqlite3.OperationalError as e:
                if "database is locked" in str(e):
                    print(f"[⚠] Database is locked, retrying ({attempt + 1}/5)...")
                    time.sleep(0.5)  # Wait before retrying
                else:
                    raise  # Raise other errors

# Get the user-selected network interface
selected_interface = get_interface()
print(f"\n[✅] Sniffing started on interface: {selected_interface}")

# Start sniffing packets on the selected interface
sniff(prn=log_packet, store=False, iface=selected_interface)
