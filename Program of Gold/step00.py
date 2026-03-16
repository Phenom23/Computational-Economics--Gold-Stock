import pandas as pd

csv_file = "Gold Futures Historical Data.csv"

# Διαβάζουμε το CSV με σωστό διαχωριστικό ';'
raw = pd.read_csv(csv_file, sep=";")

# Παίρνουμε τη στήλη Price σαν κείμενο
price_text = raw["Price"].astype(str).str.strip()


def parse_price(s: str):
    s = str(s).strip()

    if s == "":
        return None

# Αν υπάρχουν και ',' και '.', αποφασίζουμε ποιο είναι δεκαδικό από το ποιο είναι πιο δεξιά
    if ("," in s) and ("." in s):
        last_comma = s.rfind(",")
        last_dot = s.rfind(".")

# Αν η τελεία είναι πιο δεξιά, τότε '.' είναι δεκαδικό και ',' είναι χιλιάδες (US μορφή)
        if last_dot > last_comma:
            s = s.replace(",", "")   # αφαιρούμε χιλιάδες η '.' μένει ως δεκαδικό, δεν χρειάζεται αλλαγή
            return s

# Αν το κόμμα είναι πιο δεξιά, τότε ',' είναι δεκαδικό και '.' είναι χιλιάδες (EU μορφή)
        else:
            s = s.replace(".", "")   # αφαιρούμε χιλιάδες
            s = s.replace(",", ".")  # κάνουμε δεκαδικό '.'
            return s

    # Αν υπάρχει μόνο ',', το θεωρούμε δεκαδικό (EU)
    if ("," in s) and ("." not in s):
        s = s.replace(",", ".")
        return s

    # Αν υπάρχει μόνο '.', είναι ήδη ΟΚ (US/standard)
    return s

# Εφαρμόζουμε μετατροπή σε όλη τη στήλη
price_clean_text = price_text.map(parse_price)

# Μετατροπή σε αριθμούς
price_num = pd.to_numeric(price_clean_text, errors="coerce")

# Κρατάμε τις πρώτες 512 τιμές (B2:B513)
price_512 = price_num.iloc[0:512]

# Έλεγχος NaN
nan_count = price_512.isna().sum()
print("Πλήθος Nan στις 512 τιμές:", nan_count)

# Αν υπάρχουν NaN, δείχνουμε δείγμα
if nan_count > 0:
    bad_rows = price_512[price_512.isna()].index[:10]
    print("\n Δείγμα προβληματικών τιμών (raw Price):")
    for idx in bad_rows:
        print(idx, "->", raw.loc[idx, "Price"])

# Φτιάχνουμε Week 1..512
week = pd.Series(range(1, 513))

# Φτιάχνουμε WORK DataFrame
work = pd.DataFrame({
    "Week": week,
    "Price": price_512.values
})

# Αποθήκευση
work.to_excel("WORK.xlsx", index=False)

# Επιβεβαίωση
print("\n Πρώτες 5 γραμμές του WORK.xlsx:")
print(work.head())
