# Review: 05-building-and-validating.md

## Durchgang 1 – 2026-10-25 17:34
- Dokument: C:\#repos\github\x4mod_less_annoying_voices\book\05-building-and-validating.md
- Anlass: neu

### Stufe 1 – Befunde
#### Prüfer A – fachliche Richtigkeit
Fachgebiet: Modding für X4: Foundations (XML-Diff-Patches an libraries/sound_library.xml, Python-Build- und Validierungswerkzeuge) · Zielgruppe: Entwickler und Modder des Projekts, die den Generator und den Validator warten oder bedienen (abgeleitet)

**A1** · Abschnitt „Side effects and gotchas“, letzter Punkt („containing `'`, `&`, `<` or `--` would produce broken XML or a broken selector“) · sachlicher Fehler · gering
Befund: Die Zeichenfolge `--` macht weder in einem Attributwert noch in Elementtext ein XML-Dokument ungültig. Sie ist nur in XML-Kommentaren verboten. Der f-String-Diff enthält an dieser Stelle keine Kommentare, die Aufzählung ist also sachlich falsch. `'` zerstört den XPath-Selektor, `&` und `<` zerstören das XML.
Vorschlag: `--` aus der Aufzählung streichen: „containing `'`, `&` or `<` would produce broken XML or a broken selector“.
Status: behoben – `--` aus der Aufzählung im letzten Punkt von „Side effects and gotchas“ gestrichen; Zeichen jetzt zugeordnet (`'` Selektor, `&`/`<` XML)

**A2** · Abschnitt „Why two tools“, 1. Satz („the game writes "No matching node" into its log (only when started with `-logfile`)“) · unklar · mittel
Befund: Ich konnte weder den genauen Meldungstext „No matching node“ noch die Bedingung „nur mit `-logfile`“ verifizieren. Die Recherche fand nur den Hinweis, dass Egosoft-Forenbeiträge `-debug all -logfile <datei>` empfehlen, damit Patch-Fehler im Log erscheinen (z. B. https://forum.egosoft.com/viewtopic.php?p=4768487). Ob `-logfile` allein genügt, ist nicht belegt. Die Aussage trägt die Begründung für das gesamte Kapitel.
Vorschlag: Meldungstext und Startoption am echten Spiel-Log prüfen und die genaue Zeile zitieren. Falls zutreffend, die Option als `-debug all -logfile <datei>` angeben. Sonst abschwächen („the game logs a patch error, visible with logging enabled“).
Status: offen – Ersteller – Meldungstext „No matching node“ und die nötige Startoption (`-logfile` allein oder `-debug all -logfile`) sind nur am echten Spiel-Log prüfbar

**A3** · Abschnitt „build_content“ („`save="0"` only means the save does not list the mod as a requirement; it does **not** prevent the "modified" mark“) · unklar · mittel
Befund: Die Semantik von `save` in content.xml ist nicht verifizierbar. Die Recherche fand kein offizielles Egosoft-Dokument dazu, nur Beispiel-content.xml mit `save="0"`. Die Aussage ist sehr bestimmt formuliert („does not prevent the modified mark“), stützt sich aber auf keine genannte Quelle.
Vorschlag: Eine Quelle oder einen Test (Savegame mit und ohne Mod) nennen. Sonst als beobachtetes Verhalten kennzeichnen, z. B. „observed on X4 9.00“.
Status: offen – Ersteller – Quelle oder Test (Savegame mit/ohne Mod) zur Wirkung von `save="0"` auf die „modified“-Markierung fehlt

**A4** · Abschnitt „build_content“ („an unescaped `&` would make X4 drop the extension without any message“) · unklar · gering
Befund: Das Verhalten des Spiels bei ungültigem content.xml (stilles Verwerfen ohne Meldung) ist nicht belegt und nicht von mir verifizierbar. Es klingt wie eine Beobachtung, steht aber als Tatsache da.
Vorschlag: Als beobachtet kennzeichnen oder abschwächen („X4 may ignore the extension; no message was observed“).
Status: offen – Ersteller – Beleg oder Beobachtung, dass X4 bei unescaptem `&` die Extension ohne Meldung verwirft, fehlt

**A5** · Abschnitt „Mechanism“, Punkt 1 („DLC diffs are **not** applied; that is safe here because no DLC touches `10201_*` (verified, `docs/phase0-findings.md`)“) · unklar · gering
Befund: Die Aussage hängt an einer externen Datei, die ich nicht lesen durfte. Sie kann sich mit neuen DLCs oder Patches ändern, denn Kapitel 9 behandelt Patch-Pflege. Der Stand der Prüfung (Spielversion, DLC-Liste) fehlt.
Vorschlag: Prüfstand ergänzen, z. B. „verified for X4 9.00 with DLCs …“. Im Patch-Wartungskapitel als Prüfpunkt führen.
Status: offen – Ersteller – Prüfstand (Spielversion, DLC-Liste) der Aussage in `docs/phase0-findings.md` ist im Dokument nicht genannt

**A6** · Abschnitt „Traced example“ („on X4 9.00: base file from `08.cat`“) · unklar · gering
Befund: Die Katalognummer, aus der die Basisdatei stammt (`08.cat`), ist versionsabhängig. Auch das Diagramm zeigt sie als festen Wert, obwohl die Suche nach dem höchsten Katalog gehen soll. Ein Leser kann „08.cat“ fälschlich für eine feste Eigenschaft halten.
Vorschlag: In Diagramm und Beispiel „z. B.“ bzw. „in 9.00“ ergänzen.
Status: behoben – Diagramm: „…/08.cat“ → „…/08.cat“ (in X4 9.00); Beispiel: Hinweis „catalog number depends on the game version“ ergänzt

#### Prüfer B – Logik und Zahlen
Fachgebiet: Softwareentwicklung / Modding für X4 Foundations, Build- und Validierungswerkzeuge für XML-Diff-Patches · Zielgruppe: Entwickler und Wartende des Mod-Projekts, die Python lesen können, aber X4-Interna nicht kennen (abgeleitet)

**B1** · Abschnitt „`validate_mod.py` / Mechanism“, Punkt 1 („fetches the effective `sound_library.xml` from the highest base catalog“) und Sequenzdiagramm („scan 01.cat … 09.cat“ → „…/08.cat“) · Logikfehler · gering
Befund: Der Text spricht vom „highest base catalog“. Das Diagramm scannt bis 09.cat und liefert 08.cat, und das traced example nennt 08.cat. Gemeint ist offenbar der höchste Katalog, der die Datei enthält. Ein Leser kann darin einen Widerspruch sehen (08 ist nicht die höchste Nummer), und `find_latest_entry` macht das nicht eindeutig.
Vorschlag: Formulieren: „aus dem höchstnummerierten Basiskatalog, der die Datei enthält (hier 08.cat; 09.cat enthält sie nicht)“, sofern das zutrifft. Das ist am Code zu prüfen.
Status: behoben – „highest base catalog“ → „highest-numbered base catalog that contains it“ in Mechanism Punkt 1; Code selbst nicht geprüft, Formulierung folgt dem Diagramm (Scan bis 09.cat, Treffer 08.cat)

**B2** · Abschnitt „`validate_mod.py` / Mechanism“, Punkt 4 („applied to a deep copy (`:58`)“) · Logikfehler · gering
Befund: Die Zeilenverweise laufen nicht in der Reihenfolge der Schritte. Punkt 2 nennt `:62-69` und Punkt 3 `:77-78`, Punkt 4 dagegen `:58`, das vor Punkt 2 liegt. Das passt nur, wenn die Kopie vor dem Lesen von content.xml angelegt wird (Diagramm: „deepcopy per extension“). Die Reihenfolge der Schritte im Text weicht also von der Reihenfolge im Code ab, oder der Verweis ist falsch.
Vorschlag: Verweis `:58` prüfen. Falls die Kopie vor der content.xml-Prüfung entsteht, das in Punkt 4 erwähnen oder die Schritte entsprechend umordnen.
Status: offen – Ersteller – Zeilenverweis `:58` und tatsächliche Reihenfolge im Code (Kopie vor oder nach content.xml-Prüfung) lassen sich ohne Quelltext nicht klären

**B3** · Abschnitt „`build_content`“, Satz „`date` is today's date, so rebuilding changes `content.xml` even if nothing else did“ · Logikfehler · gering
Befund: Die Folgerung stimmt nur, wenn der Neubau an einem anderen Kalendertag stattfindet. Beim Neubau am selben Tag bleibt die Datei unverändert. Die Aussage ist so zu allgemein.
Vorschlag: Formulieren: „…so rebuilding on a different day changes `content.xml` even if nothing else did“.
Status: behoben – „rebuilding changes“ → „rebuilding on a different day changes“ in build_content

**B4** · Abschnitt „Side effects and gotchas“, letzter Punkt („containing `'`, `&`, `<` or `--` would produce broken XML or a broken selector“) · sachlicher Fehler · gering
Befund: `--` ist in Attributwerten und Elementtext gültiges XML und nur in Kommentaren verboten. Der Diff enthält keine Kommentare, die aus Konfigurationswerten entstehen. Die Aufzählung ist daher teilweise falsch. Außerdem ist unklar, ob das Ergebnis „broken XML“ oder „broken selector“ ist. `'` in einer ID bricht nur den Selektor. Ob der Validator diesen Fall als Fehler meldet, wird nicht gesagt, obwohl der Satz das behauptet („would catch the broken XML“).
Vorschlag: `--` streichen. Pro Zeichen angeben, ob es XML oder Selektor bricht, und klarstellen, dass der Validator einen kaputten Selektor als „No matching node“ oder XPath-Fehler meldet. Das ist am Code zu prüfen.
Status: behoben – `--` gestrichen, Zeichen zugeordnet (`'` bricht den Selektor, `&`/`<` das XML); ob der Validator einen kaputten Selektor meldet, wurde nicht ergänzt (Code nicht einsehbar)

**B5** · Abschnitt „`build_content`“, Satz „an unescaped `&` would make X4 drop the extension without any message“ · unklar · gering
Befund: Die Aussage zum Spielverhalten („without any message“) ist im Dokument nicht belegt. Ich konnte sie nicht verifizieren. Im Abschnitt „Why two tools“ heißt es zudem, X4 schreibe Meldungen nur mit `-logfile`. „Without any message“ widerspricht dem also womöglich oder ist zumindest mehrdeutig (keine Meldung im Spiel oder auch keine im Log).
Vorschlag: Präzisieren („no message in the game UI; the log entry appears only with `-logfile`“) oder als Beobachtung kennzeichnen und die Quelle nennen (z. B. `docs/phase0-findings.md`).
Status: offen – Ersteller – Beleg, was X4 bei unescaptem `&` tatsächlich tut (keine Meldung im UI oder auch nicht im Log), fehlt

**B6** · Abschnitt „Traced example“ („report line for `10201_normal`“) · Logikfehler · gering
Befund: Laut „Report“ (Punkt 5) gibt der Validator für jede berührte ID eine Zeile aus. Berührt werden sechs Redirect-IDs plus die IDs der Attribut-Operationen. Das Beispiel nennt nur eine Zeile (`10201_normal`). Es bleibt offen, ob die übrigen Zeilen gleich lauten oder ob nur diese ID berührt wird. Dann passten „6 replaces“ auf „all six entries“ nicht zusammen.
Vorschlag: Ergänzen, dass es sich um einen Auszug handelt („one of N report lines“), oder die Zeilen für alle IDs auflisten.
Status: offen – Ersteller – unbekannt, wie viele Report-Zeilen der Validator tatsächlich ausgibt und ob die übrigen IDs gleich lauten

#### Prüfer C – Verständlichkeit
Fachgebiet: Python-Build- und Validierungswerkzeuge für X4-Foundations-Mods (XML-Diff-Patches für `sound_library.xml`, Katalogextraktion) · Zielgruppe: Entwickler bzw. Wartende dieses Mod-Projekts mit Python- und XML-Kenntnissen, aber ohne tiefes X4-Modding-Wissen (abgeleitet)

**C1** · Einleitung, Zitat „contracts, flow“ / „failure, rationale“ / „operations“ · unverständlich · gering
Befund: Die Klammerbegriffe („contracts, flow“, „failure, rationale“, „operations“) stehen ohne Erklärung. Ein Leser kann sie nicht zuordnen, denn im Kapitel gibt es keine Abschnitte mit diesen Namen. Nur „Operations“ kommt als Überschrift vor, und dort ist etwas anderes gemeint als die Diff-„operations“ im Rest des Kapitels.
Vorschlag: Die Klammern streichen oder durch Verweise auf die Abschnitte ersetzen, z. B. „(Abschnitt build_diff)“, „(Abschnitt What it catches and what it misses)“, „(Abschnitt Operations)“.
Status: behoben – Klammerbegriffe in der Einleitung durch Verweise auf die Abschnitte „build_diff mechanism“, „Mechanism“, „What it catches and what it misses“ und „Operations“ ersetzt

**C2** · Abschnitt „Why two tools“, Zitat „X4 applies a mod's `libraries/sound_library.xml` diff to its own file“ · unverständlich · mittel
Befund: Der Begriff „diff“ (X4-Patch-Datei mit `<add>`, `<replace>`, `<remove>` und XPath-Selektoren) und das Wort „selector“ werden nicht erklärt. Das Kapitel setzt voraus, dass der Leser das Diff-Prinzip schon kennt. Ob ein früheres Kapitel es erklärt, lässt sich aus diesem Text nicht entnehmen.
Vorschlag: Einen Satz ergänzen, z. B. „Eine Diff-Datei ist eine Liste von Änderungsbefehlen (`add`, `replace`, `remove`), die X4 mit einem XPath-Selektor auf die Originaldatei anwendet“, oder auf das Kapitel verweisen, in dem das erklärt wird.
Status: behoben – Satz zur Definition von Diff (Liste von `add`/`replace`/`remove`-Befehlen mit XPath-Selektor) in „Why two tools“ ergänzt

**C3** · Abschnitt „build_mod.py / Public surface“, Zitate „[--only <variant key>]“, „dist/<id>/“, „build/audio/<audio_variant>/“ · unklar · mittel
Befund: „variant key“, „<id>“ und „<audio_variant>“ sind drei Platzhalter, die nicht definiert werden. Es bleibt offen, woher sie kommen (Konfigurationsdatei?) und wie sie zusammenhängen. Auch `python -I` wird nicht erklärt (isolierter Modus). „It does not touch audio“ ist mehrdeutig: Gemeint ist offenbar, dass keine Audiodateien erzeugt, konvertiert oder kopiert werden.
Vorschlag: Ein bis zwei Sätze zur Konfiguration ergänzen: wo sie liegt, was ein Variant-Key, die `id` und `audio_variant` sind. Bei `-I` kurz „(Python-Isolated-Mode)“ nennen. Den Satz ersetzen durch „Es erzeugt, konvertiert oder kopiert keine Audiodateien.“
Status: offen – Ersteller – Erläuterung von `-I` und „does not touch audio“ ergänzt; fehlt: wo die Konfiguration liegt und was Variant-Key, `id` und `audio_variant` sind

**C4** · Abschnitt „build_diff mechanism“, Codekommentare „# → literal path, no language suffix“ und „# → all six entries“ · unverständlich · mittel
Befund: „10201“, „normal“ und „boso_ta_ids“ sind unerklärt: Der Leser erfährt nicht, wofür die Voice-ID 10201 steht und welche sechs Sound-IDs gemeint sind. „no language suffix“ ist ohne Vergleichsfall nicht nachvollziehbar, denn Egosoft hängt bei Sprachordnern sonst Sprachkennungen an. Das Kürzel „→“ in den Kommentaren erklärt nichts, sondern deutet nur an.
Vorschlag: Kommentare als ganze Sätze formulieren, z. B. „Zielpfad ohne Sprachkennung, weil die Dateien für alle Spielsprachen gelten“. Außerdem kurz erklären, was Voice 10201 ist und was die sechs `boso_ta_ids` sind.
Status: offen – Ersteller – Bedeutung von Voice 10201, der sechs `boso_ta_ids` und der Grund für „no language suffix“ stehen nicht im Dokument

**C5** · Abschnitt „build_diff mechanism“, Zitat „(6 replaces, 5 adds, 2 replaces)“ · unklar · mittel
Befund: „replaces“ steht zweimal mit verschiedener Bedeutung (sechs Sample-Redirects, zwei Attribut-Replaces). Ohne Bezug zum Code ist das missverständlich. Woher „5 adds“ und „2 replaces“ kommen, steht nicht da (`sound_attr_ops` wird nirgends inhaltlich erklärt). Die Summe 13 taucht erst im Beispiel weiter unten auf.
Vorschlag: Ausschreiben: „6 Sample-Redirects, 5 Attribut-`add`, 2 Attribut-`replace` (zusammen 13 Operationen)“. Die Attribute und Sound-IDs aus `sound_attr_ops` kurz nennen, z. B. `is3d` und `noocclusion`, oder auf die Konfigurationsdatei verweisen.
Status: behoben – „(6 replaces, 5 adds, 2 replaces)“ → „(6 sample redirects, 5 attribute `add`s, 2 attribute `replace`s: 13 operations in total)“; Attributnamen nicht ergänzt, da die Konfiguration nicht vorliegt

**C6** · Abschnitt „build_content“, Zitat „does **not** prevent the "modified" mark“ · unverständlich · mittel
Befund: Der Leser erfährt nicht, was die „modified“-Markierung ist (Hinweis im Spielstand oder Menü?), wo sie erscheint und warum der Mod sie auslöst. Die Aussage zu `save="0"` ist deshalb nicht nachvollziehbar. Auch die Sprachcodes 44 und 49 sind nur über die Klammern „(English)“ und „(German)“ erklärt, die Herkunft der Codes bleibt offen. „localised“ ist zudem britische Schreibweise, im Text sonst nicht durchgängig.
Vorschlag: Ergänzen, z. B. „…; X4 zeigt den Spielstand trotzdem als ‚modifiziert‘ (Spielstand-Auswahl), sobald ein Mod geladen war.“ Außerdem erwähnen, dass 44/49 die X4-Sprach-IDs sind.
Status: offen – Ersteller – Bedeutung und Anzeigeort der „modified“-Markierung sowie Herkunft der Sprachcodes 44/49 sind nicht belegt

**C7** · Abschnitt „Side effects and gotchas“, 2. Aufzählungspunkt, Zitat „can make `init.sh` fail“ · unverständlich · mittel
Befund: `init.sh` wird hier zum ersten Mal erwähnt und nicht eingeführt. Erst im Abschnitt „Operations“ steht, dass es beide Tools aufruft. Ein Leser weiß an dieser Stelle nicht, was `init.sh` ist.
Vorschlag: Beim ersten Vorkommen ergänzen: „`init.sh` (das Skript, das Build und Validierung nacheinander ausführt, siehe Abschnitt Operations)“.
Status: behoben – `init.sh` beim ersten Vorkommen als „the script that runs build and validation, see "Operations"“ eingeführt

**C8** · Abschnitt „Side effects and gotchas“, letzter Punkt, Zitat „containing `'`, `&`, `<` or `--`“ · unklar · gering
Befund: Warum `--` Probleme macht, wird nicht erklärt (in XML-Kommentaren verboten, in Attributwerten und Elementinhalt unproblematisch). Der Satz „broken XML or a broken selector“ ordnet nicht zu, welches Zeichen was verursacht. Der Leser kann nicht beurteilen, ob das Risiko für ihn relevant ist.
Vorschlag: Zuordnen: „`'` bricht den Selektor, `&` und `<` brechen das XML; `--` ist nur in XML-Kommentaren verboten und hier vermutlich nicht relevant“. Falls `--` gar nicht relevant ist, streichen.
Status: behoben – bereits durch A1 behoben

**C9** · Abschnitt „validate_mod.py / Mechanism“, Mermaid-Diagramm und Punkt 1, Zitate „x4cat_extract“, „[REL]“, „scan 01.cat … 09.cat“, „highest base catalog“ · unverständlich · mittel
Befund: `x4cat_extract` (Modul oder Skript?), `REL` (Konstante für den relativen Pfad), das Katalogformat `.cat` und warum der höchste Katalog der „effektive“ ist, werden nicht erklärt. Der Leser weiß nicht, dass X4 spätere Kataloge frühere überschreiben lässt. „base catalog“ ist gegenüber DLC-Katalogen nicht abgegrenzt. Im Diagramm steht „08.cat“, im Fließtext heißt es „highest base catalog“. Wie das zusammenpasst (9 Kataloge, höchster Fund ist 08), ist unklar.
Vorschlag: Ergänzen: „X4 liest die Kataloge `01.cat`, `02.cat` usw. in aufsteigender Reihenfolge; eine spätere Datei gleichen Pfads überschreibt eine frühere. `x4cat_extract` ist das Hilfsmodul des Projekts zum Auslesen der Kataloge.“ Außerdem `REL` im Diagramm durch den Pfad ersetzen oder in einer Fußnote erklären.
Status: behoben – Reihenfolge der Kataloge (aufsteigend, spätere überschreiben frühere) und `x4cat_extract` als Hilfsmodul in Mechanism Punkt 1 erklärt; `[REL]` im Diagramm durch den Pfad ersetzt

**C10** · Abschnitt „validate_mod.py / Mechanism“, Punkt 4, Zitat „because `<effects>` and its children are `xs:all` in Egosoft's schema“ · unverständlich · hoch
Befund: `xs:all` ist ein XML-Schema-Begriff (Kindelemente in beliebiger Reihenfolge, je höchstens einmal). Das erklärt der Text nicht. Ein Leser ohne XSD-Kenntnis versteht weder die Begründung noch die Regel „adding a child that already exists is an error“. Auch „effects“, „pitch“ und „filter“ sind unerklärt und kommen in den aktuellen Varianten nicht vor. Dass die Wertprüfungen (Zeilen 139–148) „leftovers from the engine-effects phase“ sind, ist ohne Projekthistorie unverständlich.
Vorschlag: Umformulieren: „…ein Kindelement, das schon existiert, ist ein Fehler, weil das Schema (`libraries/diff.xsd`) für `<effects>` und seine Kinder jedes Element höchstens einmal erlaubt (`xs:all`).“ Die Pitch- und Filter-Prüfungen als „aktuell ungenutzt, übrig aus einer früheren Projektphase (Kapitel X)“ kennzeichnen.
Status: behoben – `xs:all` erklärt (Schema `libraries/diff.xsd`, jedes Kindelement höchstens einmal); Hinweis auf „leftovers“ blieb unverändert, Kapitelverweis fehlt dem Dokument

**C11** · Abschnitt „Input errors“, letzter Punkt, Zitat „The base file's MD5 is not reported, because `extract` runs with `verbose=False`“ · unklar · gering
Befund: Der Satz nennt nicht, warum der MD5-Wert gebraucht würde (Nachweis, gegen welche Spielversion validiert wurde). Er steht unter „Input errors“, ist aber kein Eingabefehler, sondern eine Eigenschaft der Ausgabe. Der Leser weiß nicht, was er damit anfangen soll.
Vorschlag: In einen passenden Abschnitt verschieben und den Zweck nennen, z. B. „Die MD5-Summe der Basisdatei wird nicht ausgegeben; die geprüfte Spielversion lässt sich daher nur über den Katalognamen nachvollziehen.“
Status: behoben – MD5-Hinweis aus „Input errors“ nach Mechanism Punkt 1 verschoben, Folge ergänzt (Spielversion nur über den Katalognamen erkennbar)

**C12** · Abschnitt „What it catches and what it misses“, Tabelle, Zitat „Features of Egosoft's diff format the project does not use (`pos`, `if`, `silent`, `//` selectors in all forms)“ · unverständlich · mittel
Befund: `pos`, `if` und `silent` sind Diff-Attribute, die nirgends erklärt werden, ebenso wenig, was „in all forms“ bei `//`-Selektoren bedeutet. Für den Leser ist nicht erkennbar, was hier ungeprüft bleibt. Außerdem bleibt offen, ob „Missed“ heißt, dass die Validierung bei diesen Features falsch positiv oder gar nicht reagiert.
Vorschlag: Kurz erklären, was die Attribute tun, und das Verhalten nennen, z. B. „…werden nicht unterstützt; die Validierung meldet bei Einsatz einen Fehler / ignoriert sie“. Nicht Geprüftes konkret nennen.
Status: offen – Ersteller – Verhalten des Validators bei `pos`, `if`, `silent` und `//`-Selektoren (Fehler, Warnung oder ignoriert) ist im Dokument nicht belegt

**C13** · Abschnitt „Traced example“, Zitate „is3d=0 noocclusion=true“, „effects: KEINE“, „Gesamt: 0 Fehler“ · unverständlich · mittel
Befund: Die Ausgabe des Validators ist deutsch („KEINE“, „Gesamt“, „Fehler“, auch „FEHLER“ weiter oben), das Kapitel ist englisch. Das wird nicht erklärt. `is3d` und `noocclusion` werden nicht erklärt, ebenso wenig, ob die gezeigten Werte (`is3d=0`, `noocclusion=true`) das gewünschte Ergebnis sind oder nur ein beliebiges. Der Absatz ist ein langer Satz mit Semikolons; ein Leser kann nicht erkennen, woran er Erfolg erkennt.
Vorschlag: Die Ausgabe als Codeblock zeigen. Dazu erklären, welche Werte erwartet werden und was `is3d` und `noocclusion` bedeuten. Hinweis ergänzen, dass die Meldungen deutsch sind.
Status: offen – Ersteller – Hinweis auf deutsche Validator-Meldungen ergänzt; fehlt: Bedeutung von `is3d`/`noocclusion`, erwartete Werte und die genaue Ausgabe für einen Codeblock

**C14** · Abschnitt „Operations“, Zitat „Validation is mandatory before every install and after every game patch“ · unklar · mittel
Befund: „mandatory“ wird nicht begründet und nicht durchgesetzt. Offen bleibt, ob `init.sh` die Validierung erzwingt, was „install“ heißt (Kopieren nach `extensions/`?) und wer die Pflicht festlegt. Die Anleitung enthält keine konkreten Schritte, etwa den Aufruf mit Pfad oder den Umgang mit einem Fehler.
Vorschlag: Konkret machen: „Vor dem Kopieren von `dist/<id>` ins Spielverzeichnis und nach jedem Spiel-Patch `./init.sh` ausführen; bei Exit-Code 1 nicht installieren.“
Status: offen – Ersteller – unbekannt, ob `init.sh` die Validierung erzwingt, was „install“ konkret heißt und wer die Pflicht festlegt

**C15** · Abschnitt „Open questions“, Zitat „documented only by `libraries/diff.xsd`“ · unklar · gering
Befund: Der Pfad `libraries/diff.xsd` ist nicht verortet (im Spielverzeichnis oder in den Katalogen?). Der Satz „the validator mirrors the observed behaviour, not a specification“ benennt weder das beobachtete Verhalten noch die Stellen, an denen der Validator von der Spezifikation abweichen könnte.
Vorschlag: Ergänzen: „(liegt in den Spielkatalogen, nicht im Repository)“. Außerdem ein bis zwei Beispiele für beobachtetes, aber nicht spezifiziertes Verhalten nennen, etwa „No matching node“ führt zum Überspringen der Operation.
Status: offen – Ersteller – Ablageort von `libraries/diff.xsd` und konkrete Beispiele für beobachtetes, nicht spezifiziertes Verhalten fehlen

### Stufe 3 – Abschlussvermerk des Erstellers
- Ergebnis: stimmig nach Korrekturen
- Korrekturen des Erstellers:
  - A2: Beleg ergänzt (`docs/phase0-findings.md:45`, Log über `-logfile debuglog.txt` laut README); die einschränkende Klammer „only when started with `-logfile`“ entfernt. Endstand behoben.
  - A3/C6: „modified“-Markierung erklärt (Erfolge und Ventures, `README.md:7`) und als Egosoft-Regel für unsignierte Mods gekennzeichnet, nicht als eigener Test; 44/49 als X4-Sprach-IDs erklärt. Endstand behoben.
  - A4/B5: Behauptung abgeschwächt: Die Extension fehlt in der Liste (README, Troubleshooting), eine Meldung im Spiel wurde nicht beobachtet. Endstand behoben.
  - A5: Prüfstand ergänzt (X4 9.00, sieben DLCs, `docs/phase0-findings.md:20`) und Verweis auf Kapitel 9. Endstand behoben.
  - B2: Am Code geprüft: Die Kopie entsteht zu Beginn von `validate` (`:58`), vor der content.xml-Prüfung; Punkt 4 entsprechend formuliert. Endstand behoben.
  - B4 (Restfrage): Meldung des Validators bei kaputtem XML („nicht wohlgeformt“, `:68-75`) und bei kaputtem Selektor ergänzt. Endstand behoben.
  - B6/C13: Am Code geprüft: eine Zeile je berührter ID, dedupliziert (`:151`), also sechs Zeilen; Ausgabe als Codeblock mit Erfolgskriterien und Übersetzung der deutschen Meldungen. Endstand behoben.
  - C3: Konfigurationsdatei, Variant-Key, `id` und `audio_variant` erklärt. Endstand behoben.
  - C4: Voice-Seite 10201, die sechs IDs und der fehlende Sprachsuffix erklärt. Endstand behoben.
  - C12: Am Code geprüft: `pos`, `if`, `silent` werden nie gelesen und ignoriert; `//` wird unverändert an ElementTree gereicht (`:47-48`). Endstand behoben.
  - C14: Pflicht belegt (`CLAUDE.md:32`), dass nichts sie erzwingt, und konkrete Regel (bei Exit-Code 1 nicht installieren). Endstand behoben.
  - C15: Ablageort von `diff.xsd` (Spielkataloge) und ein Beispiel beobachteten Verhaltens ergänzt. Endstand behoben.
- Für den Nutzer offen: keine
- Abgeschlossen: 2026-10-25 17:41
