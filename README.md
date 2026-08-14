# KFG Vertretungsplan

Home-Assistant-Custom-Integration für den schulweiten Untis-Vertretungsplan des Kaiserin-Friedrich-Gymnasiums.

Die Integration ruft die schulweite `w00000.htm` für die aktuelle und nächste ISO-Kalenderwoche ab und stellt die Daten als Sensorattribute bereit.

## Installation über HACS

1. HACS → Integrationen → Benutzerdefinierte Repositories.
2. `https://github.com/leonsio/kfg-vertretungsplan` hinzufügen.
3. Kategorie **Integration** wählen und installieren.
4. Home Assistant neu starten.
5. Einstellungen → Geräte & Dienste → Integration hinzufügen → **KFG Vertretungsplan**.

Die Lovelace-Karte liegt unter `frontend/vertretungsplan-card.js` und kann als Ressource eingebunden werden.
