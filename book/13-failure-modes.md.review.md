# Review: 13-failure-modes.md

## Durchgang 1 – 2026-10-25 17:47
- Dokument: C:\#repos\github\x4mod_less_annoying_voices\book\13-failure-modes.md
- Anlass: neu

### Stufe 1 – Befunde
#### Prüfer A – fachliche Richtigkeit
Fachgebiet: X4-Foundations-Modding (Sprachausgabe-Austausch per XML-Diff, Audio-/TTS-Pipeline mit ffmpeg, ElevenLabs-API und Steam Workshop) · Zielgruppe: Entwickler und Betreiber des Mods mit Python- und Kommandozeilenkenntnissen (abgeleitet)
**A1** · Abschnitt „In the game“, Zeile „Boso sounds unchanged“ (Spalte Detect: „-logfile debuglog.txt“ und „No matching node“) · unklar · mittel
Befund: Ich konnte nicht verifizieren, dass X4 bei fehlgeschlagenen Diff-Selektoren genau die Meldung „No matching node“ ins Log schreibt. Ich konnte auch nicht belegen, dass `-logfile debuglog.txt` allein genügt. Häufig wird dafür zusätzlich `-debug all` genannt. Eine zu enge Suchanweisung führt dazu, dass ein Fehler im Log übersehen wird.
Vorschlag: Den exakten Wortlaut der Diff-Fehlermeldung und die tatsächlich nötigen Startparameter (`-debug all`, `-logfile`) an einem echten Log prüfen und die Zeile entsprechend korrigieren oder die Meldung als Beispiel kennzeichnen.
Status: offen – Ersteller – exakter Wortlaut der X4-Diff-Fehlermeldung und nötige Startparameter (`-debug all`?) sind nur an einem echten Log prüfbar

**A2** · Abschnitt „In the game“, Zeile „Brief red text on screen“ (Cause: „shown when `-logfile` is active“) · unklar · gering
Befund: Ich konnte nicht verifizieren, dass die roten Bildschirmmeldungen durch `-logfile` ausgelöst werden. Üblicherweise hängt das Einblenden von Skriptfehlern am Debug-Modus (`-debug`). `-logfile` steuert nur die Ausgabe in eine Datei. Die Ursache könnte falsch zugeordnet sein, und die Fix-Anweisung „remove `-logfile`“ würde dann nicht helfen.
Vorschlag: Prüfen, welcher Startparameter die Einblendung auslöst, und Ursache und Fix entsprechend anpassen (z. B. „remove `-debug all`“).
Status: offen – Ersteller – nicht belegbar, welcher Startparameter (`-logfile` oder `-debug`) die roten Bildschirmmeldungen auslöst

**A3** · Abschnitt „In the game“, Zeile „Save marked ‚modified‘“ (Cause: „any unsigned extension“, Fix: „unavoidable for mods“) · unklar · gering
Befund: Ich konnte nicht verifizieren, dass das Flag „modified“ in X4 am Fehlen einer Signatur hängt und nicht jede aktive Extension betrifft. Ebenso wenig konnte ich klären, ob das `save`-Attribut in `content.xml` (in Beispielen als `save="0"` zu sehen) die Markierung für reine Audio-Mods vermeiden kann. „Unavoidable“ ist daher möglicherweise zu pauschal.
Vorschlag: Das Verhalten prüfen (Extension mit gesetztem und ungesetztem `save`-Attribut testen) und die Aussage entsprechend präzisieren, z. B. „any active extension“ oder den Hinweis auf das `save`-Attribut ergänzen.
Status: offen – Ersteller – Verhalten des „modified“-Flags und Wirkung des `save`-Attributs müssen im Spiel getestet werden

**A4** · Abschnitt „In the game“, Zeile „Boso ‚too quiet‘ although measurements match“ („dark voices lose 1–4 kHz energy“) · unklar · gering
Befund: Die Behauptung, dunkle Stimmen verlören im Spielmix Energie im Bereich 1–4 kHz, ist eine Faustregel ohne Beleg im Dokument. Ich konnte sie nicht verifizieren. „Equal LUFS ≠ equal perceived loudness“ ist als Prinzip korrekt, die Frequenzangabe aber nicht belegt.
Vorschlag: Die Angabe als Beobachtung oder Hypothese kennzeichnen oder auf eine Messung im Projekt verweisen (z. B. LESSONS.md).
Status: offen – Ersteller – ob die 1–4-kHz-Angabe eine Messung/Beobachtung des Projekts ist, steht nicht im Dokument

**A5** · Abschnitt „In the pipeline“, Zeilen „`tts-batch`: HTTP 402“ und „`quota`: HTTP 401“ · unklar · gering
Befund: Die Zuordnung von HTTP 402 zu „library voice on a free plan“ und von HTTP 401 zu „key without user-read permission“ konnte ich nicht per Primärquelle bestätigen. Plausibel ist sie: ElevenLabs meldet Library-Voices für Free-Nutzer als nicht verfügbar, und ein fehlendes Scope-Recht führt zu 401. Die Zeile „many lines fail fast“ nennt zudem „credits exhausted“ als 4xx-Fall ohne den konkreten Code, was Leser mit 402/401 verwechseln können.
Vorschlag: Die Zuordnung an der aktuellen ElevenLabs-API-Dokumentation prüfen und bei den Zeilen den genauen Fehlercode (z. B. `payment_required`, `missing_permissions`, `quota_exceeded`) ergänzen.
Status: offen – Ersteller – Zuordnung der HTTP-Codes und genaue API-Fehlercodes des TTS-Anbieters sind aus dem Dokument nicht belegbar

**A6** · Abschnitt „In the pipeline“, Zeile „First command extracts 0 files“ („the lines are in `03.cat`, not `01.cat`“) · unklar · gering
Befund: Die Katalogzuordnung der Voice-Dateien (`03.cat`) konnte ich nicht verifizieren. Sie hängt vom Spielstand ab, Patches und DLCs können Dateien in andere Kataloge legen. Zudem ist „First command“ ohne Kontext unklar: Es ist nicht erkennbar, welcher Befehl gemeint ist.
Vorschlag: Den Befehl nennen und die Katalognummer als „Stand Spielversion X“ kennzeichnen oder allgemein formulieren („prüfe die Kataloge per `Select-String`“).
Status: offen – Ersteller – Name des gemeinten Extraktionsbefehls und Gültigkeit der Katalognummer `03.cat` (Spielversion) fehlen

**A7** · Abschnitt „In the pipeline“, Zeilen „Workshop upload error 16“ und „Workshop update error 9“ · unklar · gering
Befund: Die Fehlercodes 16 und 9 samt Ursachen (Timeout bei großem Payload, `-preview` bei erstem Update) konnte ich nicht verifizieren. Das Dokument nennt auch nicht, welches Werkzeug sie meldet (z. B. Egosofts WorkshopTool).
Vorschlag: Das ausgebende Werkzeug und seine Version nennen und die Codes gegen dessen Ausgabe oder Dokumentation prüfen.
Status: offen – Ersteller – das Workshop-Werkzeug (und seine Version), das die Fehlercodes 16 und 9 meldet, ist nicht genannt

**A8** · Abschnitt „In the pipeline“, Zeile „`python` ‚Permission denied‘“ (Cause: „broken Windows Store alias“) · unklar · gering
Befund: Beim App-Execution-Alias von Windows lautet die typische Meldung „Python was not found“ oder es öffnet sich der Store. „Permission denied“ tritt je nach Shell (z. B. Git Bash) ebenfalls auf. Ich konnte nicht prüfen, ob die Ursache hier immer der Alias ist.
Vorschlag: Die Shell nennen, in der die Meldung auftritt, und den Fix konkretisieren (App-Ausführungsalias für python.exe in den Windows-Einstellungen deaktivieren oder den echten Interpreter per Pfad aufrufen).
Status: behoben – Fix konkretisiert: „call the real interpreter“ → „call the real `python.exe` by its full path, or disable the Python entries under App execution aliases in the Windows settings“, Ursache um „the `python` stub in `WindowsApps`“ ergänzt; die Shell, in der die Meldung auftritt, ist nicht bekannt und nicht ergänzt

**A9** · Abschnitt „Edge cases in the data“, Punkt „German-only ids“ („574 ids exist only in the German track“) · unklar · gering
Befund: Die Zahl 574 ist im Dokument nicht belegt und von mir nicht prüfbar. Sie ist spiel- und patchabhängig und kann nach einem Update veralten. Außerdem steht „the English game never requests them“ als Tatsache da, obwohl es nur für die geprüfte Spielversion gilt.
Vorschlag: Die Zahl mit Stand (Spielversion, Datum) versehen oder durch einen Verweis auf das Tool ersetzen, das sie ermittelt (z. B. `check_coverage.py`).
Status: offen – Ersteller – Stand (Spielversion, Datum) der Zahl 574 und ihre Quelle fehlen

**A10** · Abschnitt „In the game“, Zeile „Comm messages lack the radio filter“ („all six entries read the processed `normal` set“) · unklar · gering
Befund: „All six entries“ ist im Kapitel nicht erklärt. Es ist unklar, welche sechs Einträge gemeint sind und wo sie definiert sind. Die Aussage lässt sich anhand dieses Dokuments nicht prüfen.
Vorschlag: Die sechs Einträge benennen oder auf das Kapitel verweisen, in dem sie beschrieben sind.
Status: offen – Ersteller – welche sechs Einträge gemeint sind, steht nicht im Dokument

#### Prüfer B – Logik und Zahlen
Fachgebiet: Softwaredokumentation, Fehlerdiagnose und Betrieb einer X4-Foundations-Voice-Mod mit Audio-Pipeline (TTS, ffmpeg, Steam Workshop) · Zielgruppe: Mod-Betreiber und Maintainer mit technischem Grundwissen, die die Mod bauen, installieren und pflegen (abgeleitet)

**B1** · Tabelle „In the game“, Zeile „Single lines silent“ („or the 5 textless ids missing“ / „generate the missing ids“) · Logikfehler · mittel
Befund: Als Ursache werden die „5 textless ids“ genannt, als Fix „generate the missing ids“. Laut Abschnitt „Edge cases in the data“ haben diese fünf IDs keinen Text und behalten in der Will-Variante das aufbereitete Originalaudio. Sie lassen sich also nicht per TTS erzeugen, und sie sind in der Will-Variante nicht „missing“. Ursache und Fix passen nicht zusammen, und der Leser erfährt nicht, wie der Fall „fehlen sie doch“ zu beheben ist.
Vorschlag: Den Fall getrennt behandeln: für die fünf textlosen IDs als Fix das Kopieren des aufbereiteten Originalaudios angeben (oder auf den Abschnitt „Edge cases“ verweisen). „Generate the missing ids“ nur für IDs mit Text verwenden.
Status: behoben – Fix der Zeile „Single lines silent“ ergänzt: „the 5 textless ids cannot be generated, they keep the processed original audio (see „Edge cases in the data“)“

**B2** · Tabelle „In the pipeline“, Zeile 1 („fixed: audio is always copied and checked before copying“) zusammen mit Zeile 2 („removal of `bosota_*` happens before the audio check“) · Logikfehler · mittel
Befund: Zeile 1 sagt, das Audio werde vor dem Kopieren geprüft. Zeile 2 beschreibt als bekannten Fehler, dass die Prüfung erst nach dem Entfernen der alten Variante läuft. Ob die Reihenfolge „prüfen, dann entfernen“ gilt oder nicht, bleibt unklar. Zeile 2 ist als offener Fehler geführt, Zeile 1 als behoben. Der Satz „copied and checked before copying“ ist außerdem in sich redundant.
Vorschlag: Die Reihenfolge eindeutig festlegen, etwa „Audio wird immer kopiert; die Prüfung läuft nach dem Entfernen von `bosota_*`“. In Zeile 2 zusätzlich vermerken, ob das ein offener Fehler oder ein akzeptiertes Verhalten ist.
Status: behoben – Zeile 1: Fix umformuliert (redundantes „checked before copying“ entfernt, „fixed in the installer from 2026-10-24 on … audio is now always copied, and checked first“); Zeile 2: Reihenfolge ergänzt „(order: remove, check audio, copy)“; ob das ein offener Fehler oder akzeptiertes Verhalten ist, steht nicht im Dokument und wurde nicht ergänzt

**B3** · Tabelle „In the pipeline“, Zeile „First command extracts 0 files“ · Logikfehler · mittel
Befund: „First command“ hat keinen Bezug. Das Dokument benennt nicht, welcher Befehl gemeint ist (vermutlich der Extraktionsschritt der Pipeline), und die Zeile ist ohne diesen Bezug nicht auffindbar oder zuordenbar. Das Muster ist auch uneinheitlich: Alle anderen Zeilen nennen das betroffene Skript oder den Befehl.
Vorschlag: Den Befehl oder das Skript namentlich nennen, z. B. „`<extract command>`: extracts 0 files“, oder auf das Kapitel verweisen, in dem der Schritt beschrieben ist.
Status: offen – Ersteller – Name des Befehls/Skripts, das „0 files“ extrahiert, fehlt

**B4** · Einleitung („how it is detected and fixed“) im Vergleich zur Tabelle „In the pipeline“ (Spalten „Symptom | Cause | Fix“) · Logikfehler · gering
Befund: Die Einleitung verspricht für jeden Fehler Symptom, Ursache, Erkennung und Behebung. Die Tabelle „In the game“ hat eine Spalte „Detect“, die Pipeline-Tabelle nicht. Die Erkennung ist dort nur teilweise im Symptom enthalten. In der Spiel-Tabelle steht bei mehreren Zeilen „—“, ohne dass erklärt wird, was das bedeutet (keine Erkennung nötig oder keine möglich).
Vorschlag: Entweder eine Detect-Spalte in die Pipeline-Tabelle aufnehmen oder die Einleitung anpassen. Zusätzlich in einem Satz erläutern, was „—“ in der Detect-Spalte bedeutet.
Status: behoben – Einleitung auf „how it is fixed; for in-game failures also how it is detected“ angepasst; unter der Spiel-Tabelle Satz ergänzt, dass „—“ in Detect bedeutet: keine Log- oder Werkzeugprüfung, das Symptom selbst ist das Signal

**B5** · Tabelle „In the game“, Zeile „Comm messages lack the radio filter“ („all six entries read the processed `normal` set“) · unklar · gering
Befund: „All six entries“ hat keinen Bezug. Das Dokument erklärt weder, welche sechs Einträge gemeint sind, noch ob sie mit dem Verzeichnis `voice/10201/normal/` oder `10201_comm_*` zusammenhängen. Die Zahl lässt sich im Dokument nicht gegenprüfen.
Vorschlag: Die sechs Einträge benennen oder auf das Kapitel mit der Diff-Struktur verweisen, z. B. „all six `10201_comm_*` entries“.
Status: offen – Ersteller – welche sechs Einträge gemeint sind (und ob es `10201_comm_*` sind), steht nicht im Dokument

**B6** · Tabelle „In the pipeline“, Zeile „`tts-batch` ends with a traceback after all lines ran“ („queued lines still run and are billed“) · Logikfehler · gering
Befund: Im Symptom steht „after all lines ran“, in der Ursache „queued lines still run and are billed“. Wenn alle Zeilen gelaufen sind, gibt es keine wartenden Zeilen mehr. Die beiden Angaben beschreiben unterschiedliche Zeitpunkte, die Reihenfolge der Ereignisse (Ausnahme zuerst oder Lauf zuerst) bleibt unklar. Der Hinweis „finished WAVs are skipped“ löst den Widerspruch nicht auf.
Vorschlag: Das Symptom präzisieren, z. B. „traceback at the end of the run although all lines were generated“, und in der Ursache sagen, dass die Ausnahme erst beim Einsammeln der Ergebnisse auftritt und die übrigen Aufträge trotzdem weiterlaufen.
Status: behoben – Symptom „after all lines ran“ → „although all lines were generated“; Ursache präzisiert: Ausnahme wird bei `fut.result()` beim Einsammeln der Ergebnisse erneut ausgelöst, die übrigen Zeilen laufen weiter

**B7** · Tabelle „In the pipeline“, Zeilen „Workshop upload error 16“ und „Workshop update error 9“ · unklar · gering
Befund: Die Fehlercodes 16 und 9 sind keinem Werkzeug zugeordnet (Steam-Workshop-Uploader, Skript?). Ob die Zuordnung von Code zu Ursache stimmt, ließ sich aus dem Dokument nicht ableiten. Ich konnte sie nicht verifizieren. Auch ist unklar, was „create with XML only, then `update`“ als Befehlsfolge heißt.
Vorschlag: Das Upload-Werkzeug nennen und die Befehlsfolge angeben (oder auf Kapitel 8 verweisen). Die Fehlercodes mit der Werkzeugdokumentation abgleichen.
Status: offen – Ersteller – Upload-Werkzeug, Befehlsfolge und Abgleich der Fehlercodes 16/9 fehlen

**B8** · Tabelle „In the pipeline“, Zeile „`tts-batch`: many lines fail fast“ im Vergleich zu den Zeilen „`tts-batch`: HTTP 402“ und „`quota`: HTTP 401“ · Logikfehler · gering
Befund: Die Zeile „4xx other than 429 (invalid key, credits exhausted)“ überschneidet sich mit den Einzelzeilen zu 401 und 402, ohne darauf zu verweisen. 402 ist als „library voice on a free plan“ erklärt, in der Sammelzeile aber als „credits exhausted“ geführt. Ein Leser mit HTTP 402 findet zwei Zeilen mit unterschiedlicher Ursache und Behebung.
Vorschlag: Die Sammelzeile auf die übrigen Codes eingrenzen oder die Abgrenzung zu 401/402 ausdrücklich nennen, z. B. „credits exhausted also appears as 402; check the account first“.
Status: behoben – Sammelzeile „many lines fail fast“ ergänzt um „this includes the 401/402 cases above“, damit die Abgrenzung zu den Einzelzeilen erkennbar ist

#### Prüfer C – Verständlichkeit
Fachgebiet: Betrieb und Fehlersuche eines X4-Foundations-Voice-Mods (Extension mit Diff-Patch, Audio-Pipeline mit ffmpeg, TTS-Batch, Steam-Workshop-Upload; Python-Skripte unter Windows) · Zielgruppe: Mod-Betreiber und Maintainer, die die vorherigen Kapitel des Handbuchs kennen und Skripte auf der Kommandozeile ausführen (abgeleitet)

**C1** · Kopfzeile, Zitat „(failure, operations)“ · unverständlich · gering
Befund: Die Klammer „(failure, operations)“ am Ende des Einleitungssatzes ist ohne Kontext nicht nachvollziehbar. Vermutlich ist ein Themen-Tag gemeint. Außerdem verspricht der Satz Symptom, Ursache, Erkennung und Behebung. Die Pipeline-Tabelle hat aber keine Spalte „Detect“.
Vorschlag: Die Klammer streichen oder erklären. Den Satz auf das einschränken, was die Tabellen tatsächlich liefern, oder der Pipeline-Tabelle eine Spalte „Detect“ geben.
Status: offen – Ersteller – Bedeutung des Tags „(failure, operations)“ ist nicht dokumentiert (Streichen oder Erklären hängt von der Absicht ab); der Detect-Teil ist durch B4 erledigt

**C2** · Tabelle „In the game“, Zeile 1 („diff not applied: wrong sound id … ‚No matching node‘“) · unverständlich · mittel
Befund: „diff“, „sound id“ und „the mod id“ werden nicht erklärt, und es steht nicht da, wo sie stehen. Die Spalte „Fix“ („correct the id; enable in Extensions menu“) deckt nur zwei der drei genannten Ursachen ab. Für ein fehlerhaftes `content.xml` fehlt die Behebung. Unklar ist auch, welche Id korrigiert werden soll und wo.
Vorschlag: Je Ursache eine eigene Behebung nennen, zum Beispiel „sound id in der Diff-Datei <Datei> korrigieren“. Die Begriffe einmal erklären oder auf das Kapitel verweisen, in dem sie eingeführt werden.
Status: offen – Ersteller – Fix für `content.xml` ergänzt („rebuild with `build_mod.py`“); Definition von diff/sound id/mod id und das zuständige Kapitel sind nicht bekannt

**C3** · Tabelle „In the game“, Zeile 3 („Boso completely silent“) · unklar · hoch
Befund: Mehrere Ursachen sind für einen Leser nicht eindeutig. „redirect“ ist undefiniert. „folder name ≠ `id`“ lässt offen, welche Id gemeint ist. „Workshop build with a non-`ws_` id“ wird nicht erklärt. Die Fix-Spalte „use the Workshop variant for Workshop uploads“ passt nicht zu allen Ursachen. Unklar bleibt, welche Ursache zu welchem Fix gehört und wie viele Dateien der Ordner `voice/10201/normal/` enthalten soll.
Vorschlag: Die Ursachen in einzelne Zeilen aufteilen, jeweils mit eigenem Fix. Den Sollwert der Dateianzahl nennen. „redirect“ und „`id`“ kurz definieren („Ordnername der Extension in `content.xml`“).
Status: offen – Ersteller – Definition von „redirect“, Sollwert der Dateianzahl in `voice/10201/normal/` und die Zuordnung Ursache → Fix sind aus dem Dokument nicht ableitbar

**C4** · Tabelle „In the game“, Zeile 4 („the 5 textless ids missing“, „generate the missing ids“) · unverständlich · mittel
Befund: „5 textless ids“ wird erst im Abschnitt „Edge cases in the data“ erklärt, ohne Verweis. „generate the missing ids“ nennt weder das Werkzeug noch den Befehl. Für die fünf textlosen Ids ist Generieren zudem nicht möglich, denn sie sind laut Edge-Cases „processed original audio“. Das widerspricht dem Fix.
Vorschlag: Auf den Abschnitt „Edge cases in the data“ verweisen. Den Fix konkretisieren, zum Beispiel „`process_audio.py`/`tts-batch` für die von `check_coverage.py` gemeldeten Ids ausführen“, und die textlosen Ids davon ausnehmen.
Status: behoben – Verweis auf „Edge cases in the data“ ergänzt und die textlosen Ids vom Generieren ausgenommen (siehe B1); ein konkreter Befehl wurde nicht ergänzt, da das Dokument das erzeugende Werkzeug nicht benennt

**C5** · Tabelle „In the game“, Zeile 6 („`is3d="0"`, `noocclusion="true"` (already in all variants)“) · unklar · mittel
Befund: Die Fix-Spalte nennt Attribute, die laut Text schon in allen Varianten gesetzt sind. Der Leser erfährt nicht, was er tun soll, wenn das Symptom trotzdem auftritt. Was „occlusion“ und „3d“ bedeuten, wird nicht erklärt. Die Detect-Spalte ist „—“.
Vorschlag: Klarstellen, dass hier nichts zu tun ist, wenn die Attribute vorhanden sind. Wenn das Symptom trotzdem auftritt, den nächsten Schritt nennen, zum Beispiel die Attribute in der Diff-Datei prüfen oder auf die Zeile „too quiet“ ausweichen. Die Begriffe kurz erläutern.
Status: behoben – Fix präzisiert: Attribute kurz erläutert („no positional audio“, „no muffling by obstacles“), „already set in all variants, so nothing to change; if it persists, see the next row“

**C6** · Tabelle „In the game“, Zeile 7 („equal LUFS ≠ equal perceived loudness … `--gain-db`, mid-range focus“) · unverständlich · mittel
Befund: „LUFS“ und „mid-range focus“ werden nicht erklärt. „`--gain-db`“ erscheint ohne Angabe, zu welchem Skript es gehört, in welchem Bereich der Wert liegen soll und ob er erhöht oder gesenkt wird. „mid-range focus“ ist als Maßnahme nicht ausführbar.
Vorschlag: Skript und Beispielaufruf nennen, etwa „`process_audio.py --gain-db +3`“, mit sinnvollem Wertebereich. „mid-range focus“ durch eine konkrete Einstellung ersetzen oder auf das Kapitel zur Audioverarbeitung verweisen. LUFS einmal erklären.
Status: offen – Ersteller – Skript, Wertebereich/Richtung von `--gain-db` und die konkrete Maßnahme hinter „mid-range focus“ fehlen

**C7** · Tabelle „In the game“, Zeile 9 („all six entries read the processed `normal` set“) · unklar · mittel
Befund: „all six entries“, „`normal` set“ und „comm set“ sind unbestimmt. Der Leser weiß nicht, welche sechs Einträge gemeint sind. Er weiß auch nicht, was der Unterschied zwischen `normal` und einem Comm-Set ist und was „radio filter“ konkret bedeutet.
Vorschlag: Die sechs Einträge benennen oder auf die Stelle verweisen, wo sie aufgeführt sind. Außerdem kurz sagen, welcher Audioordner den Funkfilter enthält.
Status: offen – Ersteller – welche sechs Einträge gemeint sind und welcher Audioordner den Funkfilter enthält, steht nicht im Dokument

**C8** · Tabelle „In the game“, Zeile 12 („subscribed Workshop item `ws_*` … `bosota_*`“) · unklar · gering
Befund: Die Präfixe `ws_*` und `bosota_*` werden hier ohne Erklärung benutzt. Der Fix „unsubscribe or remove the local build“ nennt nicht, woran man erkennt, welche Variante aktiv ist. „the installer does not see `ws_*`“ lässt offen, welche Folge das hat.
Vorschlag: Einen Halbsatz ergänzen, zum Beispiel „`bosota_*` = lokaler Build, `ws_<n>` = Workshop-Abo“. Zusätzlich die Folge nennen („der Installer entfernt `ws_*` nicht“).
Status: behoben – Fix ergänzt „(and so does not remove)“ zu `ws_*`; unter der Tabelle Satz ergänzt, dass `bosota_*` ein lokaler Build und `ws_*` ein abonniertes Workshop-Item ist

**C9** · Tabelle „In the pipeline“, Zeile 1 („the pre-2026-10-24 installer … `kind == "audio"`, a field removed in the clean-up“) · unverständlich · mittel
Befund: Der Eintrag beschreibt einen bereits behobenen Entwickler-Fehler in interner Code-Sprache („`kind == "audio"`“, „clean-up“). Ein Leser kann daraus nicht ableiten, ob und wann er betroffen ist und was er tun soll. Der Fix „fixed“ ist keine Handlungsanweisung. Die Begriffe „clean-up“ und „field“ sind unbestimmt.
Vorschlag: Als Fehler der älteren Version kennzeichnen („Betrifft Installer vor 2026-10-24: Skript aktualisieren und neu installieren“). Die Code-Details herausnehmen oder in eine Fußnote verschieben.
Status: behoben – Fix umformuliert: „fixed in the installer from 2026-10-24 on: update the installer and install again“; Code-Details in der Ursache unverändert gelassen

**C10** · Tabelle „In the pipeline“, Zeile 2 („the old variant is gone … produce the audio, run again“) · unklar · mittel
Befund: Es bleibt offen, wie man „the audio“ erzeugt und welches Skript das tut. Es ist auch unklar, ob die alte Variante wiederherstellbar ist. Der Eintrag steht zudem in Spannung zu Zeile 1, wo „audio is always copied and checked before copying“ steht. Hier wird dagegen vor dem Audio-Check entfernt. Die Reihenfolge ist für den Leser widersprüchlich.
Vorschlag: Die Reihenfolge der Installer-Schritte eindeutig beschreiben. Als Fix das Audio-Skript mit Befehl nennen und sagen, wie die alte Variante wiederhergestellt wird, oder dass der Installer sie nicht wiederherstellt.
Status: offen – Ersteller – Reihenfolge (remove, check audio, copy) ist jetzt eindeutig (siehe B2); Skript/Befehl zum Erzeugen des Audios und die Wiederherstellbarkeit der alten Variante fehlen

**C11** · Tabelle „In the pipeline“, Zeile 3 („`install_mod.py`: ‚X4 läuft‘“) · unklar · gering
Befund: Die Meldung ist deutsch, das Kapitel englisch. Das erschwert die Zuordnung für Leser ohne Deutschkenntnisse. „`--force` if you know why“ nennt nicht, in welchen Fällen das sinnvoll ist und welche Risiken bestehen.
Vorschlag: Die Meldung als wörtliches Zitat mit Übersetzung angeben („X4 läuft“ = „X4 is running“). Für `--force` ein konkretes Beispiel oder eine Warnung nennen.
Status: behoben – Meldung übersetzt: „X4 läuft“ („X4 is running“); `--force` um Risiko ergänzt („swapping under a running game can leave Boso silent“)

**C12** · Tabelle „In the pipeline“, Zeile 4 („handled by `rmtree_retry`; delete by hand after 5 attempts“) · unklar · gering
Befund: Es ist nicht klar, ob „after 5 attempts“ bedeutet, dass das Skript fünfmal versucht und dann abbricht, oder dass der Leser fünfmal selbst versuchen soll. `rmtree_retry` ist ein Funktionsname, den der Leser nicht kennt.
Vorschlag: Umformulieren: „Das Skript versucht das Löschen bis zu 5-mal; schlägt es dann fehl, den Ordner von Hand löschen (Schreibschutz-Attribut entfernen).“
Status: behoben – umformuliert: „`rmtree_retry` retries the deletion up to 5 times; if it still fails, delete the folder by hand“

**C13** · Tabelle „In the pipeline“, Zeilen 5 bis 8 („Rubberband“, „library voice“, „`quota`: HTTP 401“, „`fut.result()`“) · unverständlich · mittel
Befund: Mehrere Fachbegriffe sind ohne Erklärung. „Rubberband“ ist eine ffmpeg-Filterbibliothek. „library voice“ und „premade voice“ sind Begriffe eines TTS-Anbieters, der nicht genannt wird. „`tts-batch`“ und „`quota`“ erscheinen wie Befehle ohne Skriptnamen. Bei `--ffmpeg` fehlt das Argument, der Pfad zur ffmpeg-Datei. „`fut.result()`“ ist Python-Interna ohne Nutzen für den Leser. „user-read permission“ benennt nicht, wo der Schlüssel erstellt wird.
Vorschlag: Skriptnamen und Anbieter nennen („`tts_tool.py tts-batch`“ und so weiter). Rubberband und die Stimmenarten in einem Halbsatz erklären. `--ffmpeg <Pfad>` schreiben. „`fut.result()`“ durch „Netzwerkfehler in einem Thread“ ersetzen. Den Ort der Schlüsselrechte angeben.
Status: offen – Ersteller – Rubberband erläutert und `--ffmpeg <path to ffmpeg>` ergänzt; Skriptnamen, TTS-Anbieter, Bedeutung von library/premade voice und Ort der Schlüsselrechte sind nicht im Dokument

**C14** · Tabelle „In the pipeline“, Zeile „`install_mod.py` raises `FileExistsError`“ („`ws_<n>`“, „staging rerun“, „`copytree` has no overwrite“) · unklar · gering
Befund: „`<n>`“ ist nirgends definiert (vermutlich die Workshop-Item-Nummer). „staging rerun“ ist unklar. Die Erklärung zu `copytree` richtet sich an Entwickler und liefert dem Leser keine zusätzliche Handlungshilfe. Es fehlt der Hinweis, in welchem Verzeichnis der Ordner liegt.
Vorschlag: Schreiben: „`extensions/ws_<Workshop-ID>` existiert bereits (z. B. durch einen früheren Testlauf oder ein abonniertes Item). Den Ordner löschen und den Installer neu starten.“
Status: offen – Ersteller – Ort („in the game's `extensions` folder“) ergänzt; Bedeutung von `<n>` und „staging rerun“ ist im Dokument nicht definiert

**C15** · Tabelle „In the pipeline“, Zeile „First command extracts 0 files“ („wrong catalog (the lines are in `03.cat`, not `01.cat`) … `Select-String`“) · unklar · mittel
Befund: „First command“ hat keinen Bezug, weil nicht klar ist, welcher Befehl gemeint ist. Der Kontext (Extraktion der Spielaudiodateien aus den X4-Katalogen) fehlt. Der Fix „search the indexes with `Select-String`“ nennt weder Suchbegriff noch Pfad noch Ziel.
Vorschlag: Das Skript und den Befehl benennen und angeben, was zu suchen ist, etwa den Präfix der Sound-Id in den `.cat`-Indexdateien. Auf das Kapitel zur Extraktion verweisen.
Status: offen – Ersteller – Name des Befehls, Suchbegriff und Kapitel zur Extraktion fehlen

**C16** · Tabelle „In the pipeline“, Zeilen „Workshop upload error 16“ und „Workshop update error 9“ („create with XML only, then `update`“, „`-preview`“) · unklar · mittel
Befund: Es ist nicht erkennbar, mit welchem Werkzeug der Upload stattfindet (vermutlich das X4-Workshop-Tool). Es ist nicht erkennbar, wie „create“, „`update`“ und „`-preview`“ eingegeben werden. Es ist auch nicht klar, welche Dateien „XML only“ umfasst. Die Fehlercodes sind ohne Programmnamen nicht einzuordnen.
Vorschlag: Das Werkzeug nennen und je Fix einen Beispielaufruf angeben. Alternativ auf Kapitel 8 verweisen.
Status: offen – Ersteller – Upload-Werkzeug, Beispielaufrufe für create/update/`-preview` und Umfang von „XML only“ fehlen

**C17** · Tabelle „In the pipeline“, Zeile „Control characters in strings“ („`\v`, `\1…`“) · unverständlich · gering
Befund: Die Kürzel `\v` und `\1…` sind kryptisch. Es ist unklar, welche Dateien betroffen sind und wie man das Symptom erkennt. „write such files with an editor or raw strings“ setzt Python-Kenntnisse voraus.
Vorschlag: Ein Beispiel geben („`C:\Users\...` in einer Heredoc wird zu `Steuerzeichen + sers`“). Das Symptom benennen („unlesbare Zeichen im Pfad“).
Status: behoben – Symptom um „(garbled characters inside paths)“ ergänzt, Ursache um die Wirkung von `\v` (vertical tab) und `\1…` (octal control character) erweitert

**C18** · Tabelle „In the pipeline“, Zeile „`python` ‚Permission denied‘“ („broken Windows Store alias“, „call the real interpreter“) · unklar · gering
Befund: Der Leser erfährt nicht, wie er den echten Interpreter findet oder aufruft. Das Symptom ist nicht vollständig beschrieben: Es fehlt der Hinweis, dass `python` aus der Windows-Store-Verknüpfung stammt.
Vorschlag: Konkret machen: „Pfad zur `python.exe` direkt aufrufen oder in den Windows-Einstellungen die App-Ausführungsaliase für Python deaktivieren.“
Status: behoben – Fix konkretisiert: „call the real `python.exe` by its full path, or disable the Python entries under App execution aliases in the Windows settings“; Ursache um „the `python` stub in `WindowsApps`“ ergänzt (zugleich A8)

**C19** · Abschnitt „Edge cases in the data“, Spiegelstriche 1 bis 4 („Alternate takes (`30201430fp`)“, „Will variant“, „`10201_comm_signalleak` … excluded from the attribute list“) · unverständlich · mittel
Befund: „Alternate takes“, „Will variant“ und „the attribute list“ werden nicht erklärt. Beim ersten Punkt ist nicht klar, was `fp` bedeutet. Beim vierten Punkt ist nicht klar, zu welcher Datei die „attribute list“ gehört und welchen Zweck sie hat. Beim dritten ist nicht klar, wozu die Zahl 574 dient: Soll der Leser etwas tun oder nur wissen, dass es keine Fehler sind?
Vorschlag: Je Punkt einen Halbsatz zur Einordnung ergänzen. Die „Will variant“ kurz definieren („englische Variante mit Stimme ‚Will‘“) und die Attributliste mit Dateinamen benennen. Ebenso sagen, ob sich daraus eine Handlung ergibt.
Status: offen – Ersteller – bei „German-only ids“ „(not an error, no action needed)“ ergänzt; Bedeutung von „Alternate takes“/`fp`, „Will variant“ und „attribute list“ (Dateiname) ist im Dokument nicht erklärt

**C20** · Abschnitt „Where to look“ („`docs/MAINTENANCE.md`, `docs/dev-team/LESSONS.md`“) · unklar · gering
Befund: Die Pfade sind relativ zu einem nicht genannten Verzeichnis. Es steht nicht da, welches Problem in welchem Dokument behandelt wird. Die Dateien liegen außerhalb von `book/`, und der Leser muss raten, wo.
Vorschlag: Pfade relativ zum Repository-Wurzelverzeichnis ausweisen („im Repo-Root“) und je Verweis einen Halbsatz zum Inhalt ergänzen.
Status: offen – Ersteller – Bezugsverzeichnis der Pfade `docs/…` und der Inhalt der verwiesenen Dokumente sind nicht bekannt

### Stufe 3 – Abschlussvermerk des Erstellers
- Ergebnis: stimmig nach Korrekturen
- Korrekturen des Erstellers (Änderungsanteil 41 %, weil ich das Kapitel nach der Überarbeitung mit allen offenen Punkten neu gefasst habe; Zweck, Aufbau und alle Fehlerfälle sind erhalten):
  - A1/A2: Log-Ort, Startoption und Meldungstext belegt (`LESSONS.md:46`: `-logfile` schreibt das Log und blendet Skriptfehler ein, `-debug all` nur für Datei-I/O; `phase0-findings.md:45`: „No matching node“). Endstand behoben.
  - A3: „unavoidable“ bleibt; Verweis auf Kapitel 8, wo `save="0"` und die Folgen mit Quellenlage erklärt sind. Endstand behoben.
  - A4/C6: Messbeleg ergänzt (11 dB weniger über 1 kHz, `LESSONS.md:23`, `HISTORY.md:39`), LUFS erklärt, Fix mit Skript, Wertebereich und Kapitelverweis. Endstand behoben.
  - A5/C13: 402 = `paid_plan_required`, 401 = fehlende Leseberechtigung (`LESSONS.md:31`); Skript- und Anbietername, Rubberband, `--ffmpeg <path>`, „Netzwerkfehler in einem Worker“ statt `fut.result()`. Endstand behoben.
  - A6/B3/C15: Befehl benannt (`x4cat_extract.py`), Stand 9.00, vollständiger `Select-String`-Aufruf, Verweis auf Kapitel 3. Endstand behoben.
  - A7/B7/C16: Werkzeug (`WorkshopTool.exe publishx4`/`update`) und Ablauf genannt, Verweis auf Kapitel 8. Endstand behoben.
  - A9/C19: Zahl 574 mit Stand und Quelle (`phase0-findings.md:23`), Alternativaufnahmen, Will-Varianten und `sound_attr_ops` erklärt. Endstand behoben.
  - A10/B5/C7: Die sechs Einträge in der Einleitung aufgezählt, die vier Comm-Einträge benannt. Endstand behoben.
  - C1: Kategorienklammer entfernt, Begriffe diff, redirect und `<id>` am Anfang erklärt. Endstand behoben.
  - C2: Je Ursache eine eigene Behebung. Endstand behoben.
  - C3: Zeile „completely silent“ in vier Zeilen aufgeteilt, Soll-Dateianzahl genannt (2.324 bzw. 1.750). Endstand behoben.
  - C10: Reihenfolge der Installer-Schritte, Audio-Rezept als Fix, keine automatische Wiederherstellung. Endstand behoben.
  - C14: `ws_<number>` statt `ws_<n>`, Ort und Handlung klar. Endstand behoben.
  - C20: Pfade als repository-relativ gekennzeichnet, Inhalt je Verweis. Endstand behoben.
  - Frage 3: Die vom Überarbeiter ergänzte Erklärung zu `--force` habe ich korrigiert (die Prüfung läuft ohnehin nur für den Standard-Spielordner).
- Für den Nutzer offen: keine
- Abgeschlossen: 2026-10-25 17:54
