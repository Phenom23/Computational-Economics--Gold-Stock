import pandas as pd
import matplotlib.pyplot as plt

# Φορτώνουμε το WORK αρχείο
work = pd.read_excel("WORK.xlsx")

# Παίρνουμε τη χρονοσειρά στοχαστικότητας
stochastic = work["Stochastic"]

# Παίρνουμε τη χρονοσειρά ποσοστιαίων μεταβολών
j = work["PctDiff"]

# Φτιάχνουμε τη στήλη P = J * 100
p = j * 100

# Αποθηκεύουμε τη νέα στήλη στο WORK
work["P_like_FINANCE"] = p

# Φτιάχνουμε ζευγάρια (I, P) και πετάμε NaN γραμμές
pairs = work[["Stochastic", "P_like_FINANCE"]].dropna()

# Δημιουργούμε το φασικό πορτραίτο (scatter)
plt.figure()

# Σημεία (λεπτά)
plt.scatter(
    pairs["Stochastic"],
    pairs["P_like_FINANCE"],
    s=8,
    linewidths=0.3
)

# Λεπτή γραμμή που ενώνει τα σημεία με τη χρονική σειρά
plt.plot(
    pairs["Stochastic"],
    pairs["P_like_FINANCE"],
    linewidth=0.5
)

plt.title("Φασικό πορτραίτο (Stochastic vs P=J*100)")
plt.xlabel("Στοχαστικότητα (I)")
plt.ylabel("P = J * 100")
plt.grid(True)

# Αποθήκευση εικόνας
plt.savefig("step14_phase_portrait.png")

# Εμφάνιση
plt.show()

# Αποθήκευση ενημερωμένου WORK.xlsx
work.to_excel("WORK.xlsx", index=False)
