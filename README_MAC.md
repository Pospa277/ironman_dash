# 🍎 Ironman Dashboard pro Mac - Stručný návod

## 🚀 Nejrychlejší způsob spuštění

### Krok 1: Stáhni projekt
```bash
git clone https://github.com/Pospa277/ironman_dash.git
cd ironman_dash
```

### Krok 2: Spusť launcher
Dvojklik na soubor: **`Start_Ironman_Dashboard.command`**

**To je všechno!** 🎉

---

## Co se stane při prvním spuštění?

1. ✅ Zkontroluje Python 3
2. ✅ Automaticky nainstaluje Flask (pokud chybí)
3. ✅ Spustí dashboard server
4. ✅ Otevře prohlížeč na http://localhost:5000
5. ✅ Hotovo!

---

## Možná varování při prvním spuštění

### "Cannot be opened because it is from an unidentified developer"

**Řešení:**
1. Pravý klik na `Start_Ironman_Dashboard.command`
2. Vyber **"Open"** (Otevřít)
3. Klikni **"Open"** v dialogu
4. Příště už půjde normálně dvojklikem

---

## Co když nemám Python?

Launcher ti řekne! Nainstaluj:

**Možnost 1 - Homebrew (doporučeno):**
```bash
brew install python3
```

**Možnost 2 - python.org:**
Stáhni z: https://www.python.org/downloads/

---

## Port 5000 je obsazený?

Na Macu často běží **AirPlay Receiver** na portu 5000.

**Launcher to automaticky vyřeší** a použije port 8080.

Nebo vypni AirPlay:
- System Preferences → Sharing → Vypni "AirPlay Receiver"

---

## Chceš vytvořit skutečnou Mac aplikaci?

Pokud chceš `Ironman Dashboard.app` kterou můžeš přidat do Applications:

```bash
# Nainstaluj PyInstaller
pip3 install pyinstaller

# Spusť build script
python3 build_mac_app.py

# Vyber možnost 2 nebo 3
```

Výsledek: `dist/Ironman Dashboard.app` 🎁

---

## Rychlé odkazy

- **Spuštění:** Dvojklik na `Start_Ironman_Dashboard.command`
- **Dashboard:** http://localhost:5000
- **Training Plan:** http://localhost:5000/training-plan
- **Stop:** Stiskni `Ctrl+C` v terminálu

---

## Potřebuješ detaily?

Podívej se na:
- **MAC_SETUP.md** - Detailní troubleshooting
- **MAC_APP_INSTALLATION.md** - Pokročilé buildování
- **README.md** - Kompletní dokumentace

---

**Užij si trénink!** 🏊‍♂️🚴‍♂️🏃‍♂️
