import pandas as pd
import matplotlib.pyplot as plt

# Φορτώνουμε WORK
work = pd.read_excel("WORK.xlsx")

# Παίρνουμε τη χρονοσειρά Price
price = work["Price"]

# Υπολογίζουμε κινητό μέσο όρο 20 βημάτων
# min_periods=20 σημαίνει ότι πριν συμπληρωθούν 20 τιμές θα είναι NaN (σαν “δεν υπάρχει”)
work["MA20"] = price.rolling(window=20, min_periods=20).mean()

# Υπολογίζουμε κινητό μέσο όρο 50 βημάτων
work["MA50"] = price.rolling(window=50, min_periods=50).mean()

# Αποθηκεύουμε τις νέες στήλες στο WORK.xlsx
work.to_excel("WORK.xlsx", index=False)

# Γράφημα MA20
plt.figure()
plt.plot(work["Week"], work["MA20"])
plt.title("Κινητός Μέσος Όρος 20 βημάτων")
plt.xlabel("Χρόνος (εβδομάδες)")
plt.ylabel("MA20")
plt.grid(True)
plt.savefig("step15_ma20.png")
plt.show()

# Γράφημα MA50
plt.figure()
plt.plot(work["Week"], work["MA50"])
plt.title("Κινητός Μέσος Όρος 50 βημάτων")
plt.xlabel("Χρόνος (εβδομάδες)")
plt.ylabel("MA50")
plt.grid(True)
plt.savefig("step15_ma50.png")
plt.show()

# Εκτύπωση για έλεγχο
print("\nΤελευταίες 3 τιμές MA20:")
print(work["MA20"].dropna().tail(3))

print("\nΤελευταίες 3 τιμές MA50:")
print(work["MA50"].dropna().tail(3))
