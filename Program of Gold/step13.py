import pandas as pd
import matplotlib.pyplot as plt

# Φορτώνουμε WORK
work = pd.read_excel("WORK.xlsx")

# Παίρνουμε τη χρονοσειρά στοχαστικότητας
x_n = work["Stochastic"]

# Δημιουργούμε τη μετατοπισμένη σειρά κατά 1 βήμα (X_{n+1})
# shift(-1) σημαίνει “πάνω”: η επόμενη τιμή έρχεται στην τωρινή γραμμή
x_n1 = x_n.shift(-1)

# Αποθηκεύουμε τη μετατοπισμένη στήλη στο WORK
work["Stochastic_shifted"] = x_n1

# Για το scatter θέλουμε ζευγάρια που δεν έχουν NaN (τελευταία γραμμή θα είναι NaN)
pairs = work[["Stochastic", "Stochastic_shifted"]].dropna()

# Φτιάχνουμε το διάγραμμα X_{n+1} (Υ) ως προς X_n (Χ)
plt.figure()

# Μικρά/λεπτά σημεία: s=1 (μέγεθος), linewidths=1 (λεπτό περίγραμμα)
plt.scatter(
    pairs["Stochastic_shifted"],
    pairs["Stochastic"],
    s=1,
    linewidths=1
)

# Λεπτή γραμμή που ενώνει τα σημεία με τη χρονική σειρά
plt.plot(pairs["Stochastic_shifted"], pairs["Stochastic"], linewidth=0.5)

# Τίτλος και άξονες
plt.title("Διάγραμμα X(n+1) ως προς X(n) (Στοχαστικότητα)")
plt.xlabel("X(n) = Stochastic (shifted)")
plt.ylabel("X(n+1) = Stochastic")
plt.grid(True)

# Αποθηκεύουμε εικόνα
plt.savefig("step13_lag_plot.png")
plt.show()

# Αποθηκεύουμε το ενημερωμένο WORK.xlsx
work.to_excel("WORK.xlsx", index=False)
