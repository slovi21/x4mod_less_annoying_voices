# Lessons Learned

Dauerhafte, nicht offensichtliche Erkenntnisse mit Beleg. Einmaliges und Allgemeinplätze gehören nicht hierher.

## Werkzeuge / Umgebung

- **OneDrive setzt das ReadOnly-Attribut auf Ordner.** Repos unter `OneDrive\Documents\#repos` haben schreibgeschützte Verzeichnisse (`attrib` zeigt `R`). Folgen: `shutil.rmtree` scheitert mit `WinError 5` beim `rmdir`, obwohl die Dateien darin gelöscht werden; `shutil.copytree` überträgt das Attribut ins Ziel, sodass auch dort nicht mehr gelöscht werden kann. Abhilfe: Ordner in place überschreiben statt löschen (`build_mod.py`), beim Löschen `onexc`-Handler mit `os.chmod(path, stat.S_IWRITE)` (`install_mod.py`), nach dem Kopieren Attribut im Ziel entfernen. Bash `rm -rf` und PowerShell `Remove-Item -Force` sind davon nicht betroffen. *(Beleg: Sitzung 2026-10-22, `attrib`-Ausgabe und Traceback in `tools/install_mod.py`.)*
- **Große Bash-Heredocs scheitern im Bash-Tool.** Mehrere lange `cat <<'EOF'`-Blöcke in einem Aufruf brachen mit „unexpected EOF while looking for matching `'`" ab. Dateien dieser Größe mit dem Write-Tool anlegen. *(Beleg: Sitzung 2026-10-22.)*

## X4-Modding

- **Boso Ta hat keine eigene Sprach-Page.** Er spricht über das geteilte Set `10201` („Boron NPC 1 / Boron rep / Misc Plot Characters"). Sprecher-Pages sind nicht über den Figurennamen in `t/0001-l044.xml` auffindbar, sondern über die `$speak`-IDs der MD-Skripte, die als Dateinamen `voice-l044/<page>/<kontext>/<speak-id>.ogg` wiederauftauchen. *(Beleg: `docs/phase0-befund.md` §1.)*
- **Die Extension-Tabelle im Nutzerordner ist rechnerspezifisch** (`content-<Rechnername>.xml`, hier `content-MSI-PRODP20Z.xml`), nicht `content.xml`. Beim Debuggen „Mod ohne Wirkung" dort nachsehen. *(Beleg: X4 9.00, Nutzerordner 2026-10-22.)*
