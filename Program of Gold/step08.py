import pandas as pd
import matplotlib.pyplot as plt

# Φορτώνουμε το WORK αρχείο
work = pd.read_excel("WORK.xlsx")

# Παίρνουμε τη στήλη Price (αρχική χρονοσειρά)
price = work["Price"]

# Υπολογίζουμε τη στήλη PctDiff
percent_diff = ((price - price.shift(1)) / price) * 100

# Αποθηκεύουμε τη νέα στήλη στο WORK
work["PctDiff"] = percent_diff

# Αποθηκεύουμε ξανά το WORK.xlsx για να κρατήσουμε τη στήλη
work.to_excel("WORK.xlsx", index=False)

# Παίρνουμε τις τιμές που αντιστοιχούν στο J3:J513 (από τη 2η τιμή και μετά)
j_values = work["PctDiff"].dropna()

# Υπολογίζουμε το πλήθος των παρατηρήσεων
total = len(j_values)

# Ορίζουμε τα διαστήματα και τις μέσες τιμές
intervals = ["(-15,-10)", "(-10,-5)", "(-5,0)", "(0,5)", "(5,10)", "(10,15)"]
midpoints = [-12.5, -7.5, -2.5, 2.5, 7.5, 12.5]

# Υπολογίζουμε Πληθικότητα
count1 = (j_values < -10).sum()
count2 = ((j_values > -10) & (j_values < -5)).sum()
count3 = ((j_values > -5) & (j_values < 0)).sum()
count4 = ((j_values > 0) & (j_values < 5)).sum()
count5 = ((j_values > 5) & (j_values < 10)).sum()
count6 = (j_values > 10).sum()

# Φτιάχνουμε λίστα με τις πληθικότητες
counts = [count1, count2, count3, count4, count5, count6]

# Υπολογίζουμε ποσοστιαία κατανομή (%)
percentages = [c / total * 100 for c in counts]

# Δημιουργούμε τον πίνακα αποτελεσμάτων
table = pd.DataFrame({
    "Διαστήματα": intervals,
    "Πληθικότητα": counts,
    "Ποσοστό (%)": percentages,
    "Μέση τιμή": midpoints
})

# Εμφανίζουμε τον πίνακα στην οθόνη
print(table)

# Αποθήκευση πίνακα ως εικόνα
fig, ax = plt.subplots()
ax.axis("off")

# Μορφοποίηση αριθμών
table_display = table.copy()
table_display["Ποσοστό (%)"] = table_display["Ποσοστό (%)"].map(lambda v: f"{v:.2f}")

table_obj = ax.table(
    cellText=table_display.values,
    colLabels=table_display.columns,
    cellLoc="center",
    loc="center"
)

table_obj.auto_set_font_size(False)
table_obj.set_fontsize(10)
table_obj.scale(1.2, 1.2)

plt.title("Ποσοστιαία κατανομή συχνοτήτων (PctDiff)", pad=12)
plt.savefig("step08_table.png", bbox_inches="tight")
plt.close(fig)

# Ραβδόγραμμα: Πληθικότητα vs Μέση τιμή 
plt.figure()
plt.bar(midpoints, counts, width=4)  # width=4 για να ταιριάζει με εύρος #διαστημάτων 5 μονάδων
plt.title("Ραβδόγραμμα Πληθικότητας ανά Διάστημα")
plt.xlabel("Μέση τιμή διαστήματος")
plt.ylabel("Πληθικότητα")
plt.grid(True)

# Αποθήκευση ραβδογράμματος
plt.savefig("step08_frequency_barchart.png")
plt.show()


# Αποθήκευση του πίνακα σε νέο sheet μέσα στο WORK.xlsx
# Γράφουμε τον πίνακα σε ξεχωριστό sheet "Q8_Distribution" 
with pd.ExcelWriter("WORK.xlsx", engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
    table.to_excel(writer, sheet_name="Q8_Distribution", index=False)
