# Ghostwriter

*[Read in English](README.md)*

Un plugin per Claude Code che tiene un profilo documentato delle persone con cui
tratti, costruito dalle trascrizioni dei tuoi incontri e salvato nel tuo workspace
Notion.

## Il problema

Fra un incontro e l'altro dimentichi cosa conta davvero per le persone. Chi deve
giustificare una decisione e davanti a chi. Cosa ha detto il cliente sui tempi di
consegna tre mesi fa. Quale concessione ha sbloccato le cose l'ultima volta. I verbali
non aiutano: registrano cosa è stato deciso, non cosa ognuno vuole, teme e accetta.

Ghostwriter legge la trascrizione di un incontro e tiene, per ogni interlocutore, un
profilo che cresce nel tempo: driver, stile decisionale, leve efficaci, cose da
evitare, timori, posizioni ferme e negoziabili. **Ogni riga poggia su una citazione
testuale con il suo minuto.** Se la citazione non c'è, il campo resta vuoto. Prima
dell'incontro successivo ti dice cosa rischia ognuno se dice sì, cosa chiedere e cosa
non dire. Scrive la bozza del follow-up. Non invia mai niente.

## Come funziona

```
registrazione ──► trascrizione ──► process-meeting ──► Notion: pagina Incontro + profili aggiornati
 (PLAUD o           (solo testo,                         + briefing, mossa consigliata,
  qualunque altro)   mai l'audio)                           bozza di follow-up, previsioni

prepare-meeting · compose-message · consult-profile   leggono i profili, non scrivono niente
```

1. Registri un incontro a cui hai partecipato (un PLAUD, il telefono, qualunque cosa).
2. Ottieni la trascrizione: da PLAUD, da un servizio qualsiasi, o in locale con
   `tools/transcribe.py`.
3. `process-meeting` la normalizza in turni numerati, identifica chi ha parlato,
   estrae fatti, posizioni e interessi, chiude le previsioni aperte e aggiorna su
   Notion il profilo di ogni persona — una alla volta, con una citazione per ogni
   affermazione.
4. `prepare-meeting`, `compose-message` e `consult-profile` leggono soltanto.

Tutto sta in due database Notion: **People** (una pagina per interlocutore) e
**Meetings** (una pagina per registrazione, con la trascrizione in una sottopagina).
Lo stato di ogni elaborazione vive su Notion, quindi un'elaborazione interrotta
riprende da dove si era fermata invece di duplicare.

Ogni briefing chiude le **previsioni** aperte e ne apre di nuove, in forma
falsificabile (`SE faccio X, ALLORA lui farà Y; SMENTITA SE Z`). Un profilo che non si
può smentire non si può nemmeno correggere. Un tasso di avveramento sotto il 40%
significa che il profilo è sbagliato; sopra il 90%, che le previsioni sono troppo
ovvie.

## Il profilo

| Campo | Cosa contiene |
|---|---|
| Key drivers | Status, Security, Control, Autonomy, Recognition, Belonging, Financial result — solo quando un pattern emerge in 2+ incontri |
| Decision style | Analytical, Intuitive, Consensual, Directive, Avoidant — solo dopo aver osservato una decisione vera |
| Communication style | come parla, con citazioni |
| Goals and interests | cosa gli permette di fare o evitare una posizione |
| Fears | i rischi che percepisce, scritti come argomenti da preparare, non come punti deboli |
| Sensitive topics | temi di business da preparare |
| Effective levers | interesse → mossa → perché funziona per lui → costo per te |
| Things to avoid | ciò che non funziona o si ritorce contro |
| Firm / Negotiable positions | negoziabile solo se ha posto una condizione («se…, allora…») |
| Alignment with me | Ally, Favorable, Neutral, Skeptical, Opponent |
| Profile reliability | Low / Medium / High, dal numero di incontri con evidenza vera |
| User notes | tue: l'agente le legge, non le scrive mai, e prevalgono sempre |

I nomi dei campi e delle opzioni su Notion restano in inglese (sono il contratto su cui
si basano le query); il contenuto è scritto nella tua lingua.

Ogni affermazione porta il suo livello di confidenza (`hypothesis`, `observed`,
`pattern`) e il numero di incontri su cui poggia. Le ipotesi non entrano mai nei campi
del profilo: finiscono in un elenco «da verificare», come domande aperte. Un profilo
con tre campi pieni e otto vuoti è un profilo sano.

## Cosa non farà mai

- **Analizzare l'audio.** Niente tono, intonazione, esitazioni, emozioni dedotte dalla
  voce. Solo il testo. L'AI Act (art. 5(1)(f)) vieta l'inferenza di emozioni da dati
  biometrici, come la voce, sul luogo di lavoro; lavorare solo sul testo è ciò che
  tiene il sistema fuori da quel divieto.
- **Inviare qualcosa.** Scrive bozze. Un invio automatico basato su un profilo
  psicologico è esattamente ciò che non deve poter accadere per errore.
- **Valutare chi lavora per te.** Niente giudizi di rendimento, nessun uso per
  assunzioni, promozioni, mansioni o provvedimenti disciplinari. Usarlo così lo
  renderebbe un sistema ad alto rischio secondo l'AI Act (Allegato III) e uno
  strumento di controllo dei lavoratori secondo la maggior parte delle leggi sul
  lavoro. Chi è nell'elenco dei tuoi subordinati ha un profilo per lo più vuoto, per
  costruzione, e le sue parole non vengono archiviate integralmente.
- **Scrivere qualcosa senza citazione.** Un campo vuoto è meglio di psicologia
  plausibile.
- **Indovinare chi sta parlando.** Se non è certo, si ferma e chiede: un'attribuzione
  sbagliata avvelena due profili per sempre.
- **Registrare dati di categorie particolari** (salute, politica, religione,
  sindacato, orientamento sessuale, origine etnica — art. 9 GDPR). Se emergono,
  vengono oscurati e non usati mai.
- **Profilare chi non era presente**, o elaborare registrazioni di conversazioni a cui
  non hai partecipato.
- **Conservare dati dopo una richiesta di cancellazione.** `remove-person` ripulisce
  la persona da tutte le pagine e ti dice i passaggi manuali (cestino, cronologia delle
  versioni, file locali) che una vera cancellazione GDPR richiede.

Il test che regge tutto: ogni riga deve poter essere mostrata alla persona di cui
parla. Il ragionamento è «cosa rischia questa persona se dice sì», non «dove la
spingo».

## Requisiti

- [Claude Code](https://claude.com/claude-code)
- Il **connettore MCP di Notion**, collegato a un workspace Notion **personale** (non
  quello aziendale: un amministratore del workspace può leggere tutto)
- Facoltativo: un registratore **PLAUD** con il suo connettore MCP, per prendere le
  trascrizioni direttamente
- Facoltativo: **mlx-whisper** su un Mac Apple Silicon, per trascrivere l'audio in
  locale con `tools/transcribe.py`

## Installazione

Come plugin:

```
/plugin marketplace add rlfszn/ghostwriter
/plugin install ghostwriter@ghostwriter
```

Oppure copia le skill a mano (tieni insieme tutte e sette le cartelle: si richiamano
a vicenda come cartelle sorelle):

```bash
git clone https://github.com/rlfszn/ghostwriter
cp -r ghostwriter/skills/* ~/.claude/skills/
```

## Primo avvio

Di' **«configura Ghostwriter»**. La skill `setup-notion-memory`:

1. crea la tua **cartella Ghostwriter**, `~/.ghostwriter/`, e ci copia i modelli:
   `configuration.md`, `style.md`, `deletions.md`, più `transcripts/incoming/` e
   `transcripts/archive/`;
2. ti chiede di compilare `configuration.md` — come minimo `me` (il tuo nome, ogni
   alias con cui una trascrizione può indicarti, un'email di contatto) e
   `subordinates` (tutti quelli che riportano a te). `me` serve a non profilare te
   stesso; `subordinates` serve a non trattare un collaboratore come una controparte;
3. verifica che il workspace Notion non abbia altri membri, poi crea i due database,
   le relazioni, i rollup e le viste, e scrive gli ID in `configuration.md`.

I tuoi file privati stanno **fuori dal plugin**, così gli aggiornamenti non li toccano
mai. Per un'istanza separata (per esempio una per il lavoro e una personale), lancia il
setup da una cartella di progetto e chiedi un'istanza di progetto: crea lì
`./.ghostwriter/`, e le skill la usano ogni volta che lavori da quella cartella.

Prima di usare `compose-message` compila `style.md` con 3-5 messaggi veri che hai
mandato, altrimenti le bozze suoneranno come l'agente, non come te.

Di default le skill girano in modalità **autonoma**: non si fermano mai a chiedere,
lasciano su Notion tutto ciò che è dubbio marcato «da confermare». Comincia la
richiesta con `MODE: interactive` (o metti quella riga nel tuo `CLAUDE.md`) se vuoi che
ti facciano le domande. Finché `confirm_before_writing_profiles` è `true`, nelle
esecuzioni interattive ti mostrano ogni modifica ai profili prima di scriverla.

## Uso

| Dici | Skill | Risultato |
|---|---|---|
| «elabora la riunione di stamattina» | `process-meeting` | pagina Incontro + profili aggiornati + briefing |
| «domani vedo Marco per il budget, come lo approccio?» | `prepare-meeting` | obiettivo, cosa rischia lui se dice sì, domande, concessioni a costo zero |
| «scrivimi il messaggio per Barlow» | `compose-message` | una bozza nel tuo registro, da rileggere |
| «cosa sappiamo di Farnsworth?» | `consult-profile` | il profilo, e su quanti incontri poggia |
| «cancella il profilo di X» | `remove-person` | bonifica completa per il GDPR, dopo la tua conferma |
| «configura Ghostwriter» / «crea i database su Notion» | `setup-notion-memory` | setup del primo avvio, una volta sola |

Le skill rispondono, e scrivono su Notion, nella tua lingua. I nomi delle proprietà su
Notion restano in inglese: sono il contratto su cui si basano le query.

### Trascrivere in locale

`tools/transcribe.py` trascrive l'audio sul tuo Mac senza mandarlo da nessuna parte:

```bash
uv venv --python 3.11 .venv && uv pip install --python .venv/bin/python mlx-whisper numpy
.venv/bin/python tools/transcribe.py --language it riunione.m4a
```

L'output va in `transcripts/incoming/` nella tua cartella Ghostwriter, senza etichette
dei parlanti: l'attribuzione la fa l'agente dal contenuto, e lo dichiara. Con PLAUD e i
parlanti rinominati nella sua app, questo passaggio non serve.

## Usarlo con altri agenti

Le skill sono semplici file markdown `SKILL.md` con frontmatter standard. Qualunque
agente che carica skill in quel formato le può usare: non c'è codice da integrare, c'è
testo da caricare. Indica all'agente `AGENTS.md` per le regole sempre valide, dagli un
connettore Notion e tieni la stessa cartella Ghostwriter. Il contratto verso l'esterno
è lo schema Notion (`skills/profiling-references/references/notion-schema.md`): chi
legge o scrive i due database rispetta quello.

Le skill sono scritte per girare anche senza presidio (un webhook dal registratore, un
job programmato). In quella modalità non chiedono mai, non sovrascrivono mai un campo
già compilato, non cancellano niente, e `remove-person` si rifiuta di partire. Vedi
`skills/profiling-references/references/execution-modes.md`.

## Com'è organizzato

```
.claude-plugin/              manifest del plugin e del marketplace
AGENTS.md                    regole sempre valide, per qualunque agente
skills/
  profiling-references/      LIBRERIA: regole, metodo, schema, limiti, modelli
  process-meeting/           il flusso principale
  prepare-meeting/           sola lettura
  compose-message/           sola lettura + bozze
  consult-profile/           sola lettura
  remove-person/             distruttiva, chiede conferma
  setup-notion-memory/       setup del primo avvio
tools/transcribe.py          trascrizione locale con mlx-whisper
tests/                       4 casi sintetici + 8 test negativi
```

Una sola copia della logica: il metodo di analisi, lo schema Notion e i limiti legali
stanno nella libreria, e le skill li richiamano.

## Test

`tests/` contiene quattro incontri sintetici con i risultati attesi e otto test
negativi in cui il comportamento giusto è fermarsi (materiale insufficiente,
trascrizione rumorosa, parlanti sconosciuti, dati sensibili, messaggio ingannevole,
incontro singolo, uso HR, analisi della voce). Eseguili su database di prova prima
della prima registrazione vera: di' «esegui la suite di test in sandbox». Istruzioni in
`tests/README.md` (in inglese).

## Note legali

Questa non è consulenza legale. Rispettare le leggi che ti riguardano è una tua
responsabilità: in molti paesi registrare una conversazione richiede di avvisare le
altre persone, o il loro consenso; i luoghi di lavoro hanno spesso regole sui
registratori; e la normativa sulla protezione dei dati (il GDPR nell'UE) si applica ai
profili che conservi. Prima di registrare una riunione verifica le policy della tua
azienda — se lo vietano, non farlo. Di' alle persone che registri, spegni quando te lo
chiedono, e se qualcuno chiede cosa hai scritto su di lui, mostragli la pagina.
`skills/profiling-references/references/ethical-legal-limits.md` spiega le regole che
applica l'agente e quelle che spettano a te.

## Licenza e autore

MIT. Creato da Elia Rolfi.
