import pandas as pd
import numpy as np

# Διαβάζουμε το CSV
raw = pd.read_csv("Gold Futures Historical Data.csv", sep=";")

# Μετατρέπουμε τη στήλη Date σε ημερομηνία
raw["Date"] = pd.to_datetime(raw["Date"], errors="coerce", dayfirst=False)

# Συνάρτηση καθαρισμού αριθμών
def parse_number(s):
    s = str(s).strip()
    if s == "" or s.lower() == "nan":
        return np.nan

    if ("," in s) and ("." in s):
        if s.rfind(".") > s.rfind(","):
            s = s.replace(",", "")
        else:
            s = s.replace(".", "").replace(",", ".")
        return s

    if "," in s:
        return s.replace(",", ".")
    return s

# Καθαρισμός στηλών
raw["Price_num"] = pd.to_numeric(raw["Price"].astype(str).map(parse_number), errors="coerce")
raw["High_num"]  = pd.to_numeric(raw["High"].astype(str).map(parse_number), errors="coerce")
raw["Low_num"]   = pd.to_numeric(raw["Low"].astype(str).map(parse_number), errors="coerce")

# Διάστημα ημερομηνιών
start_date = pd.Timestamp("2024-09-15")
end_date   = pd.Timestamp("2025-08-24")

data = raw[(raw["Date"] >= start_date) & (raw["Date"] <= end_date)].copy()
data = data.sort_values("Date").reset_index(drop=True)

# Υπολογισμοί
data["S_High"] = data["High_num"]
data["T_Low"] = data["Low_num"]
data["U_PrevPrice"] = data["Price_num"].shift(1)

data["V_HighMinusLow"] = (data["S_High"] - data["T_Low"]).abs()
data["W_HighMinusPrev"] = (data["S_High"] - data["U_PrevPrice"]).abs()
data["X_LowMinusPrev"] = (data["T_Low"] - data["U_PrevPrice"]).abs()

data["Y_Max"] = data[[
    "V_HighMinusLow",
    "W_HighMinusPrev",
    "X_LowMinusPrev"
]].max(axis=1)

# Υπολογισμοί δεικτών
Y_nonan = data["Y_Max"].dropna()
U_nonan = data["U_PrevPrice"].dropna()

Z  = Y_nonan.iloc[:30].mean()
AA = U_nonan.iloc[:50].std(ddof=0)
AB = U_nonan.iloc[:50].mean()

AC = (AA / AB) * 100
AD = (Z / AB) * 100

# ===== Συμπεράσματα =====

# Ομοιογένεια
if AC > 10:
    homogeneity = "ΜΗ ΟΜΟΙΟΓΕΝΗΣ"
else:
    homogeneity = "ΟΜΟΙΟΓΕΝΗΣ"

# Σταθερότητα
if AD < 3:
    stability = "ΣΤΑΘΕΡΗ"
elif AD < 5:
    stability = "ΑΣΘΕΝΩΣ ΑΣΤΑΘΗΣ"
elif AD < 10:
    stability = "ΑΣΤΑΘΗΣ"
else:
    stability = "ΠΛΗΡΩΣ ΑΣΤΑΘΗΣ"

# ===== Output =====
print("Z (AVERAGE Y, 30 τιμές) =", round(Z, 4))
print("AA (STDEV.P U, 50 τιμές) =", round(AA, 4))
print("AB (AVERAGE U, 50 τιμές) =", round(AB, 4))
print("AC = (AA/AB)*100 (%) =", round(AC, 2))
print("AD = (Z/AB)*100 (%) =", round(AD, 2))

print("\n--- ΣΥΜΠΕΡΑΣΜΑ ---")
print(f"Ομοιογένεια: {homogeneity}")
print(f"Κατάσταση ευστάθειας: {stability}")

