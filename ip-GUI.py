import tkinter as tk
import subprocess
import re
import random
from tkinter import ttk

class IPChangerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("IP Changer")
        self.master.geometry("400x300")
        self.master.resizable(False, False)

        # Detect Ethernet interface name
        self.eth_interface_name = self.detect_eth_interface_name()

        # Create IP address label
        self.ip_label = tk.Label(self.master, text="Current IP: " + self.get_current_ip())
        self.ip_label.pack(pady=10)

        # Create change IP button
        self.change_ip_button = tk.Button(self.master, text="Change IP", command=self.change_ip)
        self.change_ip_button.config(borderwidth=0, highlightthickness=0, relief="flat", bg="#4CAF50", fg="white", padx=10, pady=5, font=("Arial", 12), cursor="hand2")
        self.change_ip_button.pack(pady=10)

        # Create quit button
        self.quit_button = tk.Button(self.master, text="Quit", command=self.master.quit)
        self.quit_button.config(borderwidth=0, highlightthickness=0, relief="flat", bg="#F44336", fg="white", padx=10, pady=5, font=("Arial", 12), cursor="hand2")
        self.quit_button.pack(pady=10)

        # Create network status graph
        self.network_status_label = tk.Label(self.master, text="Network Connectivity Status")
        self.network_status_label.pack(pady=10)

        self.network_status_graph = ttk.Progressbar(self.master, orient='horizontal', mode='determinate', length=300)
        self.network_status_graph.pack(pady=10)

        # Update network status graph
        self.update_network_status()

    def detect_eth_interface_name(self):
        # Run ifconfig command to get network interface names and IP addresses
        output = subprocess.check_output(["ifconfig"]).decode()

        # Use regular expression to extract Ethernet interface name
        eth_regex = r"en\w+"
        eth_interface_name = re.search(eth_regex, output)

        # Return Ethernet interface name
        return eth_interface_name.group()

    def get_current_ip(self):
        # Run ifconfig command to get network interface names and IP addresses
        output = subprocess.check_output(["ifconfig"]).decode()

        # Use regular expression to extract current IP address
        ip_regex = r"inet \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
        ip_address = re.search(ip_regex, output)

        # Return current IP address
        return ip_address.group().split()[1]

    def change_ip(self):
        # Generate random IP address
        new_ip = "192.168." + str(random.randint(1, 255)) + "." + str(random.randint(1, 255))

        # Bring Ethernet interface down
        subprocess.run(["ifconfig", self.eth_interface_name, "down"])

        # Change IP address
        subprocess.run(["ifconfig", self.eth_interface_name, new_ip])

        # Bring Ethernet interface back up
        subprocess.run(["ifconfig", self.eth_interface_name, "up"])

        # Update IP address label
        self.ip_label.config(text="Current IP: " + self.get_current_ip())

        # Update network status graph
        self.update_network_status()

    def update_network_status(self):
        # Ping Google DNS server to check network connectivity
        ping_output = subprocess.check_output(["ping", "-c", "1", "8.8.8.8"]).decode()

        # Use regular expression to extract packet loss percentage
        packet_loss_regex = r"(\d+)% packet loss"
        packet_loss_match = re.search(packet_loss_regex, ping_output)

        if packet_loss_match:
            packet_loss_percent = int(packet_loss_match.group(1))
            network_status = 100 - packet_loss_percent
        else:
            network_status = 0

        # Update network status graph
        self.network_status_graph["value"] = network_status

        # Set graph color based on network status
        if network_status >= 75:
            self.network_status_graph["style"] = "green.Horizontal.TProgressbar"
        elif network_status >= 50:
            self.network_status_graph["style"] = "yellow.Horizontal.TProgressbar"
        else:
            self.network_status_graph["style"] = "red.Horizontal.TProgressbar"

        # Schedule the next update after 1 second
        self.master.after(1000, self.update_network_status)

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.theme_use('default')
    style.configure("green.Horizontal.TProgressbar", foreground='green', background='green')
    style.configure("yellow.Horizontal.TProgressbar", foreground='yellow', background='yellow')
    style.configure("red.Horizontal.TProgressbar", foreground='red', background='red')
    app = IPChangerGUI(root)
    root.mainloop()
