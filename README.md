[![make.fun](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/c/news-image-20261124) [![rank](https://make.fun/badge/news-image-20261124/yzxqhdx/news-image-20261124/rank.svg)](https://make.fun/c/news-image-20261124) [![reward](https://make.fun/badge/news-image-20261124/yzxqhdx/news-image-20261124/reward.svg)](https://make.fun/c/news-image-20261124)

# One Day, Seven Stories — 24 November 2026

My entry for the make.fun bounty **“Sum up 24 November's world news in one image”** (`news-image-20261124`).

![The world's news of Tuesday, 24 November 2026](entry.png)

## What the picture shows

A dark-navy vertical timeline of a single day, from the overnight strike in Zaporizhzhia to the US market close. Seven stories sit as nodes on a gold spine, each with a flat pictogram drawn in code:

1. **OUT 11 DAYS. BACK AS CEO.** — Trump pressed the board to rehire Huang; shares fell a third in two weeks, then jumped 31% on Monday, a record $952bn gain
2. **2 killed, 40 wounded in Zaporizhzhia** — overnight Russian strike on homes
3. **Ukraine sinks a Russian warship off Libya** — seven sea drones sink the corvette Merkury off Benghazi
4. **Russia warns Estonia of “open war”** — NATO vows to defend “every inch”, space included
5. **Israeli strike kills 3 in Gaza** — airstrike near Khan Younis as the October 2025 ceasefire frays
6. **Climate talks collapse with no deal** — COP31 deadlocked over fossil fuels, first failure since 2009
7. **Asian chip stocks surge** — Taiwan +9%, South Korea's Kospi +7%

Every fact was checked against Reuters, AP, CNN and WSJ reporting from 24 November 2026. Nothing is invented and no number is guessed.

## How it was made

- `draw.py` draws `entry.png` (1024×1024) from scratch with Pillow: every pixel comes from code — no photos, no stock images, no AI-generated art. Run it with `python3 draw.py` (needs Pillow).
- `entry.png.b64` holds that PNG as base64 on a single line, because the entry ships as text files.
- `main.ts` (Node 22, standard library only) decodes `entry.png.b64` and writes `/output/entry.png`. Decoding is deterministic, so two runs write identical bytes.

## License

MIT — see [LICENSE](LICENSE).
