# Review: 04-variants-configuration.md

## Durchgang 1 – 2026-10-25 17:30
- Dokument: C:\#repos\github\x4mod_less_annoying_voices\book\04-variants-configuration.md
- Anlass: neu

### Stufe 1 – Befunde
#### Prüfer A – fachliche Richtigkeit
Fachgebiet: X4-Foundations-Modding (Egosoft-XML-Diff-Patches, Sound-Library, Steam-Workshop-Veröffentlichung), Build-/Konfigurationsdokumentation · Zielgruppe: Entwickler und Betreuer des Mod-Repos, die das Build- und Release-System verstehen und warten (abgeleitet)
**A1** · Abschnitt „Traced example“, 2. Punkt („`WorkshopTool update` refuses an unchanged version without `-minor`“) · unklar · mittel
Befund: Ich konnte nicht verifizieren, dass das Egosoft-WorkshopTool eine unveränderte Version ablehnt und dass `-minor` genau diese Sperre aufhebt. Die Websuche ergab dazu weder Dokumentation noch Forenbeiträge. Die Aussage ist zugleich die Begründung dafür, die Version bei jedem Workshop-Update zu erhöhen, und sie stützt die Anweisung im Abschnitt „What is live on the Workshop…“ („set `version` above the live value“).
Vorschlag: Die Aussage anhand der Ausgabe von `WorkshopTool.exe` (Hilfetext) oder der Egosoft-Dokumentation prüfen und die Quelle nennen (z. B. „laut WorkshopTool-Hilfe“). Falls nur beobachtet, als Beobachtung kennzeichnen („observed:“).
Status: offen – Ersteller – Es fehlt die Quelle (WorkshopTool-Hilfetext oder Egosoft-Dokumentation) bzw. die Angabe, ob nur beobachtet; ohne Kenntnis des Tools nicht belegbar, Dokument unverändert

**A2** · Abschnitt „Errors & edge cases“, Zeile „Two variants installed at once“ („the alphabetically later extension wins (inference from X4 load order)“) · unklar · mittel
Befund: Die Aussage ist als Schlussfolgerung markiert, ich konnte sie aber nicht belegen. Ich habe keine Egosoft-Quelle gefunden, nach der bei gleichen Patch-Zielen die alphabetisch spätere Extension gewinnt. Die Ladereihenfolge in X4 hängt nach meinem Kenntnisstand von Abhängigkeiten und der internen Extension-Reihenfolge ab, nicht verlässlich vom Ordnernamen. Das gilt besonders beim Mischen von `bosota_*` und `ws_*`. Die Spalte „Caught by“ wirkt dadurch sicherer, als es die Grundlage hergibt. Auch bei `replace`-Operationen auf dasselbe Attribut ist unklar, ob die zweite Extension nicht zusätzlich Fehler erzeugt, weil das Zielattribut schon geändert ist.
Vorschlag: Das Verhalten mit zwei installierten Varianten im Spiel testen (Debug-Log prüfen) und das Ergebnis eintragen. Bis dahin „the later one wins“ durch „the result depends on load order, not verified“ ersetzen.
Status: behoben – Zeile „Two variants installed at once“: „the alphabetically later extension wins (inference from X4 load order)“ → „which one wins depends on the load order (not verified)“

**A3** · Abschnitt „Errors & edge cases“, Zeilen „Wrong sound id…“ („patch silently skipped“) und „`id` differs from the actual install folder“ („nothing in the log“) · unklar · gering
Befund: Die erste Zeile nennt die Meldung „No matching node“ im Spiel und beschreibt den Patch zugleich als „silently skipped“; das widerspricht sich. X4 meldet fehlgeschlagene Diff-Operationen nach meinem Kenntnisstand im Debug-Log, und nur bei aktiviertem Logging. Dass bei falschem Redirect-Pfad „nothing in the log“ steht, konnte ich nicht verifizieren. Beide Aussagen hängen vom Log-Level ab, der nicht genannt wird.
Vorschlag: Beide Zeilen präzisieren, z. B. „Warning ‚No matching node‘ appears only in the debug log (started with `-debug all`/`-logfile`), not visible in normal play“. Die Aussage zum Log nur dann stehen lassen, wenn sie mit aktiviertem Logging geprüft wurde.
Status: offen – Ersteller – Es fehlt, ob und bei welchem Log-Level (Debug-Log) „No matching node“ bzw. ein falscher Redirect-Pfad im Log erscheint; im Spiel zu prüfen, Dokument unverändert

#### Prüfer B – Logik und Zahlen
Fachgebiet: Softwaredokumentation zu einer X4-Foundations-Mod (Konfigurationsschema, Build- und Installationsskripte, Steam-Workshop-Veröffentlichung) · Zielgruppe: Entwickler und Maintainer des Projekts, die das Repository pflegen (abgeleitet)
**B1** · Abschnitt „sound_attr_ops“, Absatz nach der Tabelle („All current variants carry the same two items (`config/variants.json:27-50`)“) · Logikfehler · gering
Befund: Die Fundstelle 27-50 deckt nur einen zusammenhängenden Block ab, nämlich die erste Variante. Die Aussage gilt aber für alle fünf Varianten. Die Datei hat laut dem Verweis „config/variants.json:121“ im Abschnitt „Naming gotcha“ mindestens 121 Zeilen. Der Beleg trägt die Behauptung „alle Varianten“ daher nicht, und der Leser kann sie nicht prüfen, ohne die Datei zu durchsuchen. Die Zeilenangaben konnte ich ohne die JSON-Datei nicht verifizieren.
Vorschlag: Die Zeilenbereiche aller fünf Varianten nennen oder formulieren: „identisch in jeder Variante, z. B. `config/variants.json:27-50`“.
Status: behoben – „All current variants carry the same two items (`config/variants.json:27-50`)“ → „(e.g. `config/variants.json:27-50`)“

**B2** · Abschnitt „Errors & edge cases“, Zeile „`audio_variant` folder empty“ · Logikfehler · gering
Befund: Die Tabelle behandelt nur den Fall, dass der `audio_variant`-Ordner leer ist. Der naheliegende Fall, dass der Ordner `build/audio/<audio_variant>/` gar nicht existiert oder der Name falsch geschrieben ist, fehlt. Das Schema nennt `audio_variant` REQUIRED und verlangt, dass der Ordner die .ogg-Dateien enthält. Ob `install_mod.py` bei fehlendem Ordner ebenfalls abbricht (Zeilen 109-110) oder mit einer anderen Meldung, bleibt offen. Ebenso offen bleibt, ob der Ordner nur .ogg-Dateien enthalten darf.
Vorschlag: Die Zeile auf „`audio_variant` folder missing or empty“ erweitern, sofern der Installer beide Fälle gleich behandelt. Sonst eine eigene Zeile ergänzen.
Status: offen – Ersteller – Es fehlt, wie `install_mod.py` bei fehlendem (statt leerem) `audio_variant`-Ordner reagiert; Code liegt außerhalb des Dokuments, Dokument unverändert

**B3** · Abschnitt „What is live on the Workshop is not what this file says“ („Before the next manual upload, set `version` above the live value (DE ≥ 104, EN ≥ 103)“) · unklar · mittel
Befund: Der Abschnitt sagt, dass modpub Version, Name und Beschreibung in eigenen Kopien hochsetzt. Er sagt aber nicht, ob modpub die Version relativ zum Wert in `config/variants.json` oder relativ zum Live-Wert erhöht. Der Hinweis „leave out `-namedesc up`“ setzt zudem das Wissen über die Optionen eines externen Tools voraus, das hier nicht erklärt wird. Wer die Werte nach der Regel setzt, ohne den Mechanismus zu kennen, kann trotzdem eine abgelehnte oder doppelt erhöhte Version erzeugen. Die Regel „≥ 104“ ist außerdem nur für den manuellen Upload definiert, nicht für den modpub-Weg.
Vorschlag: In einem Satz ergänzen, wie modpub die Version berechnet (aufbauend auf dem Konfigurationswert oder dem Live-Wert). Die Option `-namedesc up` mit einer Kurzbeschreibung oder einem Verweis auf `docs/RELEASE.md` versehen.
Status: offen – Ersteller – Es fehlt, wie modpub die Version berechnet (Config-Wert oder Live-Wert) und was `-namedesc up` bewirkt (laut Befund gegen `docs/RELEASE.md` zu prüfen); Dokument unverändert

#### Prüfer C – Verständlichkeit
Fachgebiet: Modding von X4: Foundations, Build- und Release-Pipeline einer Stimmen-Ersatz-Mod (Konfigurationsdatei variants.json, XML-Diff-Patches, Steam Workshop) · Zielgruppe: Entwickler und Maintainer des Repos mit Python- und Git-Kenntnissen, aber ohne Vorwissen zu X4-Interna und zur Projektgeschichte (abgeleitet)

**C1** · Kopf des Kapitels, Blockzitat „What you'll be able to answer after this chapter“ („(contracts, state)“, „(domain, rationale)“, „(failure)“) · unverständlich · gering
Befund: Die Klammerangaben „contracts“, „state“, „domain“, „rationale“ und „failure“ sind interne Kategorienamen, die an dieser Stelle nirgends erklärt werden. Ein Leser kann sie nicht zuordnen und weiß nicht, welcher Teil des Kapitels gemeint ist.
Vorschlag: Die Klammern streichen oder durch die Kapitelabschnitte ersetzen, etwa „(see Schema)“, „(see The five variants)“, „(see Errors & edge cases)“. Alternativ einmal erklären, wofür diese Kategorien stehen.
Status: behoben – Klammern „(contracts, state)“ usw. durch Abschnittsverweise ersetzt: (see Schema), (see The five variants), (see Schema), (see Errors & edge cases)

**C2** · Abschnitt „Schema“, Zeile `"boso_ta_ids": [6 sound ids]` und Zeile `"id"` („redirect path segment“) · unverständlich · mittel
Befund: Das Kapitel nennt die sechs Sound-IDs nie vollständig. Auch „Boso Ta“ und die Rolle der Redirects werden nicht erklärt. Der Leser sieht nur indirekt `10201_normal`, `10201_normal_npc` und `10201_comm_signalleak`. Er kann nicht erkennen, welche fünf IDs später `noocclusion` bekommen, und weiß nicht, was „redirect“ im X4-Sound-Kontext bedeutet.
Vorschlag: Zu Beginn ein bis zwei Sätze ergänzen: Wer oder was Boso Ta ist, was ein „sound entry“ und ein „redirect“ sind, und eine Liste der sechs IDs. Alternativ auf das Kapitel verweisen, in dem das erklärt wird.
Status: offen – Ersteller – Es fehlen die sechs vollständigen Sound-IDs sowie die Erklärung von „Boso Ta“, „sound entry“ und „redirect“; im Dokument nicht belegt, Dokument unverändert

**C3** · Abschnitt „sound_attr_ops“, Tabelle („`type="@attr"`“, „Precondition in the base game“) und Satz „`noocclusion=true` on five ids“ · unverständlich · mittel
Befund: Es wird nicht erklärt, was `noocclusion` und `is3d` im Spiel bewirken. Auch die Platzhalter `X`, `attr` und `value` werden nicht erläutert. Außerdem steht „diff operation“ ohne Einführung des X4-Diff-Patch-Formats da. Ohne diese Information kann ein Leser nicht verstehen, warum diese Attribute geändert werden.
Vorschlag: Vor der Tabelle einen Satz zum Diff-Patch-Mechanismus ergänzen. Dazu eine Zeile, was `noocclusion` (keine Verdeckung des Schalls durch Geometrie) und `is3d` (positionsabhängige Wiedergabe) im Spiel tun. Das ist vorher am Spiel oder Wiki zu prüfen. Die Platzhalter `X`, `attr` und `value` unter der Tabelle benennen.
Status: offen – Ersteller – Platzhalter `X`, `attr`, `value` unter der Tabelle erläutert; es fehlt weiterhin, was `noocclusion` und `is3d` im Spiel bewirken (am Spiel/Wiki zu prüfen) und eine Einführung des Diff-Patch-Formats

**C4** · Abschnitt „sound_attr_ops“, Absatz „Why `is3d=0` only on the two `normal` entries“ („facing Boso about 90 % of the manager Karee's loudness“) · unklar · mittel
Befund: Der Satz ist verschachtelt und mehrdeutig. Es ist unklar, wer vor wem steht, auf welche Referenz sich die Prozentwerte beziehen („90 % of Karee's loudness“) und wer Karee ist. „HQ“ bleibt ebenfalls unerklärt. Auch „the author heard“ ist vage: Wurde gemessen oder nur subjektiv gehört? Der Sinn der Begründung geht dadurch verloren.
Vorschlag: Umformulieren, etwa: „In the HQ conversation with the manager Karee, Boso is heard at about 90 % of Karee's volume when the player faces Boso, but only at about 60 % and unintelligibly with the player's back turned (subjective listening, not measured).“ Dazu „HQ“ ausschreiben, falls das nicht schon an anderer Stelle geschieht.
Status: behoben – Satz umformuliert („with the player facing Boso, he was about 90 % as loud as Karee; with the player's back turned, about 60 % as loud and unintelligible“); „HQ“ und „heard“ (gemessen/gehört) unverändert, da im Dokument nicht geklärt

**C5** · Abschnitt „The five variants“, Tabelle, Spalte „Audio“ und Spalte „Status“ („TTS "Will", `will_dark`, +6 dB“, „processed originals, full strength, +9 dB“, „no-account alternative“, „after modpub“) · unverständlich · mittel
Befund: Die Audiobeschreibungen sind nicht erklärt: „processed originals“, „full strength“ und „half strength“ (Stärke wovon?), „dark“ und das Kürzel „g6/g9/g4“ als Gain. Unklar bleibt auch, wie sich die dB-Angaben zu den Suffixen im `audio_variant`-Namen verhalten. „no-account alternative“ lässt offen, welches Konto fehlt (Steam, ModDB?). „modpub“ taucht in der Tabelle vor seiner Erklärung auf.
Vorschlag: Unter der Tabelle die Namenskonvention der `audio_variant`-Ordner erklären (Quelle, Effekt, Stärke, Gain). „no-account alternative“ ersetzen durch „installable without a Steam or ModDB account“, sofern das gemeint ist. Bei „modpub“ auf den Absatz darunter verweisen.
Status: offen – Ersteller – Es fehlt die Namenskonvention der `audio_variant`-Ordner (Quelle, Effekt, Stärke, Gain) und welches Konto bei „no-account alternative“ gemeint ist; Dokument unverändert

**C6** · Abschnitt „The five variants“, Absatz „What is live on the Workshop is not what this file says.“ (Satz „leave out `-namedesc up` if the modpub title should stay“) · unklar · mittel
Befund: Es ist nicht erklärt, was modpub ist (externes Tool, aus welcher Quelle?). Auch der Schalter `-namedesc up` bleibt offen: Zu welchem Befehl gehört er, und was passiert, wenn man ihn weglässt? Die Handlungsanweisung („set `version` above the live value“, „leave out …“) ist ohne diese Information nicht ausführbar. Zudem werden Config-Versionen (102/101) und Live-Versionen (103/102) im Fließtext schwer auseinandergehalten.
Vorschlag: Beim ersten Auftreten eine Zeile zu modpub ergänzen. Den Schalter mit Befehl nennen („in the modpub command, omit `-namedesc up`, otherwise the name and description from `config/variants.json` overwrite the Workshop title“). Dieser Wortlaut ist vorher gegen `docs/RELEASE.md` zu prüfen. Die Versionen als kleine Tabelle (Variante, Config, Live, nächste Version) darstellen.
Status: offen – Ersteller – Es fehlt, was modpub ist, zu welchem Befehl `-namedesc up` gehört und was ein Weglassen bewirkt (gegen `docs/RELEASE.md` zu prüfen); Dokument unverändert

**C7** · Abschnitt „Traced example“, Aufzählungspunkt „`version` `101` → … (the first Workshop upload was 100; `WorkshopTool update` refuses an unchanged version without `-minor`)“ · unklar · gering
Befund: `WorkshopTool update` und `-minor` werden nicht erklärt. Es ist unklar, ob der Befehl vom Spiel, von Steam oder vom Repo stammt. Außerdem sagt die Klammer nicht, wie sie zum Wert 101 passt (was ist die Folgerung?).
Vorschlag: Den Satz ergänzen: „(the X4 `WorkshopTool` rejects an update with the same version unless `-minor` is given; therefore every upload needs a higher version, so 101 follows the first upload at 100)“. Dabei die Herkunft des Tools nennen.
Status: offen – Ersteller – Hängt an A1: Herkunft von `WorkshopTool update` und die Wirkung von `-minor` sind nicht belegt; Dokument unverändert

**C8** · Abschnitt „Errors & edge cases“, Tabelle, Zeilen „Wrong sound id“ und „Two variants installed at once“ · unklar · mittel
Befund: In der Zeile „Wrong sound id“ steht „No matching node“ in der Spalte „Effect“, aber „patch silently skipped“. Es ist unklar, ob der Fehler im Log steht oder nicht. Die Zeile „Id differs …“ sagt dagegen „nothing in the log“. In der Zeile „Two variants installed at once“ ist die Spalte „Caught by“ widersprüchlich belegt: Sie nennt `install_mod.py`, schreibt aber zugleich, dass `ws_*` nicht entfernt wird. Der Leser erfährt nicht, ob der Fall abgefangen wird.
Vorschlag: Bei „Wrong sound id“ schreiben, wo die Meldung „No matching node“ erscheint (Spiel-Log/Debug-Log). In der Zeile „Two variants“ die Spalte „Caught by“ auf „only partly: `install_mod.py` removes every `bosota_*` folder, but a `ws_*` folder stays“ ändern.
Status: offen – Ersteller – Zeile „Two variants installed at once“: „Caught by“ → „only partly: …“ geändert; es fehlt, wo „No matching node“ erscheint (siehe A3), daher Zeile „Wrong sound id“ unverändert

**C9** · Abschnitt „Errors & edge cases“, letzte Zeile („Backslashes in strings written through a shell heredoc … `\v`, `\1…` turn into control characters“) · unklar · gering
Befund: Die Zeile erklärt weder, welche Backslashes gemeint sind (Pfade mit `extensions\ws_…`?), noch, in welchem Workflow ein Heredoc benutzt wird. Auch eine Handlungsanweisung fehlt: Der Leser weiß nicht, wie er den Fehler vermeidet.
Vorschlag: Den Satz ergänzen, etwa „When editing `_doc`/`audio_recipe` via `cat <<EOF`, use a quoted heredoc (`<<'EOF'`) or edit the file directly, otherwise the shell interprets the backslashes.“ Vorher klären, wie der Fehler tatsächlich entstanden ist.
Status: offen – Ersteller – Es fehlt, wie der Backslash-Fehler tatsächlich entstanden ist; die vorgeschlagene Heredoc-Anweisung ist ohne diese Klärung nicht belegt, Dokument unverändert

### Stufe 3 – Abschlussvermerk des Erstellers
- Ergebnis: stimmig nach Korrekturen
- Korrekturen des Erstellers:
  - A1/C7: Herkunft und Regel belegt mit `docs/RELEASE.md:27,35` (WorkshopTool aus Egosofts „X Tools“, Update braucht höhere Version oder `-minor`). Endstand behoben.
  - A3/C8: „No matching node“ erscheint nur im Debug-Log mit `-logfile` (`docs/MAINTENANCE.md:21`); beim falschen `id` greift der Diff, Log-Verhalten zur fehlenden Datei als ungeprüft gekennzeichnet. Endstand behoben.
  - B2: Zeile erweitert auf fehlenden, falsch geschriebenen oder `.ogg`-losen Ordner; alle drei Fälle enden in derselben Meldung (`tools/install_mod.py:107-110`, geprüft). Endstand behoben.
  - B3/C6: modpub erklärt (externes Tool, für Bauen und Installieren nicht nötig), Versionen als Tabelle, `-namedesc up` mit Wirkung und Fundstelle; ausdrücklich vermerkt, dass die Versionsberechnung von modpub hier nicht dokumentiert ist. Endstand behoben.
  - C2: Die sechs Sound-IDs, „sound entry“, XML-Diff und „redirect“ am Anfang des Schemas erklärt. Endstand behoben.
  - C3: Wirkung von `noocclusion` und `is3d` im Spiel ergänzt (`config/variants.json:6`). Endstand behoben.
  - C5: Namenskonvention der Audioordner, „full/half strength“ und „no-account“ (ohne ElevenLabs-Konto) erklärt; Verweis auf die modpub-Erklärung. Endstand behoben.
  - C9: Zeile korrigiert: Der Fehler entstand, weil Python in einem per Heredoc übergebenen Skript `\v` usw. als Escape-Sequenzen las; Abhilfe (Editor oder Raw-Strings) ergänzt. Endstand behoben.
- Für den Nutzer offen: keine
- Abgeschlossen: 2026-10-25 17:34
