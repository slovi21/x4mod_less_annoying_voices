# Wie funktioniert die Boso-Ta-Mod? Eine Erklärung ohne Fachchinesisch

## Das Problem

In X4 gibt es den Boronen-Forscher Boso Ta. Er redet viel, und seine Stimme ist sehr hoch und piepsig. Wer ihn nervig findet, hat im Spiel selbst keine Möglichkeit, nur seine Stimme zu ändern. Es gibt nur einen Regler für alle Stimmen zusammen.

## Wie das Spiel Stimmen abspielt

Man kann sich das wie eine Bibliothek vorstellen:

- Jeder Satz, den eine Figur sagen kann, liegt als kleine Tondatei im Spiel. Für Boso Ta sind das auf Deutsch 2 324 Sätze.
- Dazu gibt es eine Art **Inhaltsverzeichnis**. Darin steht für jede Figur, in welchem Regal ihre Tondateien liegen, wie laut sie abgespielt werden und ob der Ton aus einer bestimmten Richtung im Raum kommen soll.
- Will das Spiel Boso Ta etwas sagen lassen, schlägt es im Verzeichnis nach, geht zum Regal, holt die passende Datei und spielt sie ab.

## Was die Mod macht

Die Mod verändert keine einzige Originaldatei des Spiels. Sie macht zwei Dinge:

1. **Sie legt ein eigenes Regal an.** Darin liegen Kopien von Boso Tas 2 324 Sätzen, die vorher durch ein Tonbearbeitungsprogramm gelaufen sind. Die Stimme wurde eine Oktave tiefer gemacht, ohne sie langsamer zu machen, bekam einen fremdartigen Klang und wurde so bearbeitet, dass man sie im Spiel gut versteht. Die Sätze sind exakt gleich lang wie vorher, deshalb passen Mundbewegung und Dialogablauf weiterhin.
2. **Sie hängt einen Zettel ins Inhaltsverzeichnis.** Darauf steht: „Boso Tas Sätze bitte nicht aus dem Originalregal holen, sondern aus dem neuen Regal der Mod." Außerdem steht darauf, dass seine Gespräche nicht mehr aus einer Richtung im Raum kommen sollen. Vorher wurde er leiser und undeutlich, sobald man ihm den Rücken zudrehte oder er hinter der Glasscheibe seines Tanks stand.

Mehr ist es nicht. Alle anderen Figuren, Geräusche und Musik bleiben, wie sie sind. Ein einziger weiterer Charakter, der Boronen-Vertreter, spricht mit demselben Sprecher wie Boso Ta und bekommt deshalb ebenfalls die neue Stimme.

## Warum die Mod nicht einfach eine Datei zum Herunterladen ist

Die bearbeiteten Tondateien sind Kopien von Egosofts Originalen. Deshalb liegen sie nicht im öffentlichen Projektordner im Internet. Stattdessen enthält das Projekt das „Rezept": Ein kleines Programm holt die Originale aus der eigenen Spielinstallation, bearbeitet sie nach dem festgelegten Rezept und legt sie in das Regal der Mod. Das dauert etwa zehn Minuten und passiert auf dem eigenen Rechner. Wer die Mod fertig als Download bekommt, braucht davon nichts; dann liegen die fertigen Dateien schon bei.

## Was „modifiziert" bedeutet

Egosoft versieht alle eigenen Spieldateien mit einer Art Echtheitssiegel. Sobald das Spiel eine Datei lädt, die dieses Siegel nicht hat, zum Beispiel den Zettel dieser Mod, schaltet es in den Modus „modifiziert". Das hat drei Folgen:

- Steam-Erfolge werden in diesem Spielstand nicht mehr vergeben.
- Die Online-Funktion „Ventures" ist abgeschaltet.
- Der Spielstand behält den Vermerk „modifiziert" dauerhaft, auch wenn man die Mod später wieder entfernt.

Das gilt für jede Mod, auch für solche aus dem Steam Workshop. Es gibt keinen Weg, eine Mod zu bauen, die dieses Siegel hat. Wer Erfolge sammeln will, muss ohne Mods spielen.

## Was passiert, wenn man die Mod wieder entfernt

Man löscht den Ordner der Mod aus dem Spielordner. Das Spiel findet den Zettel nicht mehr und holt Boso Tas Sätze wieder aus dem Originalregal. Die Spielstände funktionieren weiter, behalten aber den Vermerk „modifiziert".

## Kurzfassung

| Frage | Antwort |
|---|---|
| Was wird geändert? | Nur, woher das Spiel Boso Tas Stimme holt, und wie sie im Raum abgespielt wird. |
| Werden Originaldateien verändert? | Nein. |
| Betrifft es andere Figuren? | Nur den Boronen-Vertreter, der denselben Sprecher hat. |
| Braucht man etwas dazu? | Zum Selbstbauen: Python und das Tonprogramm ffmpeg. Als fertiger Download: nichts. |
| Gilt das Spiel als modifiziert? | Ja, wie mit jeder Mod. Keine Steam-Erfolge, keine Ventures. |
| Rückgängig machen? | Ordner löschen. |
