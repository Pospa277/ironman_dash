# 🍎 Návod pro Mac - Ironman Dashboard

## Krok za krokem spuštění na macOS

### 1️⃣ Ověř instalaci Pythonu

Otevři **Terminal** (Cmd+Space, napiš "Terminal") a zadej:

```bash
python3 --version
```

**Mělo by to vypsat:** `Python 3.8` nebo vyšší

#### Pokud Python není nainstalován:
```bash
# Nainstaluj Homebrew (pokud nemáš)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Nainstaluj Python
brew install python3
```

---

### 2️⃣ Přejdi do adresáře projektu

```bash
cd ~/Downloads/ironman_dash
# nebo kde máš projekt stažený
```

---

### 3️⃣ Vytvoř virtuální prostředí (doporučeno)

```bash
# Vytvoř virtuální prostředí
python3 -m venv venv

# Aktivuj ho
source venv/bin/activate
```

Po aktivaci uvidíš `(venv)` před promptem v terminálu.

---

### 4️⃣ Nainstaluj závislosti

```bash
pip install flask
```

Nebo nainstaluj všechny závislosti:
```bash
pip install -r requirements.txt
```

⚠️ **Poznámka:** Některé knihovny (jako reportlab pro PDF) můžou vyžadovat další nástroje.
Pro začátek stačí jen Flask.

---

### 5️⃣ Spusť aplikaci

```bash
cd web
python3 app.py
```

**Mělo by to vypsat:**
```
* Running on http://127.0.0.1:5000
* Running on http://0.0.0.0:5000
Press CTRL+C to quit
```

---

### 6️⃣ Otevři prohlížeč

Otevři Safari/Chrome a jdi na:
```
http://localhost:5000
```

---

## 🐛 Časté problémy a řešení

### Problém: "command not found: python3"

**Řešení:**
```bash
# Zkus jen "python"
python --version

# Pokud funguje, použij:
python app.py
```

---

### Problém: "Permission denied"

**Řešení:**
```bash
# Udělej run.sh spustitelný
chmod +x run.sh

# Nebo spusť přes bash
bash run.sh
```

---

### Problém: "ModuleNotFoundError: No module named 'flask'"

**Řešení:**
```bash
# Ujisti se, že máš aktivované virtuální prostředí
source venv/bin/activate

# Nainstaluj Flask
pip install flask
```

---

### Problém: "Address already in use" (Port 5000 obsazený)

**Řešení 1 - Změň port:**

Otevři `web/app.py` a na posledním řádku změň:
```python
app.run(debug=True, host='0.0.0.0', port=8080)  # Místo 5000
```

Pak jdi na `http://localhost:8080`

**Řešení 2 - Vypni službu na portu 5000:**
```bash
# Na Macu často běží AirPlay Receiver na portu 5000
# Vypni v: System Preferences > Sharing > AirPlay Receiver
```

---

### Problém: Import errors pro další moduly

**Řešení - Minimální instalace:**
```bash
# Nainstaluj jen to potřebné
pip install flask
```

Ostatní funkce (PDF export, Google Sheets) nejsou nutné pro základní fungování.

---

## ⚡ Rychlé spuštění (bez závislostí navíc)

Pokud chceš jen vyzkoušet dashboard bez všech funkcí:

1. **Edituj `requirements.txt`** - nech jen:
```
flask==3.0.0
```

2. **Nainstaluj:**
```bash
pip install flask
```

3. **Spusť:**
```bash
cd web
python3 app.py
```

---

## 📱 Test bez Apple Health dat

I bez upload můžeš prohlédnout:
- Training Plan stránku: `http://localhost:5000/training-plan`
- Design dashboardu
- UI a navigaci

---

## 🆘 Stále nefunguje?

### Pošli mi výstup těchto příkazů:

```bash
# 1. Verze Pythonu
python3 --version

# 2. Kde jsi
pwd

# 3. Co je v adresáři
ls -la

# 4. Co říká pip
pip list | grep -i flask

# 5. Zkus spustit a zkopíruj celou chybovou hlášku
cd web
python3 app.py
```

---

## ✅ Checklist

- [ ] Python3 nainstalován
- [ ] V správném adresáři (`ironman_dash/`)
- [ ] Virtuální prostředí aktivované
- [ ] Flask nainstalován (`pip install flask`)
- [ ] V adresáři `web/`
- [ ] Spuštěno `python3 app.py`
- [ ] Prohlížeč otevřený na `localhost:5000`

---

**Potřebuješ pomoct? Napiš mi přesnou chybovou hlášku!** 💪
