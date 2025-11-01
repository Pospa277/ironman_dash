# Quick Start Guide

## 🚀 Jak spustit Ironman Dashboard

### Krok 1: Nainstaluj závislosti

```bash
pip install -r requirements.txt
```

### Krok 2: Spusť Flask aplikaci

```bash
cd web
python app.py
```

### Krok 3: Otevři prohlížeč

Aplikace běží na: **http://localhost:5000**

---

## 📱 Jak použít dashboard

### 1. Export dat z Apple Health

Na iPhone:
1. Otevři aplikaci **Zdraví** (Health)
2. Klikni na svůj profil (vpravo nahoře)
3. Scrolluj dolů a vyber **Exportovat data o zdraví**
4. Ulož soubor `export.zip`
5. Rozbal ZIP a najdi soubor `export.xml`

### 2. Upload do dashboardu

1. Přejdi na http://localhost:5000
2. Přetáhni `export.xml` do upload oblasti
3. Klikni na "Upload & Analyze"
4. Počkej na zpracování (může trvat 30-60 sekund)

### 3. Zobraz analytics

Po uploadu uvidíš:
- 🎯 **Predikci času na Ironman závod**
- 📊 **Týdenní pokrok** vs. Ironman distance
- 📈 **Grafy pace trendu**
- 📄 **Export do PDF**
- 📱 **Sync do Google Sheets**

---

## ⚡ Rychlý test (bez Apple Health dat)

I bez Apple Health dat můžeš prohlédnout:
- **Training Plan** (12-týdenní plán)
- **UI a design**
- **Strukturu dashboardu**

---

## 🛠️ Troubleshooting

### Python není nainstalován
```bash
# Ubuntu/Debian
sudo apt install python3 python3-pip

# macOS
brew install python3
```

### Port 5000 je obsazený
V souboru `web/app.py` změň port na poslední řádce:
```python
app.run(debug=True, host='0.0.0.0', port=8080)  # Změň na jiný port
```

### Chyba při importu modulů
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 📚 Co dál?

- Prohlédni **README.md** pro detailní dokumentaci
- Zkontroluj **Training Plan** na `/training-plan`
- Vyzkoušej PDF export po uploadu dat
- Nastav Google Sheets sync (volitelné)

---

**Potřebuješ pomoct? Otevři issue na GitHubu!**
