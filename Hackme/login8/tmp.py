import urllib.parse
import hashlib

def url_decode_and_sha512(url):
    # Decode the URL
    decoded_url = urllib.parse.unquote(url)
    print(decoded_url)    
    # Calculate SHA-512 hash
    sha512_hash = hashlib.sha512(decoded_url.encode()).hexdigest()
    
    return sha512_hash

if __name__ == "__main__":
    # Example usage
    input_url = input("Enter the URL to decode and calculate SHA-512 hash: ")
    sha512_hash = url_decode_and_sha512(input_url)
    print(sha512_hash)
