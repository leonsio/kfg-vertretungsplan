# Installation und Dashboard

## 1. Integration über HACS installieren

1. In Home Assistant **HACS → Integrationen** öffnen.
2. Oben rechts **⋮ → Benutzerdefinierte Repositories** wählen.
3. Als Repository eintragen:

   `https://github.com/leonsio/kfg-vertretungsplan`

4. Als Kategorie **Integration** auswählen.
5. **Hinzufügen** und anschließend **KFG Vertretungsplan** installieren.
6. Home Assistant neu starten.
7. **Einstellungen → Geräte & Dienste → Integration hinzufügen** öffnen und **KFG Vertretungsplan** auswählen.
8. Den Einrichtungsdialog abschließen.

## 2. Dashboard erstellen

1. **Einstellungen → Dashboards → Dashboard hinzufügen** öffnen.
2. Ein Dashboard, z. B. **Vertretungsplan**, erstellen.
3. Das neue Dashboard öffnen.
4. **Karte hinzufügen → Manuell** auswählen.
5. Folgende YAML-Konfiguration einfügen:

```yaml
type: custom:kfg-vertretungsplan-card
sensor: sensor.vertretungsplan
selected_entity: input_text.vertretungsplan_klassen
```

6. Karte speichern.

### Keine manuelle JavaScript-Installation erforderlich

Die Karte ist Bestandteil der HACS-Integration. Beim Laden der Integration wird sie automatisch über den Home-Assistant-HTTP-Server bereitgestellt und als zusätzliches Frontend-JavaScript geladen. Es muss daher weder eine Datei nach `/config/www` kopiert noch eine Lovelace-Ressource manuell angelegt werden.

### Klassen auswählen

Die Karte zeigt die vom Vertretungsplan erkannten Klassen als anklickbare Chips. Mehrere Klassen können gleichzeitig ausgewählt werden. Ohne Auswahl werden Vertretungen für alle Klassen angezeigt.
