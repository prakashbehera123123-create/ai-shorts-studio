# Research run 2026-11-23: view-velocity shortlist (AWAITING OWNER PICK)

Owner change for this run: rank by where niche Shorts get the most views fast and are liked most, focused on AI, agents,
GenAI, ML and system design. Evidence: `velocity_evidence.md` (YouTube `/results` is robots-disallowed, so only hashtag,
channel and Shorts pages were read by hand). Contract: `candidates.json` (`python -m studio research check` passes, no warnings).
Score slot "freshness" = view-velocity evidence this run. All videos are Hinglish.

**Owner decision (2026-11-23): C01 + C06 approved. Language changed to ENGLISH (owner: "let's not take hindi").
Professional hook, intro and outro; hooks modelled on the reference reels listed under each candidate's `velocity_refs`.**

## Queue for 2026-11-24 (owner: reuse this research, do not research again)
Remaining in rank order: C03 (close to C01 — space them out or reframe), C02 (contested; close to C01), C07 (near-duplicate of
11-22), C05, C08, C04 (open the CCC primary first), C10 (off-focus), C09 (verify the Redis FAQ wording).
Before production: re-check freshness and flagged sources, then let the owner pick 2.

| Rank | id | Topic | Velocity evidence (niche) | Evidence | Score |
|---|---|---|---|---|---|
| 1 | C01 | 1 aur 1 = 11? Why AI fails simple math: tokens | TechAkshay "AI fails" Hinglish Shorts 77K–280K views/day | high (arXiv 2402.14903, 2410.19730) | 4.7 |
| 2 | C03 | Why AI lies confidently: the student who always guesses | Same "AI exposed" pattern | high (OpenAI 2025-09-05) | 4.5 |
| 3 | C02 | Why AI falls for riddles: one irrelevant line, up to 65% drop | Hotel-riddle Short ~191K/day | medium (Apple arXiv 2410.05229; contested replication) | 4.4 |
| 4 | C06 | Hundreds of AI agents built a browser in a week: why locks failed | "Agent built a browser" ~21K/day, 22K likes | medium (Cursor blog 2026-01-14, vendor-reported) | 4.3 |
| 5 | C07 | Chatbot vs workflow vs agent: when NOT to build an agent | Comparison Short ~17K/day | high (Anthropic) — near-duplicate of 11-22 | 4.2 |
| 6 | C05 | Free Wi-Fi is not the danger reels say: the fake site is | Free-Wi-Fi fear Short ~30K/day, 23K likes | high (FTC) — outside AI core | 4.1 |
| 7 | C08 | Brain surgery on an AI: how one fact gets rewritten (ROME) | Hinglish research Short ~4.8K/day | high (arXiv 2202.05262) | 3.8 |
| 8 | C04 | Can a peace-sign selfie leak your fingerprint? | Selfie-gesture Short ~206K/day, 21K likes | **flagged: no primary opened yet** | 3.8 |
| 9 | C10 | VR goggles for mice | 64M views, ~1.49M/day | high — off-focus (science) | 3.6 |
| 10 | C09 | Redis runs on one thread. Why is it so fast? | ByteByteGo evergreen, <1K/day now | medium (FAQ wording to verify) | 3.4 |

## Recommendation
- The tool's auto-pick is C01 + C03, but **both answer "why AI gets things wrong"**, so they are near-duplicates.
- Recommended pair: **C01 (tokens, ML mechanism)** and **C06 (agent swarm, agentic + system design)**. They come from
  different patterns, both fit the robot/desk 3D world, and neither repeats the 11-22 videos.
- Alternative: C03 in place of C01 (stronger "aha", vendor-sourced), or C02 if the owner accepts a contested finding.

## Approval needed
Reply with two ids (for example "C01 + C06"). Then: `research apply`, set APPROVED_TOPIC, and run produce-short for each, Hinglish, cloned voice, best-of-3 takes, 165 wpm floor, `auto_sfx` false, hook + "Aise hi … concepts ke liye, follow karo".
