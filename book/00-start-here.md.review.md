# Review: 00-start-here.md

## Durchgang 1 – 2026-10-25 17:22
- Dokument: C:\#repos\github\x4mod_less_annoying_voices\book\00-start-here.md
- Anlass: neu

### Stufe 1 – Befunde
#### Prüfer A – fachliche Richtigkeit
Fachgebiet: Modding von X4: Foundations (Sprachausgabe-Austausch, Audioverarbeitung, Build-Pipeline in Python/PowerShell) · Zielgruppe: Entwickler und Maintainer des Mod-Repositories, die es bauen, anpassen oder erweitern wollen (abgeleitet)

**A1** · Abschnitt „Run it locally“, Absatz nach dem Codeblock („`-I` runs Python in isolated mode (no environment variables, no user site packages)“) · sachlicher Fehler · mittel
Befund: Der Schalter `-I` ignoriert nur die PYTHON*-Umgebungsvariablen (er impliziert `-E` und `-s`, ab Python 3.11 auch `-P`). Umgebungsvariablen wie `X4_GAME_DIR` (im Abschnitt „Prerequisites“ genannt) bleiben für das Skript über `os.environ` lesbar. Die Aussage „no environment variables“ ist daher falsch und kann Leser glauben lassen, `X4_GAME_DIR` wirke bei `-I` nicht. Quelle: Python-Dokumentation, „Command line and environment“, Option `-I`, https://docs.python.org/3/using/cmdline.html.
Vorschlag: Ersetzen durch „`-I` runs Python in isolated mode (ignores `PYTHON*` environment variables, the user site-packages directory and the script directory on `sys.path`; ordinary variables such as `X4_GAME_DIR` are still read)“.
Status: behoben – Satz zu `-I` ersetzt: ignoriert nur `PYTHON*`-Variablen und User-site-packages, kein Skriptverzeichnis in `sys.path`; gewöhnliche Variablen wie `X4_GAME_DIR` werden weiter gelesen (jetzt als Aufzählungspunkt)

**A2** · Abschnitt „Your first change“, Überschrift „Make the English variant 2 dB quieter“ und Befehl „--gain-db 2“ · unklar · hoch
Befund: Der Parameter `--gain-db 2` steht für eine Pegelanhebung um 2 dB, sofern er wie üblich ein Verstärkungswert ist. Das Beispiel soll die Variante aber leiser machen. Das Dokument sagt nicht, welcher Gain-Wert die bestehende Variante `alien_mid_50` hat und ob `--gain-db` absolut oder relativ zur Normalisierung gilt. Auch der Name `alien_mid_50_g2` gibt keinen Hinweis auf „leiser“. Ein Leser, der den Befehl übernimmt, erhält eventuell eine lautere Variante. Ich konnte das Verhalten von `--gain-db` nicht verifizieren, weil ich nur dieses Dokument lesen durfte.
Vorschlag: Den aktuellen Gain-Wert der Variante nennen und einen Zielwert angeben, der 2 dB darunter liegt (zum Beispiel „bisher --gain-db N, neu N-2“). Alternativ erklären, dass `--gain-db` ein absoluter Wert nach der Normalisierung ist, und das Beispiel auf einen negativen oder kleineren Wert abstimmen.
Status: offen – Ersteller – fehlt: aktueller Gain-Wert von `alien_mid_50` und ob `--gain-db` absolut oder relativ wirkt (und damit der Wert, der um 2 dB leiser ergibt); Dokument an dieser Stelle unverändert

**A3** · Abschnitt „What is this?“, Aufzählung („German track“ mit „2,324 German lines“ und „English track“ mit „1,750 original English recordings“) · unklar · gering
Befund: Die Zeilenzahlen 2,324 und 1,750 sind Faktenangaben zu den Spieldaten von Version 9.00 und werden nicht belegt. Ich konnte sie nicht verifizieren. Der Unterschied zwischen den beiden Sprachen wird nicht erklärt. Da die deutschen Zeilen aus den Spieltexten neu gesprochen werden, ist die Zahl plausibel. Warum es im Englischen weniger Aufnahmen gibt, bleibt offen.
Vorschlag: Die Zahlen mit Stand und Fundstelle versehen (zum Beispiel „Stand X4 9.00, ermittelt mit tools/x4cat_extract.py“) und die Abweichung in einem Halbsatz erklären oder auf das Kapitel verweisen, das sie behandelt.
Status: offen – Ersteller – fehlt: Fundstelle der Zeilenzahlen 2,324 und 1,750 sowie der Grund, warum die englische Zahl kleiner ist; Version 9.00 steht bereits im ersten Satz des Abschnitts

**A4** · Abschnitt „Run it locally“, Kommentar zu Schritt 1 („catalog 03 holds all of them in 9.00“) und Absatz nach dem Codeblock („The text files (`t/0001-l0XX.xml`) are in `09.cat`“) · unklar · gering
Befund: Die Zuordnung der Pfade zu den Katalogdateien 03.cat und 09.cat ist versionsabhängig und kann sich mit Patches ändern. Das Dokument weist selbst darauf hin, dass man den Katalog nach einem Patch neu suchen muss. Beide Angaben sind nur für Version 9.00 formuliert, und ich konnte sie ohne Spieldateien nicht verifizieren. Außerdem passt der Sprachcode „l0XX“ nicht zum sonst verwendeten Muster „l049“ und „l044“, denn er ist nirgends als Platzhalter für die Sprach-ID erklärt.
Vorschlag: Ergänzen „(verified for 9.00; after a patch use the Select-String search below)“ und „l0XX“ einmal erläutern („l049 = German, l044 = English“).
Status: behoben – „(the catalog numbers above are verified for 9.00)“ und „in 9.00“ bei `09.cat` ergänzt, Hinweis auf die Select-String-Suche nach Patches; Legende ergänzt: `l049` = Deutsch, `l044` = Englisch, `l0XX` steht für beide

#### Prüfer B – Logik und Zahlen
Fachgebiet: Softwaredokumentation, Build-Pipeline einer X4-Foundations-Voice-Mod (Python, ffmpeg, XML-Diff-Patching) · Zielgruppe: Entwickler und Maintainer, die das Repository neu bauen oder erweitern wollen (abgeleitet)
**B1** · Abschnitt „Run it locally“, Schritt 2 und 3 („--variant d12_alien_mid --gain-db 9“, „install_mod.py alien“) und Abschnitt „What is this?“ („German track: … by an ElevenLabs text-to-speech voice“) · Logikfehler · mittel
Befund: Der veröffentlichte deutsche Track wird als ElevenLabs-Sprachsynthese beschrieben. Das Beispiel erzeugt dagegen die deutsche Variante „d12_alien_mid“ per Filterkette aus den Originalaufnahmen, als „no-account German variant“. Schritt 3 installiert die Variante `alien`. Es ist nirgends belegt, dass `alien` dieselbe Variante ist wie das in Schritt 2 erzeugte Audio `d12_alien_mid_g9`. Es ist auch nicht gesagt, dass diese Variante nicht der veröffentlichte deutsche Track ist. Der Leser kann nicht prüfen, ob die Schritte 1 bis 3 zusammenpassen.
Vorschlag: Ausdrücklich schreiben, welcher `audio_variant` in `config/variants.json` zur Variante `alien` gehört, und klarstellen, dass das Beispiel nicht der veröffentlichte (TTS-)Track ist. Alternativ ein Beispiel wählen, dessen Variante und Audioordner zusammenpassen.
Status: offen – Ersteller – fehlt: welcher `audio_variant` in `config/variants.json` zur Variante `alien` gehört und ob `d12_alien_mid_g9` dazu passt bzw. der veröffentlichte Track ist; ergänzt wurde nur, dass das Beispiel in Schritt 2 gefilterte Originale statt Text-to-Speech nutzt

**B2** · Abschnitt „Your first change“ („Make the English variant 2 dB quieter“ und „--gain-db 2“) · Logikfehler · hoch
Befund: Die Aufgabe lautet „2 dB leiser“, der Befehl übergibt aber `--gain-db 2`. Ein positiver Wert bedeutet üblicherweise lauter. Im Beispiel davor steht `--gain-db 9` als Anhebung. Das Dokument nennt weder den bisherigen Pegel der Variante `alien_mid_50` noch, ob `--gain-db` absolut oder relativ ist. Der Leser kann nicht ableiten, dass 2 den Pegel um 2 dB senkt. Ohne diese Angabe gibt der Befehl womöglich das Gegenteil des Ziels aus.
Vorschlag: Den aktuellen Gain-Wert von `alien_mid_50` nennen und angeben, ob `--gain-db` absolut oder relativ wirkt. Dann den Wert so wählen, dass er 2 dB leiser ergibt, zum Beispiel „bisher 4 → jetzt 2“ oder bei relativer Wirkung `-2`. Den Ordnernamen `_g2` darauf abstimmen.
Status: offen – Ersteller – fehlt: aktueller Gain-Wert von `alien_mid_50` und ob `--gain-db` absolut oder relativ wirkt; siehe A2

**B3** · Abschnitt „Run it locally“, Absatz nach dem Codeblock („`-I` runs Python in isolated mode (no environment variables, no user site packages)“) · sachlicher Fehler · mittel
Befund: Der Schalter `-I` ignoriert nur die `PYTHON*`-Umgebungsvariablen (er entspricht `-E -s` und entfernt außerdem das Skriptverzeichnis aus `sys.path`). Andere Umgebungsvariablen bleiben erhalten. „No environment variables“ ist daher falsch. Es widerspricht außerdem dem Hinweis „or set `X4_GAME_DIR`“, der nur funktioniert, wenn Variablen weiter gelesen werden. Quelle: Python-Dokumentation, Befehlszeilenoption `-I` (docs.python.org/3/using/cmdline.html#cmdoption-I).
Vorschlag: Ändern in „`-I` runs Python in isolated mode (ignores `PYTHON*` environment variables and the user site-packages, and does not put the script directory on `sys.path`)“.
Status: behoben – bereits durch A1 behoben

**B4** · Abschnitt „Run it locally“, Einleitung („X4 installed at `C:\Steam\steamapps\common\X4 Foundations` (or set `X4_GAME_DIR`)“) und Codeblock · Logikfehler · gering
Befund: Der Text nennt `X4_GAME_DIR` als Alternative zum Standardpfad. Die Befehle in Schritt 1 und im Abschnitt „Your first change“ enthalten den Pfad aber fest einkodiert. Bei einem anderen Installationspfad funktionieren die Beispiele so nicht. Es ist nicht erklärt, was die Variable bewirkt (nur für die Tools, nicht für den Kommandozeilenparameter).
Vorschlag: Ergänzen, dass `X4_GAME_DIR` nur die Tools betrifft (zum Beispiel `build_mod`, `validate_mod`, `install_mod`), und dass der Pfad in Schritt 1 bei anderer Installation von Hand anzupassen ist. Oder im Beispiel `$env:X4_GAME_DIR` verwenden.
Status: behoben – Satz ergänzt, dass die Befehle den Standardpfad ausschreiben und bei anderer Installation dort zu ersetzen sind; welche Tools `X4_GAME_DIR` auswerten, ist nicht belegt und wird nicht behauptet

**B5** · Abschnitt „Where things live“, Tabellenzeile `tools/` („Seven Python command-line tools, one per pipeline step“) · unklar · gering
Befund: Im Kapitel sind sechs Tools genannt: `x4cat_extract.py`, `process_audio.py`, `voice_convert_elevenlabs.py`, `build_mod.py`, `validate_mod.py` und `install_mod.py`. Ein siebtes Tool kommt nicht vor. Die Zahl „sieben, eins pro Pipeline-Schritt“ lässt sich daher nicht nachvollziehen. Ich konnte sie nicht verifizieren. Außerdem erzeugen zwei Tools (Filterkette und TTS) alternativ dasselbe Zwischenprodukt, sodass „eins pro Schritt“ nicht stimmig ist.
Vorschlag: Die Zahl gegen das Verzeichnis `tools/` prüfen und das fehlende Tool nennen. Alternativ „Python command-line tools“ ohne Zahl schreiben.
Status: offen – Ersteller – fehlt: tatsächliche Anzahl der Tools in `tools/` (im Kapitel sind nur sechs genannt) und ob ein siebtes existiert; Dokument unverändert

**B6** · Abschnitt „What is this?“ („It ships two published variants“) und Tabelle „Where things live“ (`config/variants.json` … „the five variants“) · Logikfehler · mittel
Befund: Oben stehen „two published variants“ (Deutsch, Englisch). In der Tabelle stehen „five variants“ in der Konfiguration. Im Text kommen außerdem mindestens `d12_alien_mid`, `alien`, `alien_en` und `alien_en_ws` vor. Das Verhältnis ist nicht erklärt: Welche fünf sind es, und was unterscheidet „veröffentlicht“ von den übrigen? Der Leser kann Zählung und Namen nicht zuordnen.
Vorschlag: Einen Satz oder eine kleine Liste ergänzen, die alle fünf Varianten nennt und kennzeichnet, welche zwei veröffentlicht sind und wofür die anderen (Workshop-Build, kontoloses Deutsch usw.) dienen.
Status: offen – Ersteller – fehlt: Liste der fünf Varianten in `config/variants.json` und welche zwei veröffentlicht sind; Dokument unverändert

**B7** · Abschnitt „Your first change“ („`alien_en` (`config/variants.json:55`) and the Workshop build `alien_en_ws` (`:160`)“) und Abschnitt „Run it locally“ („`config/variants.json:130`“) · unklar · gering
Befund: Die Zeilenverweise sind nicht verifizierbar und brechen bei jeder Änderung der Datei. Auffällig: Die Variante `alien_en` steht bei Zeile 55 und `alien_en_ws` bei Zeile 160, das Beispiel für `audio_recipe` aber bei Zeile 130. Die Reihenfolge ist daher nicht nachvollziehbar. `:160` ohne Dateiname ist zudem als Kurzform formuliert und nicht eindeutig.
Vorschlag: Die Zeilenangaben gegen die aktuelle `config/variants.json` prüfen. Besser auf die Schlüssel verweisen („Eintrag `alien_en` unter `variants`“), statt auf Zeilennummern.
Status: offen – Ersteller – Zeilennummern in `config/variants.json` nicht prüfbar (Datei darf nicht gelesen werden); `:160` zu `config/variants.json:160` ausgeschrieben, die Zeilenverweise folgen sonst der Zitierweise des Buchs

**B8** · Abschnitt „What is this?“ (Aufzählung „German track“ und „English track“) und Einleitung des Kapitels („build and install it in ten minutes“) · unklar · gering
Befund: Die Zusage „in ten minutes“ ist nicht belegt. Die Anleitung verlangt Extraktion eines Archivs, Verarbeitung von über tausend Dateien durch ffmpeg mit Rubberband und eine Installation. Der Zeitbedarf hängt davon ab. Ob zehn Minuten realistisch sind, ließ sich nicht verifizieren. Die unterschiedlichen Zeilenzahlen (2.324 deutsch gegenüber 1.750 englisch) sind außerdem nicht erklärt.
Vorschlag: Die Zeitangabe belegen (gemessene Laufzeit) oder streichen. Einen Halbsatz ergänzen, warum die Zeilenzahlen von Deutsch und Englisch abweichen.
Status: offen – Ersteller – „in ten minutes“ als unbelegt gestrichen (siehe C11); fehlt: Grund für die abweichenden Zeilenzahlen Deutsch/Englisch (siehe A3)

#### Prüfer C – Verständlichkeit
Fachgebiet: Softwareentwicklung / Audio-Pipeline für ein X4-Spielmod (Build-Werkzeuge, XML-Patches, Sprachausgabe) · Zielgruppe: Entwickler und Maintainer, die das Repository neu übernehmen oder erweitern wollen, mit Python- und Kommandozeilen-Kenntnissen, aber ohne X4-Modding-Vorwissen (abgeleitet)

**C1** · Abschnitt „What is this?“, Aufzählung („ships two published variants“) und Abschnitt „Run it locally“, Schritt 2 („the no-account German variant“) · unklar · hoch
Befund: Der Text nennt erst „two published variants“ (German und English), später „the five variants“ und „both English variants“ (`alien_en` und `alien_en_ws`). Der Leser erfährt nicht, wie Track, Variante und Workshop-Build zusammenhängen. Die „German track“ wird als ElevenLabs-Neusprache beschrieben, das Beispiel `d12_alien_mid` heißt aber „no-account German variant“. Das klingt nach einer Variante, die aus den Originalaufnahmen gefiltert wird, wird aber nicht erklärt. Der Leser weiß nicht, welche Variante er für die Schnellstart-Schritte bekommt und warum dafür kein ElevenLabs-Konto nötig ist.
Vorschlag: Einen Satz oder eine kleine Tabelle ergänzen, die alle fünf Varianten mit Sprache, Erzeugungsweg (Filterkette oder Text-to-Speech) und Veröffentlichungsstatus auflistet. Dabei erklären, was „no-account“ meint (ohne ElevenLabs-Konto, nur gefilterte Originale).
Status: offen – Ersteller – fehlt: Liste der fünf Varianten mit Sprache, Erzeugungsweg und Veröffentlichungsstatus; ergänzt wurde nur die Erklärung von „no-account“ (ohne ElevenLabs-Konto, gefilterte Originale statt Text-to-Speech)

**C2** · Abschnitt „Run it locally“, Prerequisites-Absatz und Codeblock („X4_GAME_DIR“, „python -I tools/…“) · unklar · mittel
Befund: Es steht nicht, dass die Befehle im Repository-Wurzelverzeichnis ausgeführt werden müssen, und nicht, in welcher Shell (PowerShell, steht nur indirekt im Codeblock-Label). Ob „X4_GAME_DIR“ nur für `build_mod`, `validate_mod` und `install_mod` gilt oder auch für den Pfad im Extraktionsbefehl, bleibt offen. Das Beispiel nutzt den Pfad fest. Die Python-Version ist nur mit „Python 3“ angegeben.
Vorschlag: Ergänzen: „Run all commands from the repository root in PowerShell.“ Außerdem angeben, welche Tools `X4_GAME_DIR` auswerten und welche Mindestversion von Python gilt.
Status: offen – Ersteller – „Run all commands from the repository root in PowerShell“ und Hinweis zum Standardpfad ergänzt; fehlt: welche Tools `X4_GAME_DIR` auswerten und die Mindestversion von Python

**C3** · Abschnitt „Run it locally“, Codeblock („voice-l049“, „voice-l044“, „03.cat“, „10201“) · unverständlich · mittel
Befund: Die Pfadbestandteile werden im Schnellstart nicht erklärt. Dazu gehören `l049` (Deutsch) und `l044` (Englisch), `10201` (Boso Ta), `normal` (Kontext) und `.cat`-Katalog. Der Leser kann nicht erkennen, was er für eine andere Sprache oder einen anderen Kontext ändern müsste. `l044` taucht erst im Abschnitt „Your first change“ auf, ohne Erklärung. Die Erklärung von 10201 steht erst unter „The mental model“, danach.
Vorschlag: Direkt unter dem Codeblock eine Legende ergänzen („l049 = German, l044 = English; 10201 = Boso Ta; normal = line context; .cat = X4 archive index, data in the matching .dat“).
Status: behoben – Legende unter dem Codeblock ergänzt: `l049` = Deutsch, `l044` = Englisch, `10201` = Boso Ta, `normal` = Zeilenkontext, `.cat` = Textindex des gleichnamigen `.dat`-Archivs

**C4** · Abschnitt „Run it locally“, Schritt 2 und 3 („--variant d12_alien_mid --gain-db 9 … --dst build\audio\d12_alien_mid_g9“, „install_mod.py alien“) · unverständlich · hoch
Befund: Nicht erklärt wird, was `--variant`, `--gain-db 9` und der Ordnername `d12_alien_mid_g9` bedeuten. Schritt 3 ruft `build_mod.py` und `validate_mod.py` ohne Argumente auf. Dem Leser ist unklar, woher diese Tools wissen, dass sie den eben erzeugten Ordner `build\audio\d12_alien_mid_g9` nehmen sollen. Erst später ist indirekt von `audio_variant` in `config/variants.json` die Rede. Auch das Argument `alien` bei `install_mod.py` bleibt unerklärt, und es ist nicht erkennbar, dass es zu `d12_alien_mid` gehört. Das Versprechen „in ten minutes“ lässt sich so nicht nachvollziehen.
Vorschlag: Nach dem Codeblock erklären, dass `audio_variant` in `config/variants.json` auf den Ordner unter `build\audio\` zeigen muss. Dazu erklären, was die Optionen und Namensteile bedeuten (z. B. `g9` = +9 dB) und welcher Variantenname `alien` entspricht.
Status: offen – Ersteller – erklärt wurde, dass `build_mod.py` über `audio_variant` in `config/variants.json` den Ordner unter `build\audio\` findet und `_g9` den `--gain-db`-Wert wiederholt; fehlt: welche Variante `alien` ist und ob sie `d12_alien_mid_g9` nutzt (siehe B1)

**C5** · Abschnitt „Run it locally“, Absatz nach dem Codeblock („`-I` runs Python in isolated mode (no environment variables, …)“) · sachlicher Fehler · mittel
Befund: Der Isolated-Modus von Python (`-I`) ignoriert nur die `PYTHON*`-Umgebungsvariablen, das aktuelle Verzeichnis und das User-site-Verzeichnis. Eigene Variablen wie `X4_GAME_DIR` bleiben für `os.environ` sichtbar. „no environment variables“ widerspricht außerdem dem Hinweis oben, man könne `X4_GAME_DIR` setzen, und lässt den Leser zweifeln, ob das funktioniert. Quelle: Python-Dokumentation zur Option `-I` (docs.python.org/3/using/cmdline.html#cmdoption-I), aus dem Gedächtnis zitiert und nicht neu abgerufen.
Vorschlag: Formulieren: „`-I` runs Python in isolated mode (ignores `PYTHON*` environment variables and the user site-packages; `X4_GAME_DIR` still works).“
Status: behoben – bereits durch A1 behoben

**C6** · Abschnitt „Run it locally“, Absatz nach dem Codeblock („search the plain-text indexes“, „./init.sh runs step 3's first two commands“) · unklar · mittel
Befund: „plain-text indexes“ ist ohne Vorwissen über X4-Archive nicht verständlich. Gemeint sind offenbar die `.cat`-Dateien, die als Textindex zu den `.dat`-Dateien dienen. `./init.sh` ist ein Shell-Skript im Bash-Stil, der Abschnitt setzt aber PowerShell voraus. Es bleibt offen, ob und wie es unter Windows läuft (Git Bash?). Der Absatz mischt zudem fünf Themen in einem Block (Katalogsuche nach Patch, Textdateien, `init.sh`, Rezept-Speicherort, Verweis). Zeilenverweise wie `config/variants.json:130` und `init.sh:6-7` sind nach jeder Änderung veraltet.
Vorschlag: In Stichpunkte aufteilen, „.cat = plain-text index of the matching .dat archive“ erklären, die nötige Shell für `init.sh` nennen und statt Zeilennummern den Schlüsselnamen angeben (z. B. „key `audio_recipe` of each variant“).
Status: offen – Ersteller – Absatz in Aufzählungspunkte aufgeteilt und `.cat` erklärt (siehe C3); fehlt: in welcher Shell `./init.sh` unter Windows laufen soll; Zeilenverweise siehe B7

**C7** · Abschnitt „The mental model“, Punkte 2 und 3 („XML diff“, „redirect path“, „mod id“, „language suffix“) · unverständlich · mittel
Befund: Nicht erklärt werden „XML diff“ (X4-Modding-Mechanismus zum Patchen von Spieldateien) und „mod id“ (wo festgelegt, z. B. in `content.xml`). Auch das „language suffix“ bleibt offen: Welches Suffix würde die Engine sonst anhängen? Der Schluss „one mod folder serves one voice language only“ folgt für den Leser nicht erkennbar aus der Aussage, dass kein Suffix angehängt wird.
Vorschlag: Je einen Halbsatz ergänzen, z. B.: „XML diff = X4's mechanism for patching a game XML file without replacing it“, und den Zusammenhang erläutern: ohne Sprachsuffix gibt es keine Trennung nach Sprache, daher ein Ordner pro Sprache.
Status: behoben – „XML diff“ als X4-Mechanismus zum Patchen einer Spiel-XML erklärt, „mod id“ als `<id>` in `dist/<id>/` benannt, Sprachsuffix erläutert (Spielpfade tragen die Sprache im Ordnernamen, der Redirect nicht, daher ein Ordner pro Sprache)

**C8** · Abschnitt „Where things live“, Tabellenzeile `release/` und Abschnitt „What is this?“ („Workshop“, „modpub“, „sound ids“) · unverständlich · gering
Befund: „modpub“ („external `modpub` release tool“) ist weder erklärt noch verlinkt. „Sound ids“ in der Zeile zu `config/variants.json` und „Workshop staging“ in der Zeile zu `build/` setzen Wissen über Steam Workshop und die X4-Soundbibliothek voraus. Der Leser weiß nicht, ob er `modpub` für den Einstieg braucht.
Vorschlag: Hinter `modpub` kurz erklären, was das Tool tut und ob es Pflicht ist. Außerdem „sound ids“ ausschreiben („the six sound-library ids“).
Status: offen – Ersteller – „sound ids“ zu „six sound-library ids“ ausgeschrieben; fehlt: was das Tool `modpub` tut und ob es für den Einstieg nötig ist

**C9** · Abschnitt „Your first change“, erster Absatz und Befehl („Make the English variant 2 dB quieter“, „--gain-db 2“, „alien_mid_50_g2“) · Logikfehler · hoch
Befund: Die Aufgabe lautet „2 dB quieter“, der Befehl übergibt aber `--gain-db 2`. Ein positiver Gain-Wert macht lauter (im Schnellstart steht `--gain-db 9` für +9 dB). Der Leser kann nicht erkennen, ob `2` hier ein Absolutwert oder eine Änderung gegenüber dem aktuellen Wert ist. Der aktuelle Gain der Variante `alien_mid_50` wird nicht genannt. Falls `2` gewollt ist, fehlt die Erklärung. Falls nicht, würde der Leser die Stimme lauter statt leiser machen. Das Namensschema `_g2` ist ebenfalls nicht erklärt.
Vorschlag: Aktuellen Gain-Wert nennen und den neuen Wert ausrechnen (z. B. „currently X dB, so use --gain-db X-2“). Alternativ das Beispiel auf „2 dB louder“ umstellen. Außerdem erklären, ob `--gain-db` absolut ist oder relativ, und das Suffix `_g2` erklären.
Status: offen – Ersteller – fehlt: aktueller Gain-Wert von `alien_mid_50` und Wirkungsweise von `--gain-db` (absolut/relativ); siehe A2; das Suffix `_g2` wurde in der Legende zu Schritt 3 als Wiederholung des `--gain-db`-Werts erklärt

**C10** · Abschnitt „Your first change“, letzter Satz („Judge the result in the game, never on headphones“) · unklar · gering
Befund: Das Spiel kann ebenfalls über Kopfhörer laufen. Gemeint ist vermutlich, dass man die fertige Datei nicht isoliert abhören darf, weil sie im Spiel gegen die Stationsgeräusche untergeht. Das ist so nicht ausgedrückt. Die Abfolge ist außerdem ein Fließtext-Satz („Then set … Then build_mod.py, validate_mod.py, close X4, install_mod.py alien_en“) und als Anleitung schwer abzuarbeiten.
Vorschlag: Umformulieren zu „Judge the result by playing the game, not by listening to the file alone“. Die Schritte nach den beiden Befehlen als nummerierte Liste mit den vollständigen Befehlszeilen schreiben.
Status: behoben – „never on headphones“ zu „never by listening to the files on their own (for example on headphones)“ präzisiert; Schritte nach den Befehlen als nummerierte Liste mit vollständigen Befehlen geschrieben

**C11** · Kapitelanfang, Einleitungs-Zitat („purpose, operations, domain, change“) · unklar · gering
Befund: Die Klammerbegriffe sind Lernziel-Kategorien, die im Kapitel nicht wieder aufgegriffen werden. Es bleibt unklar, welcher Abschnitt welche Frage beantwortet. „Ten minutes“ ist unplausibel, wenn Katalog-Extraktion, Audioverarbeitung (ffmpeg mit Rubberband über alle Zeilen) und Installation nötig sind.
Vorschlag: Die Klammerbegriffe streichen oder den Abschnitten zuordnen. „Ten minutes“ durch eine ehrlichere Angabe ersetzen oder die Annahme nennen (z. B. „bei bereits installiertem ffmpeg“).
Status: behoben – „in ten minutes“ gestrichen; Klammerbegriffe den Abschnitten zugeordnet (purpose = What is this?, operations = Run it locally, domain = The mental model, change = Your first change)

### Stufe 3 – Abschlussvermerk des Erstellers
- Ergebnis: stimmig nach Korrekturen
- Korrekturen des Erstellers:
  - A2/B2/C9: Erklärt, dass `--gain-db` absolut nach der Normalisierung wirkt (`process_audio.py:83,94-95`) und die englische Variante bisher mit `--gain-db 4` gebaut ist; `--gain-db 2` ist damit 2 dB leiser. Endstand jeweils behoben.
  - A3/B8: Stand 9.00 genannt und den Unterschied erklärt (574 Zeilen nur im deutschen Track), mit Verweis auf Kapitel 13. Endstand behoben.
  - B1/B6/C1/C4: Tabelle der fünf Varianten mit Sprache, Erzeugungsweg, Audioordner und Status ergänzt; erklärt, dass `alien` auf `d12_alien_mid_g9` zeigt und was `--variant` und `--gain-db` tun. Endstand behoben.
  - B5: Die sieben Tools namentlich aufgezählt (inklusive `check_coverage.py`); „one per pipeline step“ gestrichen. Endstand behoben.
  - B7: Zeilenverweise gegen die aktuelle `config/variants.json` geprüft (55, 130, 160 stimmen) und um die Schlüsselnamen ergänzt. Endstand behoben.
  - C2: Python-Version ergänzt (entwickelt mit 3.14). Endstand behoben.
  - C6: Shell für `init.sh` genannt (Bash, unter Windows Git Bash) und den Schlüssel `audio_recipe` benannt. Endstand behoben.
  - C8: `modpub` erklärt (externes Upload-Tool, für Bauen und Installieren nicht nötig). Endstand behoben.
- Für den Nutzer offen: keine
- Abgeschlossen: 2026-10-25 17:32
