How to use: open a new chat inside the 25352_BBI project on claude.ai (so it can read our problem-framing notes), attach the files listed below, and paste everything under the line. Use Opus with high effort.

Attach:
1. `outputs/results.md` (created by the model run)
2. `outputs/skill_vs_lead_Cyanea_capillata.png` and `outputs/skill_vs_lead_Aurelia_aurita.png`
3. A screenshot of the website map on a busy summer day (Cmd + Shift + 4 on Mac)
4. The website link (paste it in the chat)

---

Make a slide deck for our midterm pitch in DTU course 25352 Blue Bioeconomy Innovation (19 October, feedback only, not graded). Hard limit: **3 minutes spoken**, so 6 main slides plus 2 backup slides for questions. Each main slide gets a time budget and speaker notes that fit it when read at a normal pace (about 130 words per minute).

Rules:
- Use only numbers from the attached `results.md` and the facts written below. Do not invent figures. If a number is missing, write `[NUMBER]`.
- Slides 4 and 5 are partly for my teammates (the fertilizer part). Put clear placeholders in [square brackets] with a short hint of what goes there, so they can fill them in. Keep their suggested subtitles, but they may change them.
- Short text on slides (max 3 lines of body text or one visual). The talking goes in the speaker notes.
- No em dashes. Plain, confident, understated wording.

Our project in one sentence: **Jelly Alert predicts where jellyfish will be in Danish waters, days ahead, so fishers can avoid them and harvesters can collect them, and we turn the collected jellyfish into fertilizer.**

Slides:

**1. Title (5 s)**
Title: Jelly Alert. Subtitle: "Knowing where jellyfish will be, and putting them to use." Team names: [NAMES].

**2. The problem (35 s)**
Suggested subtitle: "Fishers find jellyfish when the net is already full."
Facts to use:
- Jellyfish blooms cost affected fisheries up to 25% of catch and up to 34% of catch value (Pitt et al. 2025; Shen et al. 2024).
- Blooms move fast with currents and are usually detected only after time, fuel and gear are already committed.
- July 2026: unusually early and heavy jellyfish occurrence across Danish waters, linked by KU researchers to record-warm water and changed salinity (DR, TV2, July 2026).
- Free ocean data that could predict this (temperature, salinity, wind) already exists, but nobody connects it to a forecast for this use.

**3. Our forecast: Jelly Alert (45 s)**
Suggested subtitle: "Tested against what really happened."
Visual: the map screenshot. Small inset: the skill chart for lion's mane.
Facts to use:
- Learns from about 1,000 public sightings per species (GBIF) and the ocean and wind conditions before them (Copernicus Marine, ERA5), 2015 to 2024.
- Tested on the 2025 and 2026 seasons, which it never saw. Use from results.md: AUC at 5 days ahead vs. the calendar-only baseline, and the season check ("X of Y real sightings fell in the top 20% of predicted waters; chance would be 20%").
- One line on what is new: "Unlike the EU's GoJelly Risk Map, ours doesn't need to know where jellyfish start life on the seabed (polyp beds), and it is checked against real sightings."
- If the model does not beat the calendar baseline for a species, say so honestly in the notes and present it as what we learned.

**4. Our product: jellyfish fertilizer (40 s)**
Suggested subtitle: "From nuisance to nutrient." (teammates may change)
Placeholders: [What we make and how: dehydration process in 1 line], [Prototype status: photo of our dried jellyfish], [What is new compared with GoJelly, which already showed jellyfish fertilizer improves soil quality (CORDIS, EU project 774499)], [First test result or next test].

**5. How it fits together and who pays (35 s)**
Suggested subtitle: "One map, two customers."
Show a simple loop: forecast says where jellyfish will be → fishers avoid them (save catch, fuel, gear) → harvesters go there to collect → biomass becomes fertilizer.
Customers: fishers (subscription to the forecast), [fertilizer buyers: organic farms? garden market?], [cosmetics/collagen buyers, optional].
Placeholders: [price idea], [first customer we will interview].

**6. Next steps and what we want feedback on (20 s)**
Suggested subtitle: "What we will prove next."
- Interview fishers and Danmarks Fiskeriforening: is the problem still costly, would they pay, would they report sightings?
- Fisher reports fill our biggest data gap: today almost all sightings come from the coast, not where fishing happens.
- [Fertilizer next test].
- Ask the audience: [one specific question we want feedback on].

**Backup A (not presented): How we compare with GoJelly**
Table with rows: needs polyp-bed locations (GoJelly yes, ours no); checked against real sightings (GoJelly: not yet, authors state there was not enough data; ours: yes, 2025 to 2026); time (GoJelly: monthly scenarios from one simulated year, 2021; ours: specific dates 0 to 10 days ahead); species (GoJelly: moon jelly; ours: moon jelly and lion's mane); collects new observations (GoJelly no; ours yes). One line on their strength: GoJelly explains why blooms form; ours only finds patterns. Source: Cant et al. 2025, Journal of Applied Ecology, doi:10.1111/1365-2664.70186.

**Backup B (not presented): Limits**
Mostly coastal sightings; predicts where, not how many; relative likelihood, not a probability; prototype, not yet a live service.

At the end, give me the total spoken word count of the notes, and confirm it fits 3 minutes.
