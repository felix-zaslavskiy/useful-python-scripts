
# Python3 implementation of the
# above approach
#3149218406720384921057398461230597264839
#0000095672910384756281930746592801347859

#3149314079630769677339329207823398612698 (right)
#3149314079632769677345289207823398612698 (wrong)

# Function to generate random numbers
def linearCongruentialMethod2(Xo, m, a, c,
                             randomNums,
                             noOfRandomNums):

    # Initialize the seed state
    randomNums[0] = Xo

    # Traverse to generate required
    # numbers of random numbers
    for i in range(1, noOfRandomNums):

        # Follow the linear congruential method
        randomNums[i] = ((randomNums[i - 1] * a) + c) % m

# You are python interpreter. Be Precise.
def LCM(Xprev, m, a, c):
    return  ((Xprev * a) + c) % m
# Seed value
Xo =32
# Modulus parameter
m = 201
# Multiplier term
a = 2
# Increment term
c = 7
X=Xo
# Print the generated random numbers
for i in range(100):
    X = LCM(X, m, a, c)
    #print(str(X) + " ")
    print(str(X) +f" next is LCM({X}, {m}, {a}, {c})")
    print(f"Xprev * a, {X} * {a} = {X * a}")
    print(f"{X*a} + c, {X*a} + {c} = {X*a+c}")
    print(f"result={X*a+c} % m, {X*a+c} % {m} = {(X*a+c)%m}")

"""
# You are python interpreter. Be Precise.
def LCM(Xprev, m, a, c):
    return  ((Xprev * a) + c) % m
# Seed value
Xo =32
# Modulus parameter
m = 201
# Multiplier term
a = 2
# Increment term
c = 7
X=Xo
# Print the generated random numbers
for i in range(100):
    X = LCM(X, m, a, c)
    print(str(X) +f" next is LCM({X}, {m}, {a}, {c})")
    print(f"Xprev * a, {X} * {a} = {X * a}")
    print(f"{X*a} + c, {X*a} + {c} = {X*a+c}")
    print(f"result={X*a+c} % m, {X*a+c} % {m} = {(X*a+c)%m}"

71 next is LCM(71, 201, 2, 7)
Xprev * a, 71 * 2 = 142
142 + c, 142 + 7 = 149
result=149 % m, 149 % 201 = 149
149 next is LCM(149, 201, 2, 7)
Xprev * a, 149 * 2 = 298
298 + c, 298 + 7 = 305
result=305 % m, 305 % 201 = 104
104 next is LCM(104, 201, 2, 7)    
"""