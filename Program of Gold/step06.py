import pandas as pd
import matplotlib.pyplot as plt

# Φορτώνουμε το WORK αρχείο
work = pd.read_excel("WORK.xlsx")

# Παίρνουμε τη στήλη Price
price = work["Price"]

# Υπολογίζουμε τις πρώτες διαφορές
# Η πρώτη γραμμή δεν έχει προηγούμενη τιμή, οπότε θα βγει NaN
first_diff = price.diff()

# Αποθηκεύουμε τη νέα στήλη στο WORK
work["FirstDiff"] = first_diff

# Εκτυπώνουμε τις πρώτες 10 γραμμές για έλεγχο
print(work[["Week", "Price", "FirstDiff"]].head(10))

# Γράφημα πρώτων διαφορών
plt.figure()
plt.plot(work["Week"], work["FirstDiff"])
plt.title("Χρονοσειρά Πρώτων Διαφορών")
plt.xlabel("Χρόνος (εβδομάδες)")
plt.ylabel("Πρώτη Διαφορά (ΔPrice)")
plt.grid(True)
plt.savefig("step06_first_differences.png")
plt.show()

# Αποθηκεύουμε το ενημερωμένο WORK.xlsx
work.to_excel("WORK.xlsx", index=False)
