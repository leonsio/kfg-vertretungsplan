# Installation via HACS

## 1. GitHub Repository

Dieses Repository ist für HACS vorbereitet.

## 2. HACS

1. HACS → Integrationen
2. Menü `⋮` → Benutzerdefinierte Repositories
3. `https://github.com/leonsio/kfg-vertretungsplan` eintragen
4. Kategorie `Integration`
5. Repository hinzufügen
6. `KFG Vertretungsplan` installieren
7. Home Assistant neu starten

## 3. Integration konfigurieren

Einstellungen → Geräte & Dienste → Integration hinzufügen → KFG Vertretungsplan.

## 4. Dashboard-Karte

Die Karte liegt unter `frontend/vertretungsplan-card.js`.

Nach HACS-Installation kann sie nach `/config/www/kfg-vertretungsplan/vertretungsplan-card.js` kopiert werden.

Dann als Lovelace-Ressource hinzufügen:

`/local/kfg-vertretungsplan/vertretungsplan-card.js`

Typ: `JavaScript-Modul`.

Danach in einer manuellen YAML-Karte:

```yaml
type: custom:kfg-vertretungsplan-card
sensor: sensor.vertretungsplan
selected_entity: input_text.vertretungsplan_klassen
```

Zusätzlich muss der Helper angelegt werden:

```yaml
input_text:
  vertretungsplan_klassen:
    name: Ausgewählte Klassen
    max: 255
```

Die Karte bietet anklickbare Klassen-Chips. Mehrere Klassen können gleichzeitig ausgewählt werden.
