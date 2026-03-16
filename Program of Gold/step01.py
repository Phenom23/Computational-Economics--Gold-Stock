import pandas as pd
import matplotlib.pyplot as plt

# Φορτώνουμε το WORK αρχείο
work = pd.read_excel("WORK.xlsx")

# Παίρνουμε χρόνο και τιμή
x = work["Week"]
y = work["Price"]

# Φτιάχνουμε γράφημα χρονοσειράς
plt.figure()
plt.plot(x, y)
plt.title("Χρονοσειρά Τιμών Χρυσού")
plt.xlabel("Χρόνος (εβδομάδες)")
plt.ylabel("Τιμή Χρυσού")
plt.grid(True)

# Αποθήκευση γραφήματος ως εικόνα
plt.savefig("step01_time_series.png")
plt.show()
