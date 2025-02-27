#!/bin/bash

# Run design script
./design.sh

# List available network interfaces
echo "Available network interfaces:"
ip -o link show | awk -F': ' '{print NR". "$2}'

echo ""
# Get the list of interfaces into an array
interfaces=($(ip -o link show | awk -F': ' '{print $2}'))

# Prompt user to select an interface by number
read -p "Enter the number corresponding to the network interface: " index
echo ""

# Validate user input
if [[ ! $index =~ ^[0-9]+$ ]] || [[ $index -lt 1 || $index -gt ${#interfaces[@]} ]]; then
    echo "❌ Invalid selection. Exiting."
    exit 1
fi

# Get the selected interface
interface=${interfaces[$((index-1))]}

echo "🔍 Running arp-scan on $interface..."
echo ""

# Run arp-scan with the selected interface and capture output
arp_output=$(sudo arp-scan -I "$interface" --localnet)

echo "📋 ARP-scan results with numbering:"
mapfile -t devices < <(echo "$arp_output" | awk '/^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+/ {count++; printf "%d. %s %s %s\n", count, $1, $2, $3}')

# Display numbered results
for i in "${!devices[@]}"; do
    echo "${devices[i]}"
done

# Prompt user to select MAC addresses by number
echo ""
read -p "Enter the numbers corresponding to the devices you want to whitelist (e.g., 2 or 1,2): " selection
echo ""

# Validate input and store MAC addresses
IFS=',' read -ra indices <<< "$selection"
for i in "${indices[@]}"; do
    if [[ $i =~ ^[0-9]+$ ]] && [[ $i -gt 0 && $i -le ${#devices[@]} ]]; then
        mac=$(echo "${devices[$((i-1))]}" | awk '{print $3}' | tr '[:upper:]' '[:lower:]')  # Convert to lowercase
        if grep -Fxq "$mac" whitelist.txt; then
            echo "✅ $mac is already whitelisted."
        else
            echo "$mac" >> whitelist.txt
            echo "✅ $mac is now whitelisted."
        fi
    else
        echo "❌ Invalid selection: $i"
    fi
done

echo ""
echo "✅ Whitelist configured. To add a new device, use: "
echo "   sudo ./white_list.sh"
