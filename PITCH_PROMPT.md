How to use: open a new chat inside the 25352_BBI project on claude.ai (so it can read our problem-framing notes), attach the files listed below, and paste everything under the line. Use Opus with high effort. Whoever builds the deck can change anything in the "Team's story" part; the "Forecast pack" part is ready to drop in.

Attach:
1. `outputs/results.md` (created by the model run)
2. A screenshot of the website map on a busy summer day, with the "57% / 2.8x chance" card visible (Cmd + Shift + 4 on Mac)
3. Photos from the lab: the team working with jellyfish
4. The website link: https://diegoa-ml.github.io/jelly-alert/

---

Make a slide deck for our midterm pitch in DTU course 25352 Blue Bioeconomy Innovation (19 October). Hard limit: **3 minutes spoken**.

## Audience

Not the teachers. Pitch as if the room is early-stage investors, coaches and mentors, potential customers and other startups. They want to know: is the problem real, who pays, does it work, can this team do it, and what could kill it.

## Required content

The course requires all seven, clearly visible:
1. Name of the product
2. Problem statement, relevant to as many people as possible
3. Who benefits and who is affected (specific stakeholders)
4. The solution: how our approach works
5. The value, in the hands of the people affected (bottom-up and top-down)
6. Team and our ability to make it happen
7. The open risk or unknown: the single biggest risk of our solution

## Part 1: The team's story (the team decides)

The team leads the pitch with its product. Current direction: **[PRODUCT, e.g. salt made from jellyfish]**. Leave every part of this open with [brackets] and short hints, and do not decide it for them:
- [Product name]
- [Problem we solve and for whom]
- [How we make it: one line on the process] + lab photos
- [Who buys it and why]
- [Team: who does what] + lab photos (real people with real jellyfish make this credible)
- [Biggest risk of the product: e.g. cost per kg, regulation, buyers]
- [One ask to the room]

Propose a slide order and a time budget that adds up to 180 seconds, with the forecast taking about 50 to 60 seconds of it (one content slide plus the live demo). Suggest where the forecast fits best, but let the team move it.

## Part 2: Forecast pack (ready to drop in)

**Role in the story.** The forecast is a tool that supports the product: it tells the team where and when to catch jellyfish. Every business that uses wild jellyfish as a raw material has the same first problem, which is that blooms come and go and move with currents. Jelly Alert turns that into a map: where the jellyfish will be, up to 10 days ahead. Use it as an argument under "solution" (how we get our raw material), "value" (we harvest where they are, not by searching) and "risk" (supply is the risk; this reduces it). Do not let it take over the pitch.

**Forecast slide (about 15 to 20 s).** Title suggestion: "We know where to catch them." Visual: the map screenshot. One big number from `results.md`: in both test seasons, the 20% of water the map flagged 5 days ahead held more than half of the real sightings (52% to 64%; a blind guess catches 20%). Under it, small: "Free public data. Tested on 2025 and 2026, seasons it never saw."

**Live demo slide (45 s).** The slide shows only the link https://diegoa-ml.github.io/jelly-alert/ (large), a QR code to it, and the text "45-second live demonstration" under it. Speaker notes = demo script: pick Moon jelly, 2026; point at the headline card; press play; point at blue dots (real sightings) landing in purple water (predicted); switch to Lion's mane. Fallback: if the internet fails, show the screenshot.

**Numbers: use only these, from `results.md`.** If a number is missing, write `[NUMBER]`. Never round up.
- Season check per species and season: "X of Y real sightings in the flagged 20% of water."
- AUC at 5 days ahead against a calendar-only guess: moon jelly is clearly ahead of the calendar; for lion's mane the gain is small, so the value there is mostly *where*, not *when*.
- What the model leans on most: salinity and time of year. That fits the July 2026 reports linking early blooms to warm water and changed salinity.

**Do not claim:**
- "A day earlier" because the AUC is higher. AUC measures ranking, not timing.
- "Cuts bloom problems by half." The check shows where sightings fell, not damage avoided. Safe: "The flagged fifth of the water held more than half of the sightings."
- More accurate than GoJelly (the EU Risk Map). GoJelly has not published a test against real sightings, so there is nothing to compare. Our edge: public data only, no need to find seabed polyp beds, a map for each day instead of monthly scenarios, tested on unseen seasons, two species, collects new sightings.

**The forecast's own risk** (for the risk slide, if the team wants it): almost all public sightings come from the coast, while harvesting happens offshore. The model scores lower on open-water sightings. Our own catches and reports from fishers will test it where the boats are.

**Optional problem facts** (use if they help the team's story):
- Jellyfish blooms cost affected fisheries up to 25% of catch and up to 34% of catch value (Pitt et al. 2025; Shen et al. 2024).
- July 2026: unusually early and heavy jellyfish occurrence across Danish waters, linked by KU researchers to record-warm water and changed salinity (DR, TV2, July 2026).

## Part 3: The forecast is bigger than this pitch (backup slide, not presented)

One backup slide, "One forecast, many users", for questions from investors about scale. The same map, with no extra data, serves:
- Jellyfish harvesters and processors (salt, fertilizer, food, collagen for cosmetics): where to source
- Fishers: where to avoid, to protect catch, gear and fuel
- Power plants, desalination and aquaculture: early warning for blocked water intakes and stung fish
- Municipalities, beaches and tourism: swimmer warnings
- Researchers and authorities: a tested, open bloom monitor that improves with every reported sighting

Point: the forecast is a platform the product sits on, and it can earn on its own later.

## Style

Short text on slides: at most 3 lines of body text or one visual. The talking goes in the speaker notes, at about 130 words per minute (about 390 words in total). No em dashes. Plain, confident, specific. Big numbers on slides, explanations in the notes.

At the end, give me the spoken word count per slide and in total, and confirm it fits 3 minutes.
