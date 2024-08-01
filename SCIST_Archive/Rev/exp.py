with open('rev', 'rb') as input_file:
    bytes_data = input_file.read()

reversed_bytes = bytes_data[::-1]

with open('ver', 'wb') as output_file:
    output_file.write(reversed_bytes)