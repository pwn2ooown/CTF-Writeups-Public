def factorize(number):
    factors = []
    divisor = 2  # Start with the smallest prime number

    while number > 1:
        while number % divisor == 0:
            print(factors)
            factors.append(divisor)
            number //= divisor
        divisor += 1  # Move to the next potential factor

    return factors

# Example usage:
num = 6954494065942554678316751997792528753841173212407363342283423753536991947310058248515278 
result = factorize(num)
print(f"The factors of {num} are: {result}")