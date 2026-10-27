# Patch Jury — submission kit

## Status dla PW — 27.10.2026

Offline MVP i materiały są gotowe lokalnie. **Live Nebius nie zostało zweryfikowane**; nie zgłaszaj trybu offline jako spełnienia wymogu runtime. Devpost: zarejestrowani; Builder Program: approved (status przekazany przez ownera). Nie otwierano konsoli ani formularza zgłoszenia w tej sesji.

- Deadline roboczy PW: **30.10, 18:00 Europe/Warsaw**. Regulamin podaje 30.10, 10:00 PDT = **18:00 Warszawa / 17:00 UTC**. Cutoff wewnętrzny: 29.10, 23:00 PL.
- Repo: https://github.com/Schultzenator/patch-jury
- Dotychczasowy test build: https://github.com/Schultzenator/patch-jury/releases/tag/v0.1.1-preview — **nie zawiera obecnego lokalnego commita**.
- Nowy test build: [demo/submission/patch-jury-submission.tar.gz](demo/submission/patch-jury-submission.tar.gz), przygotowany do późniejszego udostępnienia przez PW.
- Film: [80 s offline screen capture](demo/submission/submission-offline.mp4); brak publicznego URL YouTube.
- Kluczy i promo code nie dołączamy do publicznych materiałów.

## Co robi PW

1. Po własnym logowaniu GitHub do konsoli zastosuj przekazany kod Token Factory ($25; termin 31.12.2026), potwierdź saldo i utwórz klucz. Nie potrzeba LangSmith ani Tavily do tego MVP.
2. Wykonaj instrukcję **Live NVIDIA inference on Nebius** w [README](README.md). Wprowadź klucz w ukrytym promptcie shell, ustaw ENV, uruchom `--live --output live-report.json`; bez zmian kodu. Zrestartuj serwer i wybierz live w UI.
3. Sprawdź raport: `provenance.mode=live`, NVIDIA model, request ID, usage, challenge inputs i wyniki. Zachowaj autentyczny raport. Brak rozróżnienia przez model też jest wynikiem — nie zastępuj go authored jako live.
4. Nagraj live ujęcia według [scenariusza](demo/README.md); usuń placeholder i zmień narrację wyłącznie zgodnie z faktycznym wynikiem. Udostępnij aktualny commit/test build i publiczny film YouTube. Te działania nie zostały wykonane w tej sesji.
5. Wklej pola poniżej do Devpost, uzupełnij rzeczywiste URL i feedback live. Zweryfikuj eligibility i aktualne pola formularza. Submit oraz potwierdzenie Submitted pozostają po stronie PW.

## Pola Devpost

**Project name:** Patch Jury — Evidence before merge

**Elevator pitch:** Two patches pass the smoke test. Patch Jury finds boundary counterexamples and turns them into executable evidence for a maintainer's decision.

**Track:** Coding and Agentic Engineering

**Tags / Built with:** Python, TypeScript, Docker, NVIDIA Nemotron, Nebius Token Factory, OpenAI-compatible API, agentic testing, developer tools, regression testing.

**Source code:** https://github.com/Schultzenator/patch-jury — PW publikuje aktualny lokalny commit przed wskazaniem go sędziom.

**Try it out / test build:** [PW: URL aktualnego publicznego archiwum testowego]. Wersja lokalna jest gotowa; nie wpisuj ścieżki dyskowej do Devpost.

**Video:** [PW: public YouTube URL po nagraniu live]. Nie wklejaj placeholdera jako finalnego URL.

## Description — English, two paragraphs

Patch Jury helps maintainers distinguish a root-cause fix from a patch that only passes the obvious smoke test. Choose one of three original regression fixtures—page counts, decimal rounding, or interval overlap—and compare a buggy base with two competing fixes. A juror workflow proposes boundary inputs, a trusted specification oracle computes expected answers, and isolated Docker containers execute each version. The result is an inspectable verdict with counterexamples, per-group pass counts, source hashes, and downloadable JSON evidence. A unique patch passing the complete evaluated suite is supported; ambiguous evidence stays inconclusive, with the merge decision left to a human.

The live adapter uses NVIDIA Nemotron through Nebius Token Factory's OpenAI-compatible inference endpoint to generate test inputs, while validation, execution, and verdict logic remain deterministic. The model never supplies executable code or expected answers and does not see the competing patches or held-out cases. The current offline demo uses explicitly labeled hand-authored inputs; authenticated Nebius inference is pending the owner's API key and has not yet been demonstrated. Python, TypeScript, and a durable call-budget ledger keep the workflow small and auditable. These synthetic examples demonstrate the review process, not general correctness or benchmark accuracy.

Po potwierdzeniu live PW zastępuje zdanie o pending faktem: model, data, request ID i zaobserwowany wynik; nie deklaruje skuteczności bez dowodu.

## Testing instructions — English

Install Python 3.12+ and Docker on Linux. Extract the test build, run `docker pull "$(cat runner-image.txt)"`, then `python3 -m patchjury --serve`. Open http://127.0.0.1:8000, leave **Authored examples · offline** selected, and click **Compare patches**. Inspect the verdict, smoke/challenge/held-out counts and counterexamples; export the JSON evidence. Repeat with decimal rounding and interval overlap. No app account is required. Live mode requires a server-side Nebius key and confirmed credits as documented in README. The test build supports bundled fixtures only.

## Wymagania regulaminowe — kontrola PW

Sprawdzone 27.10 w [oficjalnym regulaminie](https://nebiusglobalaihackathon.devpost.com/rules):

- Działający runtime Token Factory lub AI Cloud oraz NVIDIA open source model. **Adapter/mock/offline nie wystarcza; realny runtime jest nadal bramką.**
- Publiczne repo open source z licencją, źródłami, assetami i README; URL działającego demo lub test buildu dostępnego bez opłat przez ocenianie do 15.12.2026.
- Angielski opis, instrukcje, wybrany track i feedback o użytych narzędziach.
- Film pokazujący działającą aplikację, poniżej 3 minut, publiczny na YouTube; prawa do użytych materiałów. Projekt jest w tracku Coding, bez sprzętu Physical AI.
- PW potwierdza pełnoletność, miejsce zamieszkania, brak konfliktów/wykluczeń, prawa do pracy i upoważnienie reprezentanta. Podać rozwój w okresie konkursu; AI coding assistance ujawnione w README. Rejestracja nie oznacza Submitted.

## Tools feedback — truthful English draft

The public model catalog made model IDs and pricing inspectable before inference. Token Factory's OpenAI-compatible request shape let us keep the juror adapter small and separate from deterministic test execution. We would welcome a documented machine-readable stability policy for model IDs and pricing metadata. Authenticated latency, output quality and credit activation have not yet been evaluated; the owner will add those observations after the live smoke test. We did not use AI Cloud, fine-tuning, LangSmith or Tavily in this MVP.
