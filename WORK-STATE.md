# Patch Jury — WORK STATE

Aktualizacja: **27.10.2026**. Stan: offline submission kit gotowy lokalnie; live wymaga klucza ownera. **NOT SUBMITTED.** Ten dokument zastępuje operacyjny stan z 25.10; historyczne testy/publiczny preview pozostają w lokalnym checkpoint Git.

## Konta i granice sesji

- Devpost: **ZAREJESTROWANI**; Builder Program: **APPROVED** — dane od ownera w zadaniu, bez ponownego logowania.
- Blokada PW: sesja console.nebius.ai przez GitHub, zastosowanie kodu $25 i klucz API. Kod przekazany ownerowi; nie skopiowano go do publicznego pakietu. Termin zastosowania 31.12.2026. Kredyty partnerskie LangSmith/Tavily pozostają w mailach Welcome z 26.10; projekt ich nie wymaga.
- W tej sesji: brak logowania do konsoli, inferencji, push, uploadu YouTube i submitu. Rzeczywisty koszt inferencji: **$0**, wywołania live: **0**.
- Deadline operacyjny: **30.10.2026 18:00 Europe/Warsaw**; oficjalne 10:00 PDT = 17:00 UTC = 18:00 PL. Cutoff wewnętrzny 29.10, 23:00 PL.

## Gotowe

- Flow: fixture z patchem A/B → walidowane boundary inputs → trusted oracle → Docker base/A/B → deterministyczny werdykt i eksport JSON.
- Werdykt `supported` tylko dla jedynego patcha bez niepowodzeń; remis albo obydwa niepełne wyniki → `inconclusive`. Nie ma automatycznego merge.
- Adapter przez `NEBIUS_API_KEY`, `NEBIUS_BASE_URL`, `MODEL` oraz potwierdzenie kredytów. Domyślnie Token Factory `/v1`, NVIDIA `nvidia/Nemotron-3_5-Lightning`; klucz od PW wystarczy bez zmiany kodu. Live działa bez cichego fallbacku, ale uwierzytelnionego kontraktu nadal nie potwierdzono.
- Aktualny publiczny katalog 27.10 potwierdza model i ceny $0.06/$0.24 per million input/output tokens: evidence/model-catalog-20261027.json. Ledger i ograniczenia kosztowe zachowane.
- README, `.env.example`, SUBMISSION-KIT.md (dwa akapity EN, pola, tagi, wymagania, kroki PW), scenariusz 80 s i English TTS.
- `demo/submission/submission-offline.mp4`: 80 s, 1280×720, H.264/AAC. Rzeczywiste zrzuty lokalnej aplikacji, montaż statycznych klatek; nie ciągłe nagranie interakcji. Jawny banner offline, placeholder klucza, brak twarzy i udawanego wywołania API. 76.1 s narracji + cisza do końca. Klatki przejrzane, film zdekodowany przez FFmpeg.
- Allowlist archiwum `demo/submission/patch-jury-submission.tar.gz` + SHA256, kod, skompilowany UI, testy i materiały. Bez credential/account evidence, logów sesji i runtime ledger.

## Weryfikacja

- `npm run build`: PASS.
- `PATCHJURY_INTEGRATION=1 python3 -W error::ResourceWarning -m unittest discover -s tests -v`: **17/17 PASS**, bez skipów (evidence/final-test-output.txt).
- Docker: trzy regresje, readonly/nonroot, brak sieci i sekretów hosta, timeout cleanup.
- Nowe testy: routing ENV/modelu/provenance, utrzymanie rezerwacji po timeout/błędnym JSON/złym modelu bez retry i fallbacku, odrzucanie błędnego URL i modelu, fail closed przy zmianie ceny, brak fałszywego zwycięzcy przy remisie lub dwóch porażkach. Mock nie potwierdza realnego API.
- Realny browser smoke podczas renderu: pages 6/3/9, money 1/4/9, werdykt, counterexamples i przełączenie fixture. Report `evidence/submission-pages.json`.
- Wyniki pass/fail offline są powtarzalne; czasy wykonania i hash zawierający czasy różnią się między uruchomieniami.

## Końcowy przegląd w bieżącej sesji

- Porównano strukturę submission kit z `qloo-agentic-2026/SUBMISSION-KIT.md`: status, kroki PW, pola, opis EN i testing instructions.
- Ponownie sprawdzono publiczny regulamin i katalog modelu; bez logowania i bez inferencji.
- UI pokazuje request ID i usage live oraz osobną liczbę challenge-only przypadków rozróżniających. Zmiana trybu ukrywa poprzedni wynik do ponownego uruchomienia.
- Ponownie zbudowano TypeScript, wykonano pełne 17 testów, odświeżono render oraz allowlistowane archiwum.

## Lokalny Git i publikacja

Chronione `.git` jest read-only/puste w sesji. Istniejące lokalne metadane **checkpoint.git** służą do commita: `git --git-dir=checkpoint.git --work-tree=. log -1`. Nie wykonano push. Logi sesji i prywatne account evidence pozostają poza publicznym archiwum.

Publiczne repo https://github.com/Schultzenator/patch-jury i release v0.1.1-preview pochodzą z 25.10 i **nie zawierają nowych zmian**. Publikacja bieżącego commita/archiwum jest krokiem PW.

## Pozostaje PW

1. Console/GitHub ownera → kredyty → API key → ENV → realny live report z request ID, modelem i usage.
2. Ocenić challenge-only rozróżnienie osobno od holdoutów; dopisać autentyczny feedback.
3. Live screen capture 60–90 s według demo/README.md, publiczny YouTube, aktualny publiczny kod i test build.
4. Wkleić SUBMISSION-KIT.md do Devpost, sprawdzić eligibility i URL, submit oraz dowód Submitted. Utrzymać dostęp do końca oceniania 15.12.

Nie zaplanowano automatycznej publikacji ani przyszłego submitu.
