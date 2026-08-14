# KFG Vertretungsplan

Home-Assistant-Custom-Integration für den schulweiten Untis-Vertretungsplan des Kaiserin-Friedrich-Gymnasiums.

Die Integration ruft die schulweite `w00000.htm` für die aktuelle und nächste ISO-Kalenderwoche ab und stellt die Daten als Sensorattribute bereit.

## Installation über HACS

1. Öffne in Home Assistant **HACS → Integrationen**.
2. Öffne oben rechts das Menü **⋮**.
3. Wähle **Benutzerdefinierte Repositories**.
4. Trage als Repository ein:

   `https://github.com/leonsio/kfg-vertretungsplan`

5. Wähle als Typ **Integration**.
6. Klicke auf **Hinzufügen**.
7. Öffne in HACS den Eintrag **KFG Vertretungsplan**.
8. Klicke auf **Download**.
9. Starte Home Assistant neu.
10. Öffne **Einstellungen → Geräte & Dienste → Integration hinzufügen** und suche nach **KFG Vertretungsplan**.
11. Folge dem Einrichtungsdialog.

Die Lovelace-Karte ist Bestandteil der Integration. Nach der Installation wird die JavaScript-Datei automatisch aus der Integration bereitgestellt und von Home Assistant geladen. **Es ist kein Kopieren der Datei nach `/config/www` und keine manuelle Lovelace-Ressource erforderlich.** Home Assistant dokumentiert für Integrationen die Bereitstellung statischer Dateien über `async_register_static_paths`; die Integration nutzt diesen Mechanismus und lädt die Karte anschließend automatisch. citeturn3search1turn3search5

## Dashboard erstellen

### 1. Dashboard anlegen

Öffne:

**Einstellungen → Dashboards → Dashboard hinzufügen**

und erstelle beispielsweise ein Dashboard mit dem Namen:

**Vertretungsplan**

### 2. Karte hinzufügen

Öffne das neue Dashboard und wähle:

**Karte hinzufügen → Manuell**

Füge folgende Konfiguration ein:

```yaml
type: custom:kfg-vertretungsplan-card
sensor: sensor.vertretungsplan
selected_entity: input_text.vertretungsplan_klassen
```

Speichere die Karte.

Nach der Installation der Integration sollte die Karte bereits als **KFG Vertretungsplan** verfügbar sein. Eine zusätzliche JavaScript-Ressource muss nicht angelegt werden.

### 3. Klassen auswählen

Die Karte liest die verfügbaren Klassen aus den Daten des Vertretungsplan-Sensors. Mehrere Klassen können gleichzeitig über die anklickbaren Klassen-Chips ausgewählt werden.

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
- Die Lovelace-Karte wird automatisch mit der Integration bereitgestellt.
- Nach einem Update der Integration kann ein Neuladen des Browsers erforderlich sein, damit eine aktualisierte JavaScript-Karte geladen wird.
