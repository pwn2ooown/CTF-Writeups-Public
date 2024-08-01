def char_diff(str1, str2):
    # Create dictionaries to store character counts
    count1 = {}
    count2 = {}
    
    # Count characters in str1
    for char in str1:
        if char in count1:
            count1[char] += 1
        else:
            count1[char] = 1
    
    # Count characters in str2
    for char in str2:
        if char in count2:
            count2[char] += 1
        else:
            count2[char] = 1
    
    # Create a set of all characters in both strings
    all_chars = set(count1.keys()).union(set(count2.keys()))
    
    # Compare counts and show differences
    diff = {}
    for char in all_chars:
        count_in_str1 = count1.get(char, 0)
        count_in_str2 = count2.get(char, 0)
        if count_in_str1 != count_in_str2:
            diff[char] = {
                "str1": count_in_str1,
                "str2": count_in_str2
            }
    
    return diff

# Example strings
str1 =__import__("string").printable
str2 = "0123456789abdefgijklmnopqstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'*,-./:;<>?@[\]^_`{|}~"

# Show the character differences
diff = char_diff(str1, str2)
for char, counts in diff.items():
    print(f"'{char}': str1={counts['str1']}, str2={counts['str2']}")
