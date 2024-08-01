import re

data = open('./orig.py').read().splitlines()
# data = ["""ooo""", "ooo","hehe.__getitem__(17106^17105).__pow__(8).__eq__(11716593810022656)"]
print(data[2])
# Define a regular expression pattern to match the required data
pattern = r"\.__getitem__\(([0-9^]+)\)\.__pow__\((\d+)\)\.__eq__\((\d+)\)"

# Find all matches in the data string
matches = re.findall(pattern, data[2])
flag = [None for _ in range(51)]
if matches:
    # Process each match
    for match in matches:
        getitem_data = int(eval(match[0]))  # Data inside __getitem__ parentheses (including numbers, spaces, and ^ character)
        pow_data = int(match[1])  # Data inside __pow__ parentheses (only numbers)
        eq_data = int(match[2])   # Data inside __eq__ parentheses (only numbers)

        # Remove any spaces from getitem_data
        # getitem_data = getitem_data.replace(" ", "")

        assert flag[getitem_data] is None
        flag[getitem_data] = round(eq_data**(1/pow_data))
        # print(pow_data,getitem_data,flag[getitem_data])
else:
    print("Pattern not found in the data.")
print(len(matches))
print(''.join(chr(i) for i in flag))