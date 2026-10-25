# Review: 08-installing-and-releasing.md

## Durchgang 1 – 2026-10-25 17:41
- Dokument: C:\#repos\github\x4mod_less_annoying_voices\book\08-installing-and-releasing.md
- Anlass: neu

### Stufe 1 – Befunde
#### Prüfer A – fachliche Richtigkeit
Fachgebiet: Modding von X4: Foundations (Installer-Skript, Steam-Workshop- und ModDB-Veröffentlichung) · Zielgruppe: Entwickler und Betreuer des Mods, Python- und Windows-Kenntnisse vorausgesetzt, Einsteiger in das Release-Verfahren (abgeleitet)

**A1** · Abschnitt „Legal and „modified““, 1. Satz („Any unsigned extension marks the game as modified (no achievements, no Ventures, sticky on saves)“) · sachlicher Fehler · mittel
Befund: Die Klammer nennt „no achievements“ als Folge eines modifizierten Spiels. Forenberichte von Spielern (Steam-Community-Diskussionen zu X4, https://steamcommunity.com/app/392160/discussions/0/2269194717053088520 und https://steamcommunity.com/app/392160/discussions/0/3757726349613527161) sagen, dass Achievements mit Mods weiter vergeben werden. Das sind Nutzerberichte, keine offizielle Quelle, ich konnte die Aussage nicht abschließend verifizieren. Die Ventures sind laut Egosoft-Wiki seit Version 4.0 für alle Spiele deaktiviert (Seite „X4 Foundations Feature Development Overview“, https://wiki.egosoft.com/X4%20Foundations%20Wiki/Game%20Updates%20and%20Patch%20History/X4%20Foundations%20Feature%20Development%20Overview), nicht erst durch Mods. Die Aussage ist daher unbelegt bis irreführend. Der Hinweis „sticky on saves“ wird dagegen von Nutzerberichten gestützt. Die Einschränkung „unsigned“ fand ich nicht belegt.
Vorschlag: Die Klammer anhand einer Egosoft-Primärquelle prüfen (Spielversion, Steam-Achievements, Multiverse/Ventures) und entweder belegen oder vorsichtig formulieren, etwa „Mods markieren das Spiel als modifiziert; Folgen für Achievements und Online-Funktionen hängen von der Spielversion ab (nicht verifiziert)“.
Status: behoben – Klammer „no achievements, no Ventures“ gestrichen; neu: Modified-Flag bleibt an Spielständen, Folgen für Achievements/Online-Funktionen hängen von der Spielversion ab und sind nicht verifiziert

**A2** · Abschnitt „Steam Workshop“, Liste „Observed behaviour of the tool“, Punkte 3 bis 5 („`-namedesc up`“, „`-minor`“, „`-changenote`“, „`sync="false"`“, „Steam error 16“, „error 9“) · unklar · gering
Befund: Ich konnte die Schalter `-namedesc`, `-minor` und `-changenote` sowie das Attribut `sync="false"` und die Steam-Fehlercodes 16 und 9 nicht verifizieren. Die Suche ergab nur `publishx4`, `-path`, `-preview` und `-buildcat` (Egosoft-Wiki, Forum https://forum.egosoft.com/viewtopic.php?p=4768514). Alles hängt allein an `docs/RELEASE.md`. Die Stelle `sync="false"` ist zudem als „inference“ gekennzeichnet und im selben Satz als dokumentiert dargestellt, was widersprüchlich wirkt.
Vorschlag: Die Schalter mit der Ausgabe von `WorkshopTool.exe` (ohne Argumente aufgerufen) abgleichen und im Text klar trennen zwischen „vom Tool dokumentiert“ und „selbst beobachtet“. Die `sync="false"`-Angabe entweder belegen oder streichen.
Status: offen – Ersteller – Abgleich der Schalter (-namedesc, -minor, -changenote) und der Steam-Fehlercodes 16/9 mit der Ausgabe von WorkshopTool.exe fehlt (nicht aus dem Dokument belegbar); sync="false" siehe B5; Fehlercodes sind im Text nun als reine Kennungen gekennzeichnet (siehe C11)

**A3** · Abschnitt „Legal and „modified““, 2. bis 3. Satz („Free distribution as a mod is the common, tolerated practice; selling it is not possible without Egosoft“) · unklar · gering
Befund: Die rechtliche Aussage zu Duldung der freien Verbreitung, zur Nutzung bearbeiteter Egosoft-Aufnahmen und zu KI-Sprachsynthese aus Egosoft-Texten wird ohne Quelle als Tatsache dargestellt, nur mit Verweis auf interne Dokumente. Ob Egosofts Nutzungsbedingungen das so hergeben, konnte ich nicht verifizieren.
Vorschlag: Die einschlägige Egosoft-Regelung (Modding-/Urheberrechtsbedingungen) mit Titel und URL nennen oder die Aussage als Einschätzung des Autors kennzeichnen.
Status: behoben – „in the author's assessment“ ergänzt, damit die Duldung der freien Verbreitung als Einschätzung des Autors gekennzeichnet ist; eine Egosoft-Quelle mit Titel/URL kann ich nicht benennen

#### Prüfer B – Logik und Zahlen
Fachgebiet: Softwaredokumentation, Python-Installer und Release-Prozess für eine X4-Mod (Steam Workshop, ModDB) · Zielgruppe: Entwickler und Maintainer des Projekts, die den Quellcode und die Release-Abläufe verstehen müssen (abgeleitet)
**B1** · Abschnitt „Gotchas“, 1. Punkt („Removal happens before the audio check. If the audio folder is empty …“) · Logikfehler · mittel
Befund: Laut Flussdiagramm erfolgt auch die Prüfung „dist/id exists?“ (Exit E3) erst nach dem Löschen aller `bosota_*`-Ordner. Der Gotcha nennt nur den leeren Audio-Ordner. Ein fehlendes `dist/<id>/` hat dieselbe Folge: Die zuvor installierte Variante ist weg, der Installer bricht ab. Die Unvollständigkeit zeigt sich auch daran, dass „Post“ und das Diagramm „checking for audio before anything is copied“ als Schutz darstellen, obwohl nichts davor geschützt wird, dass bereits gelöscht wurde.
Vorschlag: Den Gotcha auf beide Abbrüche erweitern: „Removal happens before the dist and audio checks (E3/E4); if either fails, the previously installed variant is already gone.“
Status: behoben – Gotcha 1 erweitert: Removal vor den dist- und Audio-Prüfungen (E3/E4), bei jedem Abbruch ist die alte Variante schon gelöscht

**B2** · Abschnitt „Gotchas“, 2. und 3. Punkt („`ws_*` folders are not removed“ / „Installing over an existing folder crashes“) · Logikfehler · mittel
Befund: Der 2. Punkt zählt „an earlier staging run“ als Ursache für einen `extensions/ws_<n>/`-Ordner, der das lokale `bosota_*`-Install „coexists with the subscribed item“. Ein Staging-Lauf legt den Ordner aber unter `build/workshop/stage2/extensions/` an, nicht im Spielordner. Dort kann er nicht mit einem abonnierten Item koexistieren. Die Koexistenz-Aussage gilt nur für das Abo und für lokale `ws_`-Installs im Spielordner. Außerdem sagt der 3. Punkt, ein lokales Install „while the Workshop item is subscribed“ scheitere. Das gilt nur für `ws_*`-Varianten, im 2. Punkt aber wird ein `bosota_*`-Install als koexistierend beschrieben. Das wirkt wie ein Widerspruch, solange nicht dasteht, welche Variantenart gemeint ist.
Vorschlag: Die Fälle trennen: Abo und lokaler `ws_`-Install im Spielordner führen zu Koexistenz bzw. `FileExistsError`; Staging-Läufe betreffen nur `build/workshop/stage2/extensions/`. Dazu jeweils angeben, ob eine `bosota_*`- oder eine `ws_*`-Variante installiert wird.
Status: behoben – Gotchas 2 und 3 getrennt nach Fall: Abo/lokaler ws_-Install im Spielordner (Koexistenz), Staging-Lauf nur unter build/workshop/stage2/ (blockiert den nächsten Lauf); in Gotcha 3 „local ws_* install“ statt „local install“

**B3** · Abschnitt „Gotchas“, 5. Punkt („It deletes any folder named `bosota_*` … (`:92-94`)“) · Logikfehler · gering
Befund: Im Abschnitt „Mechanism“ und bei „Removal“ wird der Löschblock als `:92-95` angegeben, in „Gotchas“ als `:92-94`. Die Zeilenverweise sind uneinheitlich.
Vorschlag: Beide Stellen auf denselben, geprüften Zeilenbereich bringen.
Status: offen – Ersteller – richtiger Zeilenbereich des Löschblocks (:92-94 oder :92-95) lässt sich ohne Blick in tools/install_mod.py nicht klären

**B4** · Abschnitt „Steam Workshop“, Aufzählung 1. Punkt („Only `.cat/.dat/.cur/.mkv/.txt/.pdf` are uploaded“) gegenüber dem Absatz davor („packed as `content.xml` + `ext_01.cat` + `ext_01.dat`“) · unklar · mittel
Befund: `.xml` steht nicht in der Liste der hochgeladenen Dateitypen. Das Item enthält aber `content.xml`, und mehrere Punkte verlangen eine geänderte `content.xml` (`version`, `-namedesc`, `ws_`-Id). Es bleibt offen, wie `content.xml` ins Item gelangt. Möglich wäre, dass das Tool sie gesondert behandelt oder dass die Liste unvollständig ist.
Vorschlag: Ergänzen, dass `content.xml` vom Tool separat behandelt wird, oder die Liste korrigieren. Falls unklar, die Stelle in `docs/RELEASE.md` prüfen und als nicht verifiziert kennzeichnen.
Status: behoben – als nicht verifiziert gekennzeichnet: „How content.xml itself gets into the item is not recorded here (not verified)“; Dateityp-Liste unverändert

**B5** · Abschnitt „Steam Workshop“, letzter Aufzählungspunkt („the tool's documentation also mentions a `sync="false"` attribute (inference: not recorded in the repository)“) · unklar · gering
Befund: Der Satz widerspricht sich. Die Dokumentation des Tools „erwähnt“ das Attribut, zugleich wird es als „inference“ (Schlussfolgerung) bezeichnet und als im Repository nicht belegt. Es ist unklar, ob es eine belegte Tatsache oder eine Vermutung ist, und was das Attribut bewirkt.
Vorschlag: Entweder mit Quellenangabe belegen und die Wirkung nennen oder den Halbsatz streichen oder als „unverified“ kennzeichnen.
Status: behoben – Halbsatz zu sync="false" als unverifizierte Notiz umformuliert, Ort und Wirkung als nicht im Repository belegt gekennzeichnet

**B6** · Abschnitt „Steam Workshop“, letzter Punkt („uploads happen from staging copies under `build/workshop/`“) gegenüber Abschnitt „`release/` and modpub“ („`release/out/workshop/<lang>/` holds modpub's upload copies“ und „Workshop item numbers and staging paths (`release/mod.yaml:39-43`)“) · Logikfehler · mittel
Befund: Es werden zwei verschiedene Orte für Upload-Kopien genannt (`build/workshop/…` und `release/out/workshop/<lang>/`). Das Dokument erklärt nicht, wie sie sich zueinander verhalten. Das Manifest führt zudem „staging paths“, ohne dass klar ist, auf welchen der beiden Orte sie zeigen. Der Leser kann nicht erkennen, ob „never from `dist/`“ auch für modpub gilt und welcher Ort für welchen Weg (manuell oder modpub) maßgeblich ist.
Vorschlag: Ausdrücklich festhalten: manueller Upload über `build/workshop/stage2/`, modpub-Upload über `release/out/workshop/<lang>/`. Ergänzen, auf welchen Pfad die „staging paths“ in `mod.yaml` zeigen.
Status: offen – Ersteller – unklar, auf welchen Pfad (build/workshop/ oder release/out/workshop/<lang>/) die „staging paths“ in release/mod.yaml zeigen und ob die Aufteilung manuell/modpub zutrifft

**B7** · Abschnitt „Steam Workshop“, 1. Absatz („The configuration holds versions 102 and 101; the modpub upload of 2026-10-24 pushed 103 and 102“) · unklar · gering
Befund: Die Reihenfolge der beiden Item-Paare ist nicht ausdrücklich zugeordnet. Die Versionspaare ergeben nur implizit und in der Reihenfolge der Items DE=102→103 und EN=101→102, und das ist nicht gesagt. Dass die Konfiguration niedrigere Versionen hält als hochgeladen, ist ein Zustandsunterschied, dessen Folge für den nächsten Upload (Versionsabgleich) nicht benannt wird. Ein Leser muss die Zuordnung raten.
Vorschlag: Explizit schreiben: „DE (3824406333): Konfiguration 102, hochgeladen 103; EN (3824446410): Konfiguration 101, hochgeladen 102“, und ergänzen, ob die Konfiguration nachgezogen werden muss.
Status: behoben – Versionen den Items zugeordnet (DE 102→103, EN 101→102, Zuordnung per Reihenfolge und +1-Muster erschlossen) und festgehalten, dass die Konfiguration um eine Version hinterherhinkt; ob sie nachgezogen werden muss, bleibt dem Ersteller überlassen

**B8** · Abschnitt „Contract“, Zeile „`python -I tools/install_mod.py <variant key> [--game-dir <X4>] [--force]` or `--remove`“ · unklar · gering
Befund: Die Syntax lässt offen, ob `--remove` den `<variant key>` ersetzt oder zusätzlich angegeben wird, und ob `--game-dir` und `--force` damit kombinierbar sind. Laut Flussdiagramm laufen Prüfung von `extensions/`, Laufzeit-Guard und Löschen auch bei `--remove`, `dist` und Audio aber nicht. Die Pre-Bedingungen gelten daher nicht unterschiedslos.
Vorschlag: Die Syntax als zwei Formen angeben, z. B. `install_mod.py <variant key> [...]` und `install_mod.py --remove [--game-dir …] [--force]`. Außerdem vermerken, dass die Pre-Bedingungen zu `dist` und Audio bei `--remove` entfallen.
Status: behoben – Contract-Zeile in Install- und Remove-Form getrennt, Pre-Bedingungen zu dist/Audio auf „when installing“ eingeschränkt

#### Prüfer C – Verständlichkeit
Fachgebiet: Softwareentwicklung/Mod-Betrieb (X4-Mod, Installer-Skript, Steam-Workshop- und ModDB-Veröffentlichung) · Zielgruppe: Entwickler oder Maintainer des Mod-Repositorys, vermutlich der Autor selbst oder Mitwirkende ohne Vorkenntnis der Projektinterna (abgeleitet)

**C1** · Abschnitt „install_mod.py“ > „Contract“, erste Zeile („`python -I tools/install_mod.py <variant key> [--game-dir <X4>] [--force]` or `--remove`“) · unklar · mittel
Befund: Es ist nicht erkennbar, ob `--remove` zusätzlich zum `<variant key>` oder an dessen Stelle steht und ob dann `--game-dir` und `--force` gelten. Das Ablaufdiagramm zeigt, dass `--remove` erst nach dem Löschen geprüft wird, also ohne Variante auskommen müsste. Die Option `-I` wird nicht erklärt (isolierter Python-Modus).
Vorschlag: Zwei Aufrufformen getrennt angeben, z. B. „Installieren: `python -I tools/install_mod.py <variant key> [--game-dir <X4>] [--force]`“ und „Entfernen: `python -I tools/install_mod.py --remove [--game-dir <X4>] [--force]`“. Dahinter in einem Halbsatz erklären, was `-I` bewirkt.
Status: behoben – Aufrufformen getrennt (Install; --remove mit Hinweis, welche Prüfungen entfallen) und -I (isolierter Modus) erklärt

**C2** · Abschnitt „Contract“, Stichpunkte „Pre“ und „Post“ („`dist/<id>/`“, „`build/audio/<audio_variant>/`“, „<variant key>“) · unverständlich · mittel
Befund: Die Begriffe `variant key`, `<id>`, `audio_variant` und `<line id>` werden in diesem Kapitel nicht definiert. Der Leser erfährt nicht, wie sie zusammenhängen, ob also der Variantenschlüssel die id ergibt, und auch nicht, woher die `.ogg`-Dateien stammen. Nur der Verweis auf Kapitel 4 weiter unten deutet an, wo das steht.
Vorschlag: Am Kapitelanfang oder im Contract in zwei Sätzen erklären, was `variant key`, `id` und `audio_variant` sind, mit einem Beispiel (z. B. `bosota_voice_will_de`), und auf Kapitel 4 verweisen.
Status: behoben – im Contract ergänzt: variant key (config/variants.json, ch. 4), id (Modordnername, Beispiel bosota_voice_will_de / ws_<number>), audio_variant (Ordner unter build/audio/), line id; Herkunft der .ogg-Dateien steht nicht im Dokument (siehe C3)

**C3** · Abschnitt „Mechanism“, Mermaid-Diagramm, Knoten E4 („exit: run the audio recipe“) · unverständlich · mittel
Befund: „audio recipe“ wird nirgends erklärt oder verlinkt. Der Leser weiß nicht, welchen Befehl oder welche Anleitung er ausführen soll, wenn der Ordner keine `.ogg`-Dateien enthält. Bei E3 steht dagegen mit `build_mod.py` ein konkretes Skript.
Vorschlag: „run the audio recipe“ durch das konkrete Skript oder Kapitel ersetzen, z. B. „exit: generate audio first (see ch. X)“.
Status: offen – Ersteller – fehlt: welches Skript bzw. Kapitel die Audio-Erzeugung beschreibt („audio recipe“)

**C4** · Abschnitt „Mechanism“, Stichpunkt „Running-game guard“ („X4 reads the diff at start-up; replacing the mod folder underneath a running game leaves the loaded redirect pointing at deleted files, and Boso goes silent“) · unverständlich · mittel
Befund: „diff“ (X4-Diff-Patch) und „redirect“ (Umleitung der Sounddateien) sind Fachbegriffe, die hier nicht erklärt werden. „Boso“ wird im Kapitel nicht eingeführt. Der Begründungssatz, der den Zweck des Guards erklären soll, bleibt deshalb ohne Vorwissen unverständlich.
Vorschlag: Ein bis zwei Sätze zum Mechanismus ergänzen, etwa „X4 lädt die Mod-Anpassungen (diff-Dateien in `libraries/sound_library.xml`, die Sprachaufnahmen auf die Mod-Dateien umleiten) beim Start“. „Boso“ beim ersten Auftreten erklären oder auf das Kapitel verweisen, in dem die Figur eingeführt wird.
Status: behoben – diff (sound_library.xml mit Umleitungen auf die .ogg-Dateien), redirect und Boso (die vom Mod ersetzte Stimme) im Guard-Punkt erklärt

**C5** · Abschnitt „Mechanism“, Stichpunkt „Running-game guard“ („tasklist prints in the OEM code page and decoding as cp1252 crashed“) · unverständlich · gering
Befund: „OEM code page“ und „cp1252“ sind Zeichensatz-Fachbegriffe. Der Zusammenhang, warum die Suche als Bytes erfolgt, bleibt ohne Vorwissen unklar.
Vorschlag: Ergänzen: „(die Windows-Konsole gibt Text in einem anderen Zeichensatz aus als Python erwartet, das Dekodieren schlug mit einem Fehler fehl)“.
Status: behoben – OEM code page in Klammern als Zeichensatz der Konsole erläutert, der nicht dem von Python verwendeten entspricht

**C6** · Abschnitt „Gotchas“, Stichpunkt „`ws_*` folders are not removed“ („a local `install_mod.py alien_ws`, or an earlier staging run“) und Stichpunkt „Installing over an existing folder crashes“ („`build/workshop/stage2/extensions/ws_<n>`“) · unverständlich · mittel
Befund: `alien_ws` ist ein Variantenschlüssel, der nicht eingeführt wird. „staging run“ und „stage2“ (ein Zwischenordner, aus dem das Workshop-Werkzeug hochlädt) werden erst im Workshop-Abschnitt andeutungsweise genannt, nie definiert. Der Leser kann nicht erkennen, wann und wie ein „staging run“ stattfindet, obwohl sich der Fehler gerade dort wiederholt. Auch warum „stage2“ und ob es „stage1“ gibt, bleibt offen.
Vorschlag: Vor den Gotchas oder im Workshop-Abschnitt erklären, was Staging ist (Ordner `build/workshop/<stage>/`, Aufruf mit welchem Variantenschlüssel) und welche Workshop-Varianten es gibt (z. B. `alien_ws`, ... aus `config/variants.json`).
Status: behoben – alien_ws als ws_*-Workshop-Variante (ch. 4) benannt und Staging-Lauf definiert (Workshop-Variante nach build/workshop/stage2/ installieren, um die Upload-Kopie zu erzeugen); ob es ein stage1 gibt und die Liste der Workshop-Varianten stehen nicht im Dokument und sind nicht ergänzt

**C7** · Abschnitt „Gotchas“, Stichpunkt „It deletes any folder named `bosota_*`“ („"Other mods are untouched" holds only by naming convention.“) · unklar · gering
Befund: Das Zitat „Other mods are untouched“ steht an keiner Stelle des Kapitels. Der Leser weiß nicht, woher die Aussage stammt (Skriptausgabe, andere Dokumentation) oder worauf sich „holds“ bezieht.
Vorschlag: Quelle des Zitats nennen (z. B. „der Hinweis in `docs/RELEASE.md`“) oder ohne Anführungszeichen formulieren: „Dass andere Mods unangetastet bleiben, gilt nur, solange deren Ordner nicht mit `bosota_` beginnen.“
Status: behoben – Anführungszeichen entfernt: „That other mods are left untouched holds only by naming convention.“

**C8** · Abschnitt „Steam Workshop“, 1. Absatz („The configuration holds versions 102 and 101; the modpub upload of 2026-10-24 pushed 103 and 102 with its own titles“) · unklar · mittel
Befund: Der Satz hat zwei Probleme. Die Zuordnung der Versionen zu den beiden Items ist nur durch die Reihenfolge angedeutet (102 zum deutschen, 101 zum englischen?). Zudem bleibt unklar, ob die Konfiguration nach dem Upload veraltet ist, welche Version also gilt. „with its own titles“ ist nicht verständlich (modpub setzte eigene Titel, die von `content.xml` abweichen?). Dazu kommt, dass modpub hier erwähnt wird, bevor es im Abschnitt „ModDB and other channels“ erklärt wird.
Vorschlag: Versionen den Items ausdrücklich zuordnen („DE: Konfiguration 102, hochgeladen 103; EN: Konfiguration 101, hochgeladen 102“), sagen, welcher Stand maßgeblich ist, und „modpub“ beim ersten Auftreten kurz erklären („siehe unten“).
Status: behoben – bereits durch B7 behoben (Zuordnung der Versionen, Rückstand der Konfiguration, „with the titles modpub set“, Verweis auf den modpub-Abschnitt)

**C9** · Abschnitt „Steam Workshop“, 1. Absatz („**3824406333** (German, Will voice)“) · unverständlich · gering
Befund: „Will voice“ wird nicht erklärt (Stimme einer Figur, eines Sprechers oder eines TTS-Profils?). Der Begriff taucht nur im ModDB-Paketnamen `bosota_voice_will_de` wieder auf.
Vorschlag: Kurz erläutern, z. B. „German, TTS voice ‚Will‘“, oder auf das Kapitel mit den Varianten verweisen.
Status: behoben – „Will voice“ → „TTS voice "Will"“ (TTS laut Legal-Abschnitt für die deutsche Variante)

**C10** · Abschnitt „Steam Workshop“, 2. Absatz („Either way the redirect contains the folder name, so the uploaded build must have `id = ws_<number>`.“) · unklar · mittel
Befund: „redirect“ wird nicht definiert. Der Leser erkennt nicht, in welcher Datei die Umleitung steht und warum dort der Ordnername vorkommt. Unklar ist auch „the engine resolves the redirect path through the mounted catalog the same way“: Mit „the same way“ ist unklar, womit verglichen wird. Die Gegenüberstellung der beiden Ordnerpfade (Spielordner und `Documents\Egosoft...`) führt außerdem nicht zu einer klaren Aussage, welcher Pfad für Nutzer gilt.
Vorschlag: „redirect“ einmal definieren (z. B. „der Eintrag in `sound_library.xml`, der den Pfad zur `.ogg`-Datei enthält“). Den Satz zum Katalog umformulieren: „Der Pfad bleibt derselbe wie bei losen Dateien, die Engine findet die Datei im gemounteten Katalog.“ Am Ende festhalten, welcher Pfad für Abonnenten gilt.
Status: behoben – redirect definiert (sound_library.xml-Eintrag mit Pfad zur Sprachdatei), Katalog-Satz präzisiert („as it would for loose files“); welcher Pfad für Abonnenten gilt, bleibt wie beobachtet (Spielordner auf dem Rechner des Autors)

**C11** · Abschnitt „Steam Workshop“, Liste „Observed behaviour of the tool“ („`publishx4`“, „`update`“, „`-buildcat`“, „`-preview`“, „`-minor`“, „`-changenote`“, „`-namedesc up`“, „Steam error 16“, „error 9“) · unverständlich · mittel
Befund: Die Befehle und Optionen von `WorkshopTool.exe` werden ohne Erklärung benutzt. Aus dem Kapitel geht nicht hervor, was `publishx4` und `update` tun, wie man sie aufruft und was `-preview`, `-minor` oder `-namedesc up` bewirken. Die Fehlernummern 16 und 9 sind ohne Bedeutung angegeben. Das Kapitel soll aber erklären, wie die Releases entstehen.
Vorschlag: Eine kurze Tabelle oder Liste ergänzen: Befehl/Option, Wirkung, ein beispielhafter Aufruf. Alternativ klar auf den Abschnitt in `docs/RELEASE.md` verweisen. Die Fehlernummern mit einem Halbsatz Bedeutung versehen oder ausdrücklich als „nur Kennung“ kennzeichnen.
Status: behoben – Einleitung der Liste ergänzt: Aufrufsyntax steht in docs/RELEASE.md, publishx4 = neues Item, update = Upload in bestehendes Item, Fehlernummern 16/9 nur Kennungen

**C12** · Abschnitt „Steam Workshop“, Liste, 1. Stichpunkt („Only `.cat/.dat/.cur/.mkv/.txt/.pdf` are uploaded, subfolders are not“) · unklar · mittel
Befund: Mehrdeutig, ob nur der Unterordner selbst oder auch die darin liegenden Dateien nicht hochgeladen werden. Der Zusammenhang mit `-buildcat` bleibt offen: Es wird nicht gesagt, dass die Dateien deshalb im Katalog gebündelt werden müssen und was mit `content.xml` (kein erlaubter Dateityp) geschieht.
Vorschlag: Umformulieren: „Das Werkzeug lädt nur Dateien der Typen … im obersten Ordner hoch, Dateien in Unterordnern werden ignoriert. Deshalb packt `-buildcat` alles in `ext_01.cat/.dat`.“ Dazu ergänzen, wie `content.xml` hochgeladen wird.
Status: behoben – Satz präzisiert („Files of the types … subfolders and their contents are not“) und offene Frage zu content.xml als nicht verifiziert vermerkt (siehe B4)

**C13** · Abschnitt „Steam Workshop“, Liste, letzter Stichpunkt („the tool's documentation also mentions a `sync="false"` attribute (inference: not recorded in the repository)“) · unklar · mittel
Befund: Es wird nicht gesagt, wo das Attribut steht (`content.xml`?) und was es bewirkt. „inference: not recorded in the repository“ lässt offen, was genau gefolgert wurde, und es ist unklar, ob das Attribut für die Praxis relevant ist. Dass der Satz zugleich die Begründung für den Staging-Ablauf liefert, geht dadurch unter.
Vorschlag: Beschreiben, was `sync="false"` laut Werkzeugdokumentation bewirkt, und die Vermutung als solche formulieren („Vermutung, im Repository nicht belegt“). Wenn die Bedeutung unbekannt ist, den Halbsatz streichen.
Status: behoben – bereits durch B5 behoben (Halbsatz als unverifiziert gekennzeichnet; Ort und Wirkung des Attributs sind im Dokument nicht bekannt)

**C14** · Abschnitt „ModDB and other channels“ > „`release/` and modpub“ („`release/assets/` (copies of game audio) and other outputs are not committed (`.gitignore:10-13`)“) · unklar · gering
Befund: „other outputs“ ist unbestimmt. Der Satz davor nennt `release/out/text/*.md` und `release/out/status.json` mit Zeilenverweis, sodass der Leser nicht weiß, ob diese ins Repository gehören oder ebenfalls ausgeschlossen sind. Dass `release/out/workshop/` „ignored by git“ ist, steht davor, `.gitignore:10-13` wird aber erst hier zitiert.
Vorschlag: Aufzählen, welche Unterordner von `release/` versioniert sind und welche nicht, z. B. „versioniert: `release/mod.yaml`, `release/out/text/`, `release/out/status.json`; nicht versioniert: `release/assets/`, `release/out/workshop/`“, sofern das zutrifft (anhand von `.gitignore` prüfen).
Status: offen – Ersteller – fehlt: Inhalt von .gitignore, um aufzuzählen, welche Unterordner von release/ versioniert sind

**C15** · Abschnitt „Legal and „modified““ („no achievements, no Ventures, sticky on saves“) · unverständlich · gering
Befund: „Ventures“ (Mehrspieler-/Online-Funktion von X4) und „sticky on saves“ (der Modified-Status bleibt im Spielstand auch nach Entfernen der Mod) werden nicht erklärt. Die Aussage „Free distribution … is the common, tolerated practice“ ist im Kapitel nicht belegt und nur durch „Details: `docs/RELEASE.md`“ gestützt. Ich konnte sie nicht verifizieren.
Vorschlag: „Ventures“ und „sticky“ in einem Halbsatz erklären. Für die Duldung eine Quelle nennen (Egosoft-Richtlinie oder Forumsaussage) oder die Formulierung als Einschätzung des Autors kennzeichnen.
Status: behoben – bereits durch A1/A3 behoben (Ventures-Erwähnung entfernt, „sticky“ als „flag sticks to saves“ formuliert, Duldung als Einschätzung des Autors gekennzeichnet)

### Stufe 3 – Abschlussvermerk des Erstellers
- Ergebnis: stimmig nach Korrekturen
- Korrekturen des Erstellers:
  - Frage 3 (Verfälschung durch die Überarbeitung): Der neue Contract-Satz „Adding `--remove` …“ und die `-I`-Erklärung („environment variables … are not used“) waren falsch. Ersetzt durch zwei getrennte Aufrufformen (Variante bei `--remove` optional, `tools/install_mod.py:78,83-84`) und die korrekte `-I`-Beschreibung. B8/C1 bleiben behoben.
  - A1/C15: Die vage Ersatzformulierung des Überarbeiters durch den recherchierten Stand ersetzt: Flag bleibt an Spielständen, Ventures gesperrt (von Egosoft ohnehin abgeschaltet), Erfolge laut Spielerberichten weiter möglich, nicht getestet; Hinweis, dass die Nutzertexte des Projekts noch das Gegenteil behaupten. Endstand behoben.
  - A2: Die Herkunft der Schalter und Fehlercodes ist jetzt klar als eigene Beobachtung aus `docs/RELEASE.md` gekennzeichnet, nicht mit der Hilfe des Tools abgeglichen. Endstand behoben.
  - B3: Am Code geprüft, der Löschblock ist `:92-95`; die abweichende Angabe angeglichen. Endstand behoben.
  - B6: Staging-Pfade aus `release/mod.yaml:41-43` gelesen (`build/workshop/stage2` und `stage2_en`) und die zwei Ebenen erklärt (manueller Upload direkt daraus, modpub kopiert nach `release/out/workshop/<lang>/`). Endstand behoben.
  - C3: E4 auf `audio_recipe` in `config/variants.json` bezogen, mit Verweis auf Kapitel 6 und 7. Endstand behoben.
  - C6 (Rest): Staging-Aufruf mit `--game-dir` und beide Staging-Ordner genannt (es gibt `stage2` und `stage2_en`, kein „stage1“ im Gebrauch). Bleibt behoben.
  - C14: `.gitignore:10-13` gelesen und aufgezählt, was versioniert ist und was nicht. Endstand behoben.
- Für den Nutzer offen:
  - A1: `README.md`, `docs/HOW-IT-WORKS.md`, `docs/release/MODDB_DESCRIPTION.md` und die Release-Texte in `release/out/text/` (Workshop, ModDB, Reddit, YouTube) behaupten noch, Mods kosteten die Steam-Erfolge. Sollen diese Texte korrigiert werden, auch die bereits auf die (privaten) Workshop-Seiten hochgeladenen?
- Abgeschlossen: 2026-10-25 17:46
