# 🚀 Mac App Installation Guide

## Jednoduchá instalace - DOPORUČENO

### Varianta 1: Launcher Script (nejjednodušší) ⭐

1. **Stáhni projekt** z GitHubu
2. **Najdi soubor**: `Start_Ironman_Dashboard.command`
3. **Dvojklik** na tento soubor
4. První spuštění:
   - Možná se objeví varování o "neoprávněné aplikaci"
   - Klikni pravým tlačítkem → "Otevřít" → Potvrď
   - Nebo jdi do System Preferences → Security → "Open Anyway"
5. **Automaticky se:**
   - Zkontroluje Python
   - Nainstaluje Flask (pokud chybí)
   - Spustí dashboard
   - Otevře prohlížeč na http://localhost:5000

**✅ To je všechno! Při příštím spuštění jen dvojklik.**

---

## Pokročilá instalace - Standalone .app

### Varianta 2: Vytvoř Mac aplikaci (.app bundle)

Toto vytvoří skutečnou Mac aplikaci, kterou můžeš:
- Přesunout do Applications
- Spustit z Launchpadu
- Nesdílí závislosti s Pythonem

#### Postup:

1. **Nainstaluj PyInstaller:**
```bash
pip3 install pyinstaller
```

2. **Spusť build script:**
```bash
python3 build_mac_app.py
```

3. **Vyber možnost 2** (Build standalone .app bundle)

4. **Po dokončení:**
   - Najdeš `Ironman Dashboard.app` ve složce `dist/`
   - Přesuň ji kamkoliv (třeba Applications)
   - Dvojklik a spusť!

---

## Vytvoření DMG instalátoru

Chceš vytvořit profesionální DMG soubor (jako ostatní Mac aplikace)?

1. **Nainstaluj create-dmg:**
```bash
brew install create-dmg
```

2. **Spusť build script:**
```bash
python3 build_mac_app.py
```

3. **Vyber možnost 3** (Build both)

4. **Výsledek:**
   - `Ironman_Dashboard.dmg` - instalátor
   - Stačí otevřít DMG a přetáhnout app do Applications

---

## Co je nejlepší pro tebe?

### Launcher Script (Start_Ironman_Dashboard.command) ✅
**Výhody:**
- ✅ Funguje hned, žádné buildování
- ✅ Automatická instalace Flask
- ✅ Jednoduchý na používání
- ✅ Malý (jen pár KB)

**Nevýhody:**
- ❌ Potřebuje Python nainstalovaný
- ❌ Otevře se terminálové okno

### Standalone .app Bundle 🎁
**Výhody:**
- ✅ Žádné externí závislosti
- ✅ Vypadá jako normální Mac app
- ✅ Můžeš sdílet s ostatními
- ✅ Ikona v Launchpadu

**Nevýhody:**
- ❌ Větší velikost (~50-100 MB)
- ❌ Vyžaduje buildování
- ❌ Delší první spuštění

---

## Rychlý start (doporučený postup)

### Pro tebe osobně:
1. Použij **Launcher Script** → Stačí dvojklik
2. Pokud to funguje dobře a chceš to používat dlouhodobě...
3. Zbuilduješ si **.app bundle** pro čistší zkušenost

### Pro sdílení s ostatními:
- Vytvoř **DMG instalátor**
- Ostatní jen stáhnou DMG a nainstalují jako normální Mac app

---

## Troubleshooting

### "Permission denied" při spuštění .command souboru

```bash
chmod +x Start_Ironman_Dashboard.command
```

### "Cannot be opened because it is from an unidentified developer"

1. Pravý klik na soubor
2. Vyber "Open"
3. Klikni "Open" v dialogu
4. Nebo: System Preferences → Security & Privacy → "Open Anyway"

### Port 5000 obsazený (AirPlay)

Launcher automaticky použije port 8080. Nebo vypni AirPlay:
1. System Preferences → Sharing
2. Vypni "AirPlay Receiver"

---

## Co dostaneš?

Po spuštění máš:
- 🌐 **Web dashboard** na http://localhost:5000
- 📊 **Training analytics**
- 🎯 **Race predictions**
- 📄 **PDF export**
- 📱 **Google Sheets sync**
- 🏃 **12-week training plan**

---

## Potřebuješ pomoct?

1. Zkus nejdřív **Launcher Script** - je to nejjednodušší
2. Pokud to nefunguje, napiš mi přesnou chybu
3. Můžu ti pomoct s buildováním .app verze

**Všechno je připravené, stačí to spustit!** 🚀
