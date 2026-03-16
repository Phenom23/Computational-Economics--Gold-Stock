import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Φορτώνουμε το WORK αρχείο
work = pd.read_excel("WORK.xlsx")

# Παίρνουμε x και y
x = work["Week"].to_numpy(dtype=float)
y = work["Price"].to_numpy(dtype=float)

# Υπολογίζουμε a και b (γραμμική παλινδρόμηση trendline)
x_mean = x.mean()
y_mean = y.mean()
sxx = ((x - x_mean) ** 2).sum()
sxy = ((x - x_mean) * (y - y_mean)).sum()

a = sxy / sxx
b = y_mean - a * x_mean

# Υπολογίζουμε Τάση
trend = a * x + b
work["Trend"] = trend

# Υπολογίζουμε R2
sse = ((y - trend) ** 2).sum()
sst = ((y - y_mean) ** 2).sum()
r2 = 1 - (sse / sst)

print("y = a*x + b")
print("a =", a)
print("b =", b)
print("R^2 =", r2)

# Αποθήκευση στο WORK.xlsx
work.to_excel("WORK.xlsx", index=False)

# Γράφημα χρονοσειράς + τάσης
plt.figure()
plt.plot(x, y, label="Τιμές Χρυσού")
plt.plot(x, trend, label="Γραμμική Τάση")
plt.title("Χρονοσειρά και Γραμμική Τάση")
plt.xlabel("Χρόνος (εβδομάδες)")
plt.ylabel("Τιμή Χρυσού")
plt.legend()
plt.grid(True)
plt.savefig("step03_trendline.png")
plt.show()
