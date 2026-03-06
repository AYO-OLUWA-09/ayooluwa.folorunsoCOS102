# Program to solve simple intrest problem

# collecting input for principal
P = float(input("Enter Principal (P): "))

# collecting input for rate
R = float(input("Enter Rate (R):"))

# collecting input for time

T = float(input("Enter Time (T):"))

# Calculation for A

A = P * (1 + (R/100) * T)

print("Amount =", A)