#program to solve simple intrest problem

# collecting input for principal
P = float(input("Enter Principal (P): "))

# collecting input for rate
R = float(input("Enter Rate (R):"))

# collect input for the number of times intrest increase

N = float(input("Enter number of times interest applied in the year (N):"))


# collecting input for time

T = float(input("Enter Time (T):"))

# calculating the value for A

A = P * (1 + (R/N)) ** (N * T)

print("Amount =",A)