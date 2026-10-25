# Submission release gates

Target: 28 October 2026. Internal cutoff: 29 October 23:00 Europe/Warsaw. Official deadline: 30 October 18:00 Europe/Warsaw (17:00 UTC). Do not wait for the hard deadline.

1. Owner mailbox existence has been verified by successful IMAP login; use the selected owner's business email. Do not invent identity, age, residency, affiliations, or event attendance.
2. Create/sign into the real Devpost account; save its password only under `factory/credentials/devpost` in OpenBao. Verify the email. Confirm actual Join Hackathon status.
3. Inspect individual eligibility: age of majority, residence, sponsor/judge/employer/household conflicts and other official exclusions. If identity evidence is requested, record the exact field and have the owner supply it securely. No identity-upload requirement was observed from the public rules.
4. Obtain the owner's Nebius account, free credits and key; save credentials under `factory/credentials/nebius` in OpenBao. No card or paid plan activation. Confirm actual balance before setting `NEBIUS_CREDITS_CONFIRMED=yes`.
5. Run live inference, retain the unedited report and token usage, assess whether generated cases distinguish the patches, update README and feedback with actual observations.
6. Run `npm ci && npm run build` and `PATCHJURY_INTEGRATION=1 python3 -m unittest discover -s tests -v`.
7. Publish public MIT repository and downloadable test build. Verify a clean clone installs and runs. Keep test build accessible through judging (15 December 2026).
8. Record final application screen capture with English TTS, no owner face. Show the real Nebius runtime call and evidence. Upload a public YouTube video under 3 minutes. Preview offline terminal footage is not final evidence.
9. Complete the description, track, public repository, working test build, video and truthful tools feedback fields on Devpost. Check actual form-specific questions and eligibility declarations. Do not invent answers.
10. Submit before the internal cutoff and verify the project shows Submitted; retain the submission URL and status evidence. Draft/save/Join are not Submitted.

Official sources checked 25 October 2026:
- https://nebiusglobalaihackathon.devpost.com/rules
- https://nebiusglobalaihackathon.devpost.com/
- https://tokenfactory.nebius.com/api/public/models_info

No unattended future run or submission is scheduled by this repository. Dates here are targets, not evidence of an active scheduler.
