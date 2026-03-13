# program to solve Annunity plan problem

# collecting input for payment per period
PMT = float(input("Enter Payment per period (PMT): "))

# collecting input for rate
R = float(input("Enter Rate (R):"))

# collect input for the number of times intrest increase

N = float(input("Enter number of times interest applied in the year (N):"))


# collecting input for time

T = float(input("Enter Time (T):"))

# calculating the value for annunity plan

A = PMT * ((1 + R/n) ** (n * t) - 1) / (R/n)

print("Amount:", A)