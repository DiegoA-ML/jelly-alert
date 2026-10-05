How to use: open a new chat inside the 25352_BBI project on claude.ai (so it can read our problem-framing notes), attach the files listed below, and paste everything under the line. Use Opus with high effort.

Attach:
1. `outputs/results.md` and `outputs/feature_selection.md` (created by the model run)
2. A screenshot of the website map on a busy summer day, with the "57% / 2.8x chance" card visible (Cmd + Shift + 4 on Mac)
3. Photos from the lab: my teammates working with the jellyfish (from them)
4. The website link: https://diegoa-ml.github.io/jelly-alert/

---

Make a slide deck for our midterm pitch in DTU course 25352 Blue Bioeconomy Innovation (19 October). Hard limit: **3 minutes spoken**.

**Audience.** Do not pitch to the teachers. Pitch as if the room is early-stage investors, coaches and mentors, potential customers (fishers, harvesters, buyers of jellyfish products) and other startups. They want to know: is the problem real and big, who pays, does it work, can this team do it, and what could kill it.

**One company, two halves.** We are one team with one story. The forecast finds the jellyfish; the lab turns them into a product. The product is [PRODUCT: jellyfish fertilizer or jellyfish salt, teammates decide]. Do not present two projects. The link: anyone who wants to use jellyfish as a raw material has the same first problem, which is knowing where and when they will be. Jelly Alert solves sourcing; the lab solves what to make. The same forecast also helps fishers avoid them. Write every slide so it works whether the product is fertilizer or salt: use [PRODUCT] as the placeholder.

**Required structure** (each one must be clearly present; the course requires all seven):
1. Name of the product
2. Problem statement, relevant to as many people as possible
3. Who benefits and who is affected: specific, named stakeholders
4. The solution: how our approach works
5. The value: in the hands of the people affected. Show both directions: bottom-up (fishers and harvesters use it and feed it with their own sightings) and top-down (authorities, municipalities, EU blue-bioeconomy programmes that want jellyfish blooms monitored and used)
6. Team and our ability to make it happen
7. The open risk or unknown: the single biggest risk of our solution

**Slides and time budget** (total 180 s; speaker notes must fit at about 130 words per minute, so about 390 words in total):

| # | Slide | Time | Content |
|---|---|---|---|
| 1 | Name | 10 s | "Jelly Alert". One-line promise, e.g. "Know where jellyfish will be, days ahead. Then put them to use." Team names: [NAMES]. |
| 2 | Problem | 30 s | Facts below. Make it relevant to many: fishers, swimmers and beaches, power-plant and aquaculture water intakes, and a growing jellyfish-product industry with no reliable supply. |
| 3 | Who is affected | 20 s | Named stakeholders: Danish fishers and Danmarks Fiskeriforening; jellyfish harvesters and [PRODUCT] buyers [e.g. organic farms / food or salt buyers]; municipalities and beach operators; Fiskeristyrelsen and marine researchers. One line each on what they lose or gain. |
| 4 | Solution | 30 s | Two-part visual: (a) forecast: public sightings + daily ocean and wind data, then a model, then a map 0 to 10 days ahead; (b) lab: harvested jellyfish, then [PROCESS, 1 line], then [PRODUCT]. One photo from the lab here. |
| 5 | Live demo | 45 s | The slide shows only the link https://diegoa-ml.github.io/jelly-alert/ (large), a QR code to it, and under it the text "45-second live demonstration". Speaker notes = a demo script: pick Lion's mane, 2026; point at the headline card; press play; point at blue dots landing in purple water; switch to Moon jelly. Add a fallback line: if the internet fails, show the attached screenshot. |
| 6 | Value | 20 s | Bottom-up and top-down, as described above. One line on why ours is cheap to run: public data only, no survey ship, no sensors, no need to find seabed polyp beds. |
| 7 | Team | 15 s | Lab photos of my teammates working with jellyfish (they make this credible). Who does what: [NAME] forecast and data; [NAMES] [PRODUCT] lab work; [any domain contacts]. |
| 8 | Risk and ask | 10 s | The biggest risk (below) and how we will test it next. End with one ask to the room: [e.g. "introductions to a fisher or harvester who will test it this season"]. |

Backup slides (not presented, for questions): A. How we compare with GoJelly. B. How we tested it (training vs test years, the calendar baseline, the feature selection on training years only). C. Limits.

**Numbers: use only these, from the attached files.** If a number is missing, write `[NUMBER]`. Never round up and never invent.
- The season check (strongest, easiest to understand): on each 2025 and 2026 test season, X of Y real sightings fell inside the 20% of water the map flagged 5 days earlier; a blind guess would catch 20%. Take X, Y and the percentages from `results.md` (currently 52% to 64%, about 2.5 to 3 times chance). Good wording: "The map flags one fifth of the water, and that fifth held more than half of the real sightings, in two seasons it had never seen."
- AUC at 5 days ahead vs the calendar baseline, per species, from `results.md`. Moon jelly is clearly ahead of the calendar. For lion's mane the gain over the calendar is small: say so in the backup slide, and say that its value is mostly in where, not when.
- What the model leans on most: salinity and time of year. That fits the July 2026 reports linking early blooms to warm water and changed salinity.

**Do not claim** (these are wrong, and investors will ask):
- That beating the calendar by a few AUC points means "a day earlier". AUC measures how well it ranks places and days, not how early it is.
- That it "cuts bloom problems by half". The season check shows where sightings fall, not damage avoided. Fine to say: "If you avoid the flagged fifth of the water, you would have avoided more than half of the encounters seen in those seasons, according to public sightings."
- That we are more accurate than GoJelly. GoJelly has not published a validation against real sightings, so there is nothing to compare. Our edge is different: no need to know polyp beds, daily dates instead of monthly scenarios, tested on unseen seasons, two species, and it collects new sightings.

**Facts for the problem slide** (use only these):
- Jellyfish blooms cost affected fisheries up to 25% of catch and up to 34% of catch value (Pitt et al. 2025; Shen et al. 2024).
- Blooms move fast with currents and are usually noticed only after time, fuel and gear are committed.
- July 2026: unusually early and heavy jellyfish occurrence across Danish waters, linked by KU researchers to record-warm water and changed salinity (DR, TV2, July 2026).
- The free ocean data that can predict this already exists, but nobody turns it into a forecast for the people who need it.

**The biggest risk** (slide 8): almost all public sightings come from the coast, while fishers and harvesters work offshore. The model scores lower on open-water sightings (see `results.md`), so how well it holds up where the boats are is the open question. How we test it: fishers and harvesters report sightings in the app this season, and we score the forecast on them. If [PRODUCT] has its own bigger risk (cost per kg, regulation, buyer demand), teammates add one line.

**Style.** Short text on slides: at most 3 lines of body text or one visual. The talking goes in the speaker notes. No em dashes. Plain, confident, specific. Big numbers on slides, explanations in the notes. Use the lab photos generously; real people with real jellyfish make this believable.

At the end, give me the total spoken word count of the notes per slide and in total, and confirm it fits 3 minutes.
