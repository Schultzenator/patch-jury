# Nebius × NVIDIA — stan pracy

Aktualizacja: 25.10.2026. Projekt: **Patch Jury**. Stan: lokalny MVP działa; rejestracja, live Nebius i submission **nieukończone**. Nie jest to zgłoszenie do konkursu.

## Terminy

- Plan ownera: build 25–26.10, demo 27.10, submit 28.10.
- Cutoff wewnętrzny: **29.10.2026 23:00 Europe/Warsaw**.
- Deadline oficjalny: **30.10.2026 18:00 Warszawa / 17:00 UTC**.
- Dostępność test buildu wymagana przez ocenianie do 15.12.2026.
- Nie utworzono automatycznego harmonogramu wznowienia; daty nie są obietnicą samoczynnego submitu.

## Rejestracja i konta

- Najpierw sprawdzono wskazany adres: **p.szutt@neisse.ai**. OpenBao `factory/credentials/neisse-mail` istnieje. **Logowanie IMAP na imap.dpoczta.pl zakończone OK**; skrzynka istnieje. MX: mx-1.dpoczta.pl / mx-2.dpoczta.pl. Wczorajszy bounce znaleziony w Gmail nie jest aktualnym dowodem braku skrzynki. Nie użyto fallback Gmail do rejestracji.
- Gmail connector potwierdza konto p.szutt@gmail.com i nazwę Piotr Szutt. Nie wysłano wiadomości.
- OpenBao dostępny i unsealed. Lista credential services nie zawiera Devpost ani Nebius. Nie zapisano fikcyjnych credentials ani nie generowano hasła jako substytutu niezałożonego konta.
- **Devpost: brak konta utworzonego w tej sesji; brak Join i Submitted.** Próby `cua.getState()` zwracają brak przeglądarek; createBrowserTab chrome oraz iab zwracają Browser is not available. Bezpośredni odczyt formularza secure.devpost.com/users/register: HTTP 403. Nie obchodzono CAPTCHA ani zabezpieczeń.
- **Nebius:** brak credentials, API key, potwierdzonych darmowych kredytów i realnej inferencji. Nie aktywowano planu, nie dodano karty, nie uruchomiono płatnego GPU/fine-tuningu.
- GitHub CLI uwierzytelniony jako **Schultzenator**. Status publikacji zostanie zapisany poniżej po weryfikacji.
- YouTube: brak dostępnego upload connectora; brak opublikowanego filmu.

## Eligibility

Publiczny regulamin sprawdzony 25.10: pełnoletność, wykluczenia terytorialne i konflikty obejmujące sponsorów, sędziów, pracodawców i gospodarstwo domowe. Nie wywnioskowano odpowiedzi ownera. Nie zaobserwowano formularza żądającego dokumentu tożsamości; konto i formularz nie zostały otwarte. Dokładne pytania można ustalić dopiero po dostępie do rzeczywistego formularza. Brak fake identity.

## Decyzje techniczne

- Najlepsza propozycja z sekcji Nebius w PROPOSALS.md: Patch Jury, Coding and Agentic Engineering.
- Python stdlib + TypeScript; bez zależności runtime Python. UI lokalne, test build do instalacji; brak publicznego serwera z Docker socket.
- Oficjalny wymóg to Nebius Token Factory/AI Cloud oraz NVIDIA model w runtime. Wybrano **inferencję**, bez fine-tuningu: `nvidia/Nemotron-3_5-Lightning`. Katalog oficjalny pobrany 25.10 i zapisany w evidence/nebius-model.json.
- Model proponuje wyłącznie JSON inputs. Host waliduje typy, domeny, liczbę i duplikaty; własny oracle dostarcza expected. Model nie dostaje patchy ani holdoutów i nie generuje wykonywanego kodu.
- Trzy własne fixture: pages, money, intervals; po dwa konkurencyjne patche, smoke/challenge/held_out, hash źródeł, czasy i eksport JSON.
- Docker: digest-pinned Python; network none, nonroot, read-only, no caps, no-new-privileges, limity RAM/CPU/PID/FD i timeout z cleanup. Bubblewrap odrzucony po rzeczywistym błędzie uprawnień namespace. Dowolne PR/repo nie są wspierane.
- Authored-example to **ręcznie napisane** przypadki, nie replay modelu. Mock API w testach nie jest dowodem realnego Nebius.

## Koszt API

**Rzeczywisty koszt inferencji tej sesji: $0; liczba wywołań inferencji: 0.** Darmowych kredytów nie potwierdzono. Publiczne pobranie katalogu nie jest inferencją.

Limit: $10. Ledger SQLite rezerwuje $0.01 na każdą próbę, także zakończoną błędem; atomowa blokada przy $10. Przy runtime sprawdzane ceny nie mogą przekroczyć $0.06/$0.24 na milion input/output tokenów, input <=20k bytes i max_tokens=4096. Przed requestem wymagane NEBIUS_CREDITS_CONFIRMED=yes. Ledger trzeba zachować i współdzielić między wszystkimi wywołaniami projektu. To nie odczyt rachunku lub salda Nebius.

## Dowody i deliverables

- README, MIT LICENSE, kod CLI/UI/backend/runner/provider, testy i .env.example.
- evidence/pages.json: base 6/9, A 3/9, B 9/9.
- evidence/money.json: base 1/9, A 4/9, B 9/9.
- evidence/intervals.json: base 5/9, A 6/9, B 9/9.
- Oba patche przechodzą smoke w każdym fixture. Holdout jest publiczny w repo, wykluczony z promptu; nie jest to niezależny blind benchmark.
- evidence/test-output.txt: wynik bieżącego sprawdzenia; końcowe podsumowanie poniżej.
- demo/preview.mp4: generowany podgląd **offline terminal replay + English TTS**, na podstawie prawdziwych zapisów CLI. Bez twarzy, kluczy i udawanego live call. To nie finalny screen-capture Nebius ani publiczny YouTube.
- docs/SUBMISSION-DRAFT.md: gotowy angielski draft z jawnymi brakami.
- docs/SUBMISSION-CHECKLIST.md: warunki release i złożenia, rzeczywiste źródła i terminy.

## Blokady i następny krok

Dostęp do sesji przeglądarki/formularzy jest potrzebny do rzeczywistej rejestracji i potwierdzenia Join. Brak konta/klucza/kredytów Nebius blokuje realny runtime test. Brak YouTube upload/access blokuje wymagany publiczny film. Nie jest to problem z kodem ani prośba do ownera o implementację. Techniczne części niezależne od kont są wykonywane dalej.

Po odblokowaniu: rejestracja i zapis prawdziwego hasła w OpenBao → konto/kredyty/key Nebius → realne wywołanie i raport → finalny screen-capture+TTS → public YouTube → komplet formularza → Submit i dowód statusu przed cutoffem. Nie zgłaszać wersji offline jako spełniającej wymóg runtime Nebius.

## Checkpoint

Chroniony .git jest read-only. Osobne lokalne metadane checkpoint.git w tym workspace, używane przez --git-dir i --work-tree, jak w hack-sweep. Logi sesji, sekrety, runtime ledger i metadane repo nie są śledzone. Publiczny eksport wyklucza TASK.md i WORK-STATE.md.

## Wynik publikacji i weryfikacji

- Publiczne repo: https://github.com/Schultzenator/patch-jury ; finalny publiczny commit `8641d85`.
- GitHub potwierdza isPrivate=false i licenseInfo=MIT License; default branch main.
- Finalny release: https://github.com/Schultzenator/patch-jury/releases/tag/v0.1.1-preview ; prerelease=true. Wcześniejszy v0.1.0-preview zachowany jako poprzednia wersja.
- Finalne assets mają stan uploaded. Hash SHA256 archiwum i filmu z API GitHub jest identyczny z lokalnym; dowód evidence/release.json.
- Preview: H.264 1280×720 + AAC, 116.635 sekund; obejrzane klatki początku i środka, bez clippingu tekstu. Nagranie terminalowe, nie screen-capture aplikacji z live Nebius.
- Publiczny eksport nie zawiera TASK.md, WORK-STATE.md, account-access.json, session logs, kluczy, tokenów OpenBao ani runtime ledger.
- `npm run build`: PASS. `PATCHJURY_INTEGRATION=1 python3 -W error::ResourceWarning -m unittest discover -s tests -v`: **12/12 PASS**. Naprawiono jawne zamykanie SQLite po wykryciu ResourceWarning podczas dodatkowej weryfikacji.
- Zainstalowano archiwum finalnego test buildu w czystym .state/final-build i uruchomiono jego testy: **12/12 PASS**, evidence/release-test-output.txt. Integralność opublikowanych assetów zweryfikowana przez sha256 z GitHub.
- HTTP smoke: HTML/JS/CSS/fixtures HTTP 200; prawdziwy POST porównania HTTP 200 i wyniki 6/3/9; live bez kredytów HTTP 400, bez inferencji. evidence/http-smoke.json.
- Trzy hashe report_sha256 zweryfikowane przez ponowne obliczenie. UI skompilowano i sprawdzono HTTP; brak dostępnej przeglądarki uniemożliwił wizualny test interakcji aplikacji.
- **Rejestracja Devpost i submission nadal NIE wykonane.** Repo/release nie są Submitted. Brak runtime call NVIDIA/Nebius oznacza niespełniony obecnie obowiązkowy wymóg konkursu. Brak public YouTube i finalnego screen-capture.
- Koszt inferencji nadal **$0**, brak płatnych kart i planów. Żadne zadanie automatycznego przyszłego submitu nie zostało zaplanowane.

## Ponowne sprawdzenie dostępu — 25.10, 08:56 Warszawa

- Wznowiono istniejący checkpoint, bez powielania ukończonego MVP. Logowanie IMAP ponownie potwierdziło istnienie p.szutt@neisse.ai. Nie użyto Gmail i nie wysłano wiadomości.
- OpenBao ponownie odczytany: brak credentials `devpost`, `nebius`, `youtube`. Nie utworzono pustych lub fikcyjnych wpisów. Dowód bez sekretów: `evidence/access-recheck.json`.
- CUA: inventory apps=0, browsers=0. Rzeczywiste próby utworzenia zakładki zarówno chrome, jak i iab zwróciły `Browser is not available`. Bezpośredni request do formularza rejestracji nadal HTTP 403. Publiczny odczyt strony przez web zwraca treść informacyjną; nie daje interaktywnej sesji do założenia konta.
- GitHub ponownie potwierdził publiczne repo z MIT, main `8641d85705eacf4efa0e5a0e47ff3395d036f3de`, prerelease v0.1.1-preview i dwa assets uploaded. Kod nie został zmieniony; nie powtarzano wcześniej zaliczonych testów.
- Aktualna blokada operacyjna: brak dostępnej przeglądarki do rejestracji i kont usług. Potrzebne jest udostępnienie sesji przeglądarki w narzędziu CUA; owner nie musi implementować kodu. Formularz eligibility i ewentualne żądanie dokumentu pozostają niezaobserwowane.
- Stan końcowy tego wznowienia: **NOT SUBMITTED**, inferencja 0 wywołań / $0, darmowe kredyty niepotwierdzone. Film preview jest offline, bez twarzy. Nie zaplanowano przyszłego automatycznego submitu.
