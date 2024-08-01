import codecs

# Define a function to decode Punycode
def decode_punycode(encoded_string):
    decoded_string = codecs.decode(encoded_string, 'punycode')
    return decoded_string

# Decoded Punycode string
decoded_string = decode_punycode('gdd7dd23l3by980a4baunja1d4ukc3a3e39172b4sagce87ciajq2bi5atq4b9b3a3cy0gqa9019gtar0ck')

# Check if the input matches the expected format
input_flag = input('Enter the flag: ')
expected_flag = 'DUCTF{%s}' % decoded_string
print(expected_flag.encode('utf-8').decode())
print('gdd7dd23l3by980a4baunja1d4ukc3a3e39172b4sagce87ciajq2bi5atq4b9b3a3cy0gqa9019gtar0ck'.decode('idna'))
if input_flag == expected_flag:
    print('Correct!')
else:
    print('Wrong!')