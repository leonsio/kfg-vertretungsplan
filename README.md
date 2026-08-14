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

Die Lovelace-Karte ist Bestandteil der Integration. Nach der Installation wird die JavaScript-Datei automatisch aus der Integration bereitgestellt und von Home Assistant geladen. **Es ist kein Kopieren der Datei nach `/config/www` und keine manuelle Lovelace-Ressource erforderlich.**

## Dashboard erstellen

### 1. Dashboard anlegen

Öffne:

**Einstellungen → Dashboards → Dashboard hinzufügen**

und erstelle beispielsweise ein Dashboard mit dem Namen:

**Vertretungsplan**

### 2. Karte hinzufügen

Öffne das Dashboard und wähle:

**Karte hinzufügen → Manuell**

Die einfachste Konfiguration ist:

```yaml
type: custom:kfg-vertretungsplan-card
sensor: sensor.vertretungsplan
```

Speichere die Karte.

Nach der Installation der Integration sollte die Karte bereits als **KFG Vertretungsplan** verfügbar sein. Eine zusätzliche JavaScript-Ressource muss nicht angelegt werden.

## Dashboard konfigurieren

Die Karte kann über YAML-Parameter an die gewünschte Darstellung angepasst werden.

### Alle Klassen interaktiv auswählen

Wenn kein `classes`-Parameter angegeben wird, zeigt die Karte die verfügbaren Klassen als anklickbare Auswahl an:

```yaml
type: custom:kfg-vertretungsplan-card
sensor: sensor.vertretungsplan
```

Über die Klassen-Chips können **eine oder mehrere Klassen gleichzeitig** ausgewählt werden. Mit **Alle Klassen** wird die Auswahl zurückgesetzt und wieder der vollständige Vertretungsplan angezeigt.

### Eine Klasse fest konfigurieren

Für ein Dashboard, das ausschließlich für eine bestimmte Klasse gedacht ist, kann die Klasse fest vorgegeben werden:

```yaml
type: custom:kfg-vertretungsplan-card
sensor: sensor.vertretungsplan
classes:
  - 5b2
```

Die interaktive Klassenauswahl wird bei einer festen Konfiguration nicht benötigt. Die Karte zeigt dann nur die Vertretungen für `5b2`.

### Mehrere Klassen fest konfigurieren

Es können auch mehrere Klassen fest hinterlegt werden:

```yaml
type: custom:kfg-vertretungsplan-card
sensor: sensor.vertretungsplan
classes:
  - 5b2
  - 7n
  - 9ac
```

In diesem Beispiel zeigt die Karte ausschließlich Vertretungen für `5b2`, `7n` und `9ac`.

### Konfigurationsparameter

| Parameter | Pflicht | Beschreibung | Beispiel |
|---|---|---|---|
| `type` | Ja | Name der Custom Card. | `custom:kfg-vertretungsplan-card` |
| `sensor` | Nein | Entity-ID des Vertretungsplan-Sensors. Standard ist `sensor.vertretungsplan`. | `sensor.vertretungsplan` |
| `classes` | Nein | Liste mit einer oder mehreren fest vorgegebenen Klassen. Wird der Parameter weggelassen, erscheint die interaktive Klassenauswahl. | `['5b2', '7n']` |

### Mehrere Karten für unterschiedliche Klassen

Es ist möglich, mehrere Karten auf einem Dashboard zu verwenden, beispielsweise eine Karte für jedes Kind bzw. jede Klasse:

```yaml
- type: custom:kfg-vertretungsplan-card
  sensor: sensor.vertretungsplan
  classes:
    - 5b2

- type: custom:kfg-vertretungsplan-card
  sensor: sensor.vertretungsplan
  classes:
    - 7n
```

Alternativ kann eine gemeinsame Karte für mehrere Klassen verwendet werden:

```yaml
- type: custom:kfg-vertretungsplan-card
  sensor: sensor.vertretungsplan
  classes:
    - 5b2
    - 7n
```

## Darstellung

Die Karte zeigt den Vertretungsplan ab dem aktuellen Tag und für die folgenden Schultage der aktuellen bzw. nächsten verfügbaren Kalenderwoche.

Die Vertretungen werden tabellarisch mit folgenden Informationen dargestellt:

- **Klasse**
- **Stunde**
- **Fach**
- **Lehrer**
- **Vertretung**
- **Raum**
- **Art**

Vorhandene Tagesnachrichten werden ebenfalls angezeigt. Der Wochentyp (**Woche A** bzw. **Woche B**) wird im jeweiligen Tagesbereich hervorgehoben.

Die Karte verwendet eine farbliche Kennzeichnung der verschiedenen Vertretungsarten, damit Änderungen wie Vertretung, Entfall oder Tausch schneller erkennbar sind.

Lehrerkürzel werden – soweit auf der Kollegiumsseite des Kaiserin-Friedrich-Gymnasiums vorhanden – durch den Namen ergänzt. Wenn für ein Kürzel kein Name gefunden wird, bleibt das Kürzel aus dem Vertretungsplan erhalten.

## Aktualisierung

Der Sensor wird von der Integration automatisch aktualisiert. Das Dashboard verwendet die aktuellen Daten des Sensors; eine manuelle Aktualisierung der Karte ist nicht erforderlich.

## Hinweise

- Für HACS muss das Repository als **Integration** hinzugefügt werden.
- Die Lovelace-Karte wird automatisch mit der Integration bereitgestellt.
- Die Klassenauswahl wird bei einer interaktiven Karte lokal im Browser gespeichert; sie benötigt keinen zusätzlichen Home-Assistant-Helper.
- Bei einer festen `classes`-Konfiguration wird die Anzeige durch die YAML-Konfiguration des Dashboards bestimmt.
- Nach einem Update der Integration kann ein Neuladen des Browsers erforderlich sein, damit eine aktualisierte JavaScript-Karte geladen wird.
