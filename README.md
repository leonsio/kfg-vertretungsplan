# KFG Vertretungsplan

Home-Assistant-Custom-Integration für den Untis-Vertretungsplan des Kaiserin-Friedrich-Gymnasiums.

Die Integration ruft die schulweite `w00000.htm` für die aktuelle und nächste ISO-Kalenderwoche ab. Pro konfigurierter Klasse werden eigene Sensoren erzeugt; der Kollegium-Sensor wird systemweit nur einmal angelegt.

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
11. Gib die gewünschte Klasse, die Basis-URL und das Aktualisierungsintervall an.

Für weitere Klassen kann **KFG Vertretungsplan mehrfach hinzugefügt** werden. Eine Klasse kann dabei nur einmal konfiguriert werden.

Die Lovelace-Karte ist Bestandteil der Integration. Die JavaScript-Datei wird automatisch bereitgestellt. Es ist kein Kopieren nach `/config/www` und keine manuelle Lovelace-Ressource erforderlich.

## Sensoren pro Klasse

Für die Klasse `7n` entstehen beispielsweise:

```text
sensor.vertretungsplan_7n
sensor.vertretungsplan_7n_json
```

Für `5b2` entsprechend:

```text
sensor.vertretungsplan_5b2
sensor.vertretungsplan_5b2_json
```

### Vertretungsplan-Sensor

`sensor.vertretungsplan_7n` enthält ausschließlich Vertretungseinträge, die zur Klasse `7n` gehören. Auch Einträge mit mehreren Klassen wie `(7n, 7b1)` werden berücksichtigt.

Die Struktur enthält weiterhin unter anderem:

- `generated`
- `today`
- `current_week`
- `next_week`
- `next_week_available`
- `class`
- `classes`
- `weeks`
- Tagesnachrichten (`news`)
- gefilterte Vertretungen (`entries`)

### JSON-Sensor

`sensor.vertretungsplan_7n_json` stellt dieselben klassenbezogenen Daten als kompaktes JSON bereit.

Da ein Home-Assistant-Sensorzustand nur eine begrenzte Textlänge unterstützt, liegt der vollständige JSON-Inhalt im Attribut:

```text
json
```

Der eigentliche Sensorzustand enthält den Zeitpunkt der Datengenerierung.

## Kollegium

Unabhängig von der Anzahl konfigurierter Klassen wird nur einmal erzeugt:

```text
sensor.kfg_kollegium
```

Der Sensor enthält im Attribut `lehrer` die Zuordnung der Lehrerkürzel zu den Namen. Die Daten stammen von der offiziellen Kollegiumsseite des KFG und werden regelmäßig aktualisiert.

## Klasse oder Aktualisierungsintervall nachträglich ändern

Öffne:

**Einstellungen → Geräte & Dienste → KFG Vertretungsplan → Zahnrad / Konfigurieren**

Dort können geändert werden:

- **Klasse**
- **Aktualisierungsintervall**

Bei einer Klassenänderung werden die zugehörigen Sensoren entsprechend umbenannt. Aus beispielsweise

```text
sensor.vertretungsplan_7n
sensor.vertretungsplan_7n_json
```

wird bei Änderung auf `8b1`:

```text
sensor.vertretungsplan_8b1
sensor.vertretungsplan_8b1_json
```

## Dashboard erstellen

Öffne das gewünschte Dashboard und wähle:

**Karte hinzufügen → Manuell**

Für Klasse `7n`:

```yaml
type: custom:kfg-vertretungsplan-card
sensor: sensor.vertretungsplan_7n
```

Da der Sensor bereits nur Daten für `7n` enthält, ist ein zusätzlicher `classes:`-Filter normalerweise nicht erforderlich.

Für eine weitere Klasse kann eine zweite Karte verwendet werden:

```yaml
- type: custom:kfg-vertretungsplan-card
  sensor: sensor.vertretungsplan_7n

- type: custom:kfg-vertretungsplan-card
  sensor: sensor.vertretungsplan_5b2
```

### Konfigurationsparameter der Karte

| Parameter | Pflicht | Beschreibung | Beispiel |
|---|---|---|---|
| `type` | Ja | Name der Custom Card. | `custom:kfg-vertretungsplan-card` |
| `sensor` | Ja empfohlen | Entity-ID des klassenbezogenen Vertretungsplan-Sensors. | `sensor.vertretungsplan_7n` |
| `teacher_sensor` | Nein | Sensor mit Lehrerkürzeln und Namen. Standard ist `sensor.kfg_kollegium`. | `sensor.kfg_kollegium` |
| `classes` | Nein | Zusätzlicher Frontend-Filter. Bei einem bereits klassenbezogenen Sensor normalerweise nicht erforderlich. | `['7n']` |

## Darstellung

Die Karte zeigt den Vertretungsplan ab dem aktuellen Tag und für die folgenden Schultage der aktuellen bzw. nächsten verfügbaren Kalenderwoche.

Die Vertretungen werden tabellarisch dargestellt mit:

- **Klasse** – entfällt bei einer einzelnen fest konfigurierten Klasse
- **Stunde**
- **Fach**
- **Lehrer**
- **Vertretung**
- **Raum**
- **Art**

Vorhandene Tagesnachrichten werden ebenfalls angezeigt. Der Wochentyp (**Woche A** bzw. **Woche B**) wird hervorgehoben.

Lehrerkürzel werden über `sensor.kfg_kollegium` aufgelöst. Fehlt ein Kürzel dort, wird das Originalkürzel des Vertretungsplans angezeigt.

## Aktualisierung

Jeder Klassen-Eintrag besitzt ein eigenes einstellbares Aktualisierungsintervall. Es kann nachträglich über das Zahnrad des jeweiligen Integrationseintrags geändert werden.

## Hinweise

- Für HACS muss das Repository als **Integration** hinzugefügt werden.
- Die Lovelace-Karte wird automatisch als Ressource bereitgestellt.
- Mehrere Klassen werden als mehrere Integrationseinträge angelegt.
- `sensor.kfg_kollegium` wird nur einmal erstellt.
- Nach einem Update kann ein vollständiges Neuladen des Browsers erforderlich sein, damit eine neue JavaScript-Version der Karte verwendet wird.
