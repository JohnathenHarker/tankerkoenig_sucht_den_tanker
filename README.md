# tankerkoenig_sucht_den_tanker

## Änderungen am Entwurf aom 29.12.
- Für die Grobsortierung können wir wohl nicht alle Werte verwenden, da 24000 sehr wahrscheinlich zu viele sind. Ich würde vorschlagen, hier jeweils nur einen Wert pro Tag zu betrachten, dann haben wir ca 1000 Werte. Das sollte noch berechenbar sein (in erlebbarer Zeit)
- für die Feinsortierung: auf der SOFM Abschnitte von 8 Tagen anorden lassen. dann Interpretation als Funktion wie folgt: von den ersten sieben Tagen wird auf den achten (folgenden) Tag abgebildet. Vorteil: weniger Zugriffe und wir können mit "verrauschten" Werten als Vorhersage arbeiten. 
