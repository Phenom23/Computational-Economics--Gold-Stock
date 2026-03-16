import pandas as pd
import matplotlib.pyplot as plt

# Φορτώνουμε το WORK αρχείο
work = pd.read_excel("WORK.xlsx")

# Παίρνουμε τη στήλη Week για τον άξονα χρόνου
x = work["Week"]

# Παίρνουμε τη στήλη F (Price - Trend)
F = work["F"]

# Παίρνουμε τη στήλη Seasonality (εποχικότητα)
S = work["Seasonality"]

# Υπολογίζουμε τη στοχαστικότητα
stochastic = F - S

# Αποθηκεύουμε τη νέα στήλη στο WORK
work["Stochastic"] = stochastic

# Εκτυπώνουμε τις πρώτες 5 τιμές για έναν γρήγορο έλεγχο
print("Πρώτες 5 τιμές στοχαστικότητας:")
print(work["Stochastic"].head())

# Φτιάχνουμε γράφημα της στοχαστικότητας
plt.figure()
plt.plot(x, stochastic)
plt.title("Χρονοσειρά Στοχαστικότητας")
plt.xlabel("Χρόνος (εβδομάδες)")
plt.ylabel("Στοχαστικότητα")
plt.grid(True)

# Αποθηκεύουμε το γράφημα ως εικόνα
plt.savefig("step05_stochasticity.png")

# Εμφανίζουμε το γράφημα
plt.show()

# Αποθηκεύουμε το ενημερωμένο WORK.xlsx
work.to_excel("WORK.xlsx", index=False)
