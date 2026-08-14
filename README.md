# KFG Vertretungsplan

Home-Assistant-Custom-Integration für den schulweiten Untis-Vertretungsplan des Kaiserin-Friedrich-Gymnasiums.

Die Integration ruft die schulweite `w00000.htm` für die aktuelle und nächste ISO-Kalenderwoche ab und stellt die Daten als Sensorattribute bereit.

## Installation über HACS

Die Integration kann direkt aus dem GitHub-Repository als **Benutzerdefiniertes Repository** installiert werden.

1. Öffne in Home Assistant **HACS → Integrationen**.
2. Öffne oben rechts das Menü **⋮**.
3. Wähle **Benutzerdefinierte Repositories**.
4. Trage als Repository ein:

   `https://github.com/leonsio/kfg-vertretungsplan`

5. Wähle als Typ **Integration**.
6. Klicke auf **Hinzufügen**.
7. Suche anschließend in HACS nach **KFG Vertretungsplan** und öffne den Eintrag.
8. Klicke auf **Download** und installiere die aktuelle Version.
9. Starte Home Assistant anschließend neu.
10. Öffne **Einstellungen → Geräte & Dienste → Integration hinzufügen** und suche nach **KFG Vertretungsplan**.
11. Folge dem Einrichtungsdialog der Integration.

HACS dokumentiert das Hinzufügen eines benutzerdefinierten Repositories über **⋮ → Benutzerdefinierte Repositories**, die Auswahl des Repository-Typs und anschließend **Hinzufügen**. Nach dem Download wird eine HACS-Integration unter `custom_components/` installiert.

## Dashboard erstellen

Die Integration stellt den Vertretungsplan über den Sensor `sensor.vertretungsplan` bereit. Für die komfortable Darstellung ist zusätzlich die mitgelieferte Lovelace-Karte `frontend/vertretungsplan-card.js` vorgesehen.

### 1. Lovelace-Karte als Ressource einbinden

Kopiere die Datei `frontend/vertretungsplan-card.js` aus diesem Repository in den Home-Assistant-Konfigurationsordner, z. B. nach:

```text
/config/www/kfg-vertretungsplan/vertretungsplan-card.js
```

Falls der Ordner `/config/www` noch nicht existiert, erstelle ihn.

Öffne anschließend in Home Assistant:

**Einstellungen → Dashboards → ⋮ → Ressourcen**

und füge folgende Ressource hinzu:

```text
URL: /local/kfg-vertretungsplan/vertretungsplan-card.js
Typ: JavaScript-Modul
```

Home Assistant stellt Dateien aus `/config/www` über `/local` bereit. Nach dem Hinzufügen oder Aktualisieren einer Ressource sollte die Oberfläche neu geladen werden.

### 2. Dashboard anlegen

Öffne:

**Einstellungen → Dashboards → Dashboard hinzufügen**

und erstelle beispielsweise ein Dashboard mit dem Namen:

**Vertretungsplan**

Öffne anschließend das neue Dashboard und wähle:

**Karte hinzufügen → Manuell**

Füge die Vertretungsplan-Karte mit folgender Konfiguration ein:

```yaml
type: custom:vertretungsplan-card
entity: sensor.vertretungsplan
```

Speichere die Karte.

### 3. Klassen auswählen

Die Karte liest die verfügbaren Klassen aus den Daten des Vertretungsplan-Sensors. Mehrere Klassen können gleichzeitig ausgewählt werden.

Beispiel:

```text
[ 5b2 ✓ ] [ 6ac ] [ 7n ✓ ] [ 8b1 ] [ Q1 ]
```

In diesem Beispiel werden nur die Vertretungen für `5b2` und `7n` angezeigt.

Wenn keine Klasse ausgewählt ist, werden die verfügbaren Vertretungen für alle Klassen angezeigt.

### 4. Aktualisierung

Der Sensor wird von der Integration automatisch aktualisiert. Das Dashboard verwendet die aktuellen Daten des Sensors; eine manuelle Aktualisierung der Karte ist nicht erforderlich.

## Hinweise

- Für HACS muss das Repository als **Integration** hinzugefügt werden.
- Die Lovelace-Karte ist eine separate Frontend-Ressource und muss einmalig als Ressource registriert werden.
- Bei Änderungen an der JavaScript-Karte kann ein vollständiges Neuladen des Browsers erforderlich sein.
