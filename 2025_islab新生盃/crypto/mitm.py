#!/usr/bin/env python3

import socket
import os
import time
import threading
import hashlib
import secrets
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

# --- Server Settings ---
HOST = '0.0.0.0'
PORT = 1337
FLAG_FILE = 'flag.txt'

def get_flag():
    if not os.path.exists(FLAG_FILE):
        return "flag{file_not_found_on_server}"
    with open(FLAG_FILE, 'r') as f:
        return f.read().strip()

def handle_connection(conn, addr):
    print(f"[+] New connection from {addr[0]}:{addr[1]}, for which a separate thread has been created.")
    try:
        # --- Beginning of eavesdropping scenario ---
        conn.sendall(b"----- MITM Attack Initialized. Intercepting encrypted channel -----\n\n")
        time.sleep(1)

        # --- 1. Diffie-Hellman parameters ---
        p = 155214169224186174245759019817233758959712483609876556421679567759735878173206273314271380424223420051598278563855517852997101246947883176353747918435174813511975576536353646684036755728974423538143090186411163821396091652013002565116673426504500657692938270440503451481091007910872038288051399770068237950977
        g = 5

        # --- 2. Initial Handshake ---
        conn.sendall(b"Alice: Hello Bob, initiating secure channel.\n")
        time.sleep(1)
        conn.sendall(b"Bob: Hello Alice, I am ready.\n\n")
        time.sleep(1)

        # --- 3. Key Exchange ---
        # Alice generates private key a and calculates public key A
        alice_private_key = secrets.randbelow(p - 101) + 100 # Ensure a >= 100
        alice_public_key = pow(g, alice_private_key, p)
        conn.sendall(f"Alice -> Bob (Public Key): {alice_public_key}\n".encode('utf-8'))
        time.sleep(1)

        # Bob generates private key b and calculates public key B
        bob_private_key = secrets.randbelow(p - 101) + 100 # Ensure b >= 100
        bob_public_key = pow(g, bob_private_key, p)
        conn.sendall(f"Bob -> Alice (Public Key): {bob_public_key}\n\n".encode('utf-8'))
        time.sleep(1)
        
        # --- 4. Calculate shared secret & generate symmetric key ---
        # The server simulates Alice and calculates the shared secret (g^b)^a mod p
        shared_secret_alice = pow(bob_public_key, alice_private_key, p)

        # The server also simulates Bob to calculate the shared secret (g^a)^b mod p
        shared_secret_bob = pow(alice_public_key, bob_private_key, p)

        # Server-side verification to ensure the algorithm is implemented correctly
        if shared_secret_alice == shared_secret_bob:
            print("[V] Verification successful! Computed the same shared secret.")

        # Convert the shared secret (a large number) to a 32-byte key using SHA-256
        secret_bytes = shared_secret_alice.to_bytes((shared_secret_alice.bit_length() + 7) // 8, byteorder='big')
        symmetric_key = hashlib.sha256(secret_bytes).digest()

        # --- 5. Use AES-256-CBC to encrypt and send the message ---
        conn.sendall(b"Alice: Message is encrypted. Here it is.\n")
        
        # Encrypt Alice's message
        flag = get_flag()
        alice_part = flag[:10]
        plaintext_alice = f"Great. The first part is: {alice_part}".encode('utf-8')
        
        iv_alice = get_random_bytes(AES.block_size) # Generate a random 16-byte IV
        cipher_alice = AES.new(symmetric_key, AES.MODE_CBC, iv_alice)
        ciphertext_alice = cipher_alice.encrypt(pad(plaintext_alice, AES.block_size))
        
        encrypted_message_alice = iv_alice.hex() + ciphertext_alice.hex()
        conn.sendall(f"Alice -> Bob (Encrypted): {encrypted_message_alice}\n".encode('utf-8'))
        time.sleep(1)

        # Encrypt Bob's message
        bob_part = flag[10:]
        plaintext_bob = f"Perfect! I have the rest. It's: {bob_part}".encode('utf-8')
        
        iv_bob = get_random_bytes(AES.block_size) # A new IV must be used for each encryption
        cipher_bob = AES.new(symmetric_key, AES.MODE_CBC, iv_bob)
        ciphertext_bob = cipher_bob.encrypt(pad(plaintext_bob, AES.block_size))
        
        encrypted_message_bob = iv_bob.hex() + ciphertext_bob.hex()
        conn.sendall(f"Bob -> Alice (Encrypted): {encrypted_message_bob}\n\n".encode('utf-8'))
        
        # --- End of eavesdropping scenario ---
        conn.sendall(b"----- Target communication terminated. Eavesdropping channel closed -----\n")

    except Exception as e:
        print(f"[!] Error handling connection from {addr[0]}:{addr[1]}: {e}")
    finally:
        conn.close()
        print(f"[-] Connection with {addr[0]}:{addr[1]} closed, thread terminated.")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Allow address reuse to avoid "Address already in use" errors
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        s.bind((HOST, PORT))
        s.listen()
        
        print(f"[*] Multi-threaded server listening on {HOST}:{PORT}")
        
        while True:
            # Wait for and accept new connections
            conn, addr = s.accept()
            
            # Create a new thread for this connection
            client_thread = threading.Thread(target=handle_connection, args=(conn, addr))
            
            # Start the thread
            client_thread.start()

if __name__ == '__main__':
    main()