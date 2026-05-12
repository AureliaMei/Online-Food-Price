# Thesis Defense Script — Content-Rich Edition
**Hedonic Price Decomposition and Promotional Erosion on Online Prices — A Case Study on Winmart**
Trần Hiếu My · Business Analytics 64 · NEU 2026
Target time: **~12 minutes** at ~140 wpm · 20 main slides + 8 appendix slides for Q&A. Slides 10–11 present the regression *numbers*; 
 Slides 12–13 then explain *why*. Same numbers-then-interpretation split for Slides 14 and 15. Slide 16 (Diagnostics) gets a one-sentence intro and a click-through.

---

## How to use this script

For each slide there is (a) a one-line **purpose** in italics, (b) a **stage direction** in square brackets where helpful, and (c) the spoken text — written to be *said*, not read.

The depth, examples, and theoretical anchoring of the long practice script are preserved; the cuts are in repetition and in the parts you can let the slide do for you. **Bold** lines are the spine — the load-bearing transitions you should not skip.

---

# PART ONE — OPENING

## SLIDE 1 — Title (≈ 15 sec)
*Purpose: identity. Audience reads, you greet.*

[Stand still. Eye contact with the chair, then sweep across the panel. Pause two seconds before speaking.]

> Good morning, distinguished members of the council. I'm Trần Hiếu My, defending my thesis *Hedonic Price Decomposition and Promotional Erosion on Online Prices — A Case Study on Winmart*, supervised by Dr. Nguyễn Mạnh Thế.

---

## SLIDE 2 — Table of Contents (≈ 5 sec)
*Purpose: mental map. Move quickly.*

> The speech will follow five parts as you can see on the slides. *With that knowledge, I shall start with the introductory puzzle.*

---

# PART TWO — INTRODUCTION

## SLIDE 3 — Two Prices, One Product (≈ 45 sec)
*Purpose: the hook. Anchor the entire thesis in one observable fact.*

[Click to advance. Point at the Vinamilk product card. Hold for a beat.]

> On the left is a product every household here recognizes — a one-litre carton of Vinamilk fresh milk. Open the Winmart website right now and you will see *two prices*. The marked price, which has been crossed out, and The checkout price with a gap of twelve and a half percent.
>
> The numbers on the right are the scope of this thesis: **over two thousand two hundred unique products**, recorded over **eighty-eight consecutive days** and **ten food categories**.
>
> **The observation begins as the gap between the two prices is not random. It varies systematically and that variation is what I set out to measure.**

---

## SLIDE 4 — Research Question & Objectives (≈ 35 sec)
*Purpose: the question on screen, three objectives in your voice.*

[Read the question slowly. Then point at each numbered card in turn.]

> That exact research question is *"What product attributes generate price premiums in Vietnamese online grocery, and to what extent do promotional pricing strategies erode those premiums?"*
>
> Thus, three objectives follow suitly: **Identify** which attributes generate statistically significant premiums. **Measure** how promotional discounts erode those premiums between sticker and checkout. **Compare** how the structure varies across categories.
>
> **Identify, measure, compare. The rest of the talk serves to achieve these RQs.**

---

# PART THREE — LITERATURE & THEORY

## SLIDE 5 — Hedonic Theory: Goods as Attribute Bundles (≈ 60 sec)
*Purpose: the 50-year lineage in three steps. Audience tracks the dates while you carry the meaning.*

[Walk left-to-right across the three dated boxes. One sentence per box; do NOT read every line.]

> Firstly, the basis of my thesis was the Hedonic theory with fifty years of lineage.
>
> It all started with sir **Lancaster, 1966** — where he proposed that consumer utility comes from *attributes, not goods*. A consumer buying milk is buying volume, calcium, brand reputation, and shelf-life — not "milk" as an indivisible unit.
>
> 8 years later, **Sherwin Rosen**, formalized it. In market equilibrium each attribute carries an *implicit price*, recoverable by regressing observed prices on observed attributes. *This is what I estimate — a Rosen first-stage price function. I describe equilibrium implicit prices the Winmart shelf reveals; and do not claim to identify structural demand or supply.*

---

## SLIDE 6 — Brand Equity: The Four-Quadrant Typology (≈ 65 sec)
*Purpose: the framework picture. Audience reads quadrants while you explain why brand has to be split.*

[Point at the centre of the 2x2, then each quadrant in turn. End on the operationalization panel on the right.]

> However, the standard hedonic regression treats "brand" as a single dummy. I argue that is *too coarse*.
>
> Drawing on **Aaker's 1991** perceived quality and **Keller's 1993** customer-based brand equity, I cross two orthogonal dimensions — recognition on one axis, price tier on the other — into four quadrants. **Household Giants** — high recognition, low price. Vinamilk fresh milk. Hảo Hảo noodles. **Premium Specialists** — high on both. **Generic Branded** — low on both. **Niche Premium** — low recognition, high price.
>
> Operationally, four hierarchical variables — the last isolating WinEco, the child brand of Win ecosystem.
>
> **With this separation, the central finding has become much more robust.**

---

## SLIDE 7 — Online Prices as a Reliable Data Source (≈ 15 sec)
*Purpose: one sentence to defuse the "it's just a website" worry, then advance.*

[One sweep across the four cards. Keep moving.]

> Meanwhile, the choice to use online prices is based on **Cavallo 2017**. He documents that across fifty-six countries, seventy-two percent of online and offline prices are identical. Together with Schipmann's single-retailer logic and Hülten's case for daily data, the four pillars on screen support the design.

---

# PART FOUR — METHODOLOGY

## SLIDE 8 — Data: Winmart, 88 days, 10 categories (≈ 30 sec)
*Purpose: establish the pipeline as personally-built craft. Slide carries the schema and category list.*

[Sweep along the pipeline diagram once. Don't read the schema or the category list — they're on screen.]

> The data was collected by a pipeline — **ten scraping robots** operating daily through an authenticated API across eighty-eight consecutive days. The schema and the ten parent categories are on the slide.
>
> The final dataset has roughly two thousand two hundred products, time-averaged across the panel.
>

---

## SLIDE 9 — Hedonic Specification & Dual-Price Design (≈ 75 sec)
*Purpose: the equation AND the erosion formula on one slide. This is the conceptual hinge — slow down.*

[Point at the equation, then at the four KPI boxes, then at the erosion formula at the bottom. Pause after the erosion definition.]

> The equation here regresses log unit price on ten product-level features — *brand bundle*, *origin and claims*, and *physical attributes* — with forty sub-category fixed effects and cluster-robust standard errors. Sample is two thousand two hundred and three products; adjusted R-squared is **zero point six four** in specifications of **both** marked and final prices.
>
> **Erosion**, in this thesis, is the percentage change in each coefficient between the two. 
>
> **Having run the model, I quickly came to the following findings:**

---

# PART FIVE — RESULTS

## SLIDE 10 — Pooled Hedonic Results (≈ 50 sec)
*Purpose: pure regression output. Read the numbers — leave the interpretation for Slide 12.*

[Walk to the slide and physically point at the three highlighted attributes — premium, high recognition, log pack size. Then point at the right-hand callouts.]

> The first plot shows the pooled coefficients with ninety-five percent confidence intervals — *gold for marked price, blue for final*. 
>
>Three coefficients stand out.
>
> **Premium tier** sits around plus zero point four three — the largest attribute premium in the model.
>
> **High recognition** brings **discounts**, with coefficient being around minus zero point two six.
>
> **Log pack size** is minus zero point three nine. Meaning for every 10% increase in the pack size, there is 3.8% decrease in unit price.
>
> *While the pooled regression tells the story from a single point, the dual-price design opens a second view.*

---

## SLIDE 11 — Promotional Erosion of Attribute Premiums (≈ 65 sec) — *the climax*
*Purpose: pure dual-price numbers. Read the table; land the headline. Reasons come on Slide 13.*

[This is your money slide. SLOW DOWN. Pause before the headline sentence. Let it land.]

>
> Here the table compares each coefficient between the marked and final regressions.
>
> **Premium tier** is *stable* — absolute erosion one point seven percent. The markup is fully transmitted from sticker to checkout.
>
> However, **Branded** is *eroded* — plus fifty point six percent. **Half of the brand-name premium evaporates between sticker and checkout.** *(Pause.)*
>
> And the most striking single transformation — **WinEco**, the house brand. While Sticker price shows *insignificant* effect, influence is 4x by the time it reachs checkout *(Pause.)*
>
> *(Look up.)* **promotion erodes brand-name premiums by half — but leaves price-tier premiums fully intact.**
>
>
> **Now — what do these numbers mean?**

---

## SLIDE 12 — Finding 1: Price-Tier Dominates and Pack Size Matters (≈ 55 sec)
*Purpose: interpret the price-tier and pack-size numbers from S10–S11. Why price-tier survives — and the practical lesson on pack size.*

[Open with the why. Walk through the bar chart on the left. End on the practical advice.]

> *Why* does the price-tier premium survive promotion almost untouched?
>
> The interpretation comes from **Varian's 1997 versioning model**. A retailer serving consumers with heterogeneous willingness-to-pay maintains *distinct price tiers* as a deliberate segmentation tool. The premium tier's value *depends on contrast* with their discounted counterparts. Discounting it would *collapse the very signal that justifies its margin*.
>
> Meanwhile, pack sizes' influence stems from economy of scale. Larger pack sizes yield roughly *three point eight percent unit-price savings per ten percent increase in pack size*. Which when looks from the shopper's perspective, **If you can buy more in one go, you will save more over the long run.** Buying too little too frequently slowly kills the wallet.
>
> *That is what the price-tier and pack-size numbers mean for a Hanoi household budget.*

---

## SLIDE 13 — Finding 2: Brand-Name Premiums Erode (≈ 55 sec)
*Purpose: interpret the brand-name and WinEco numbers from S11. The Keller logic, the WinEco illustration, and the split lesson for customers and businesses.*

[Open with the why. Walk through the WinEco contrast. End on the customer-vs-business takeaway.]

> On *Why* does brand-name erode by half?
>
> The interpretation comes from **Keller's 1993 customer-based brand equity**. High-awareness brands work as *promotional anchors*. Recognition draws traffic onto the platform; the premium *need not be large on the shelf*, because the discount delivers the value at checkout.
>
> WinEco pushes that logic to its limit — with significantly more frequent discounts. A *twenty-two-percentage-point gap* avoids the shelf-price stigma of a cheap house brand while delivering loss-leader pricing once the consumer is committed.
>
> Two real-life lessons follow — one for each side of the platform. **Customers** should know brand-name is largely a promotional vehicle. **Businesses** should focus on their *product positioning as a stable differentiator*.

---

## SLIDE 14 — Per-Category Heterogeneity (≈ 50 sec)
*Purpose: pure regression output, by category. Read the heatmap; leave the "why" for Slide 15.*

[Don't read the heatmap cell-by-cell. Call out the two highest-contrast cells, then the health-claim pattern.]

> The third finding tackles the *comparison across categories*.
>
> The heatmap shows hedonic premiums estimated separately within each parent category. Take the import-premium column on the left.
>
> **Vegetables and Fruit** — dark red — has an import coefficient so significant that Imported produce trades at almost *double* the unit price of domestic.
>
> While **Processed Food** having Same attribute, Opposite signs.
>
> Health claims show the same kind of patchiness. They are statistically significant *only* in **Spices** and **Fresh Produce**, and indistinguishable from zero in snacks, frozen, and processed food.
>
> *Why does the same attribute carry opposite signs in different categories? *

---

## SLIDE 15 — Finding 3: Category Heterogeneity is Systematic (≈ 55 sec)
*Purpose: interpret the heterogeneity numbers from S14. Why opposite signs — and what it means in real Vietnamese shopping.*

[Open with the why. Walk through the consumer logic. End on the real-life implication.]

>
> The interpretation rests on three pieces of literature. **Mergenthaler and co-authors, 2009**, document Vietnamese willingness-to-pay of around *sixty percent* for low-residue attributes in fresh produce because Food-safety concerns are most salient there.
>
> **Bell and co-authors, 2021**, confirm this systematically — food values in peri-urban Hanoi vary by category. Credence attributes are not uniformly valued; *context determines the premium*.
>
> But the *opposite* logic applies in processed food. Imported processed food carries a *negative* premium because well-established domestic brands dominate — *imports signal unfamiliarity and unnecessary risk*, not quality and convenience. When a consumer cannot inspect pesticide residue on a tomato, "imported" carries information; when the same consumer is buying their familiar Hảo Hảo noodles, "imported" carries *doubt*.
>
> **The geography is the substantive finding — not noise.**

---

## SLIDE 16 — Diagnostics & Robustness (≈ 8 sec)
*Purpose: one-sentence reassurance, then click through. The slide does the work.*

[Advance, pause one beat so the council can scan the four cards, advance again.]

> **All four standard diagnostics pass — multicollinearity, heteroskedasticity, influence, and temporal stability.** *(Advance.)*

---

# PART SIX — DISCUSSION & CONCLUSION

## SLIDE 17 — Recommendations (≈ 30 sec)
*Purpose: the slide carries four audiences; the speech surfaces only the consumer rule and the future-research roadmap. The business and policy lessons already came out on Slides 13 and 14.*

[Gesture at the consumers card and the future-research card; the council can read the rest.]

> Due to a lack of time, I will focus on Two lessons.
>
> **For consumers** — *price tier is a stronger savings signal than brand name*, because brand get discounted and product-specific premiums don't.
>
>And Pack size is the most discount-resistant savings of all.

---

## SLIDE 18 — Limitations (≈ 25 sec)
*Purpose: honest scope. Three load-bearing limits.*

[Read with composure — limitations honestly disclosed are a strength.]

> Limitations also leave room for improvements to future researches.
>
> **Single-retailer external validity** is restricted *by design* — it holds platform, logistics, and presentation constant. Multi-retailer extension is the headline future-research priority.
>
> **No transaction volumes** — so the analysis is very limited and could not cover sellers' side story
>
> Natural language processing is currently based on a self-made dictionary, which could have lead to biases. So a different approach aimed at objectivity or a comparison research is most welcomed. 

---

## SLIDE 19 — What did we learn? (≈ 35 sec)
*Purpose: three sentences. Land them.*

[Slow. Confident. Look at the council, not the slide.]

> Long story short, I have learned three major lessons.
>
> **One.** Attribute premiums exist — price tier, pack size, and category-specific imports and health claims are the dominant ones.
>
> **Two.** Promotion erodes brand-name premiums by half between sticker and checkout, but leaves price-tier premiums fully intact. *That asymmetry is the central empirical contribution.*
>
> **Three.** To the best of my knowledge, this is the first hedonic decomposition of Vietnamese online grocery using web-scraped daily dual-price data, and thus a proof-of-concept for future academic work.

---

## SLIDE 20 — Thank you (≈ 15 sec)
*Purpose: acknowledgements. Sincere, brief.*

[Stand still. Both hands at your sides or lightly clasped. Make eye contact with the chair.]

> Thank you, esteemed members of the Committee.
>
> My deepest thanks to my supervisor, Dr. Nguyễn Mạnh Thế, and my mentor Dr. Đinh Thị Hồng Thêu.
>
> *I welcome your questions.*

[Pause. Smile. Wait for the chair to invite the first question. Do not fill silence.]

---

# Speaker reminders

## Pace and pauses

- **Estimated time: ~12:00** at 140 wpm — comfortable, not rushed.
- The slowest beat is **Slide 11**. Let the three numbers land — 50.6%, WinEco sticker, WinEco checkout.
- **Deliberate silence (~1 sec)** after: the Vinamilk gap (S3), the research question (S4), each of the three numbers on S11, and each of the three sentences on S19.

## The spine — transitions you must not skip

| From → To | The bridge |
|---|---|
| S3 → S4 | *"That observation gave me the research question."* |
| S4 → S5 | *"Identify, measure, compare. The rest of the talk follows that order."* |
| S5 → S6 | *"With that scaffolding in place, let me show you the framework I use to think about brand."* |
| S6 → S7 | *"Without it, the central finding of this thesis would be invisible."* |
| S9 → S10 | *"The dual-price design exposes an asymmetry that would otherwise be invisible."* |
| S10 → S11 | *"Those are the pooled numbers. The dual-price design opens a second view."* |
| S11 → S12 | *"Now — what do these numbers mean?"* |
| S13 → S14 | *"Step back to the third objective — comparison across categories."* |
| S14 → S15 | *"Why does the same attribute carry opposite signs? Let me explain."* |
| S15 → S16 | *"The geography is the substantive finding — not noise."* |
| S16 → S17 | *"The estimates are stable."* |

## Optional — cuts to land at ~10:30 if you run long

Each saves roughly 8–12 seconds.

1. **Slide 5** — drop the Ekeland sentence. Lineage works with Lancaster + Rosen alone.
2. **Slide 7** — keep only Cavallo and Schipmann; drop Hülten and the consumer-research line.
3. **Slide 9** — cut the "log-linear not Box-Cox" defence; save it for Q&A.
4. **Slide 14** — cut the second pattern (health claims) and stay on the import contrast.
5. **Slide 16** — replace with: "All four standard diagnostics pass."
6. **Slide 18** — drop the brand-dictionary and Tết items; keep single-retailer + Jevons.

## Q&A — common questions and where to point

| Question | Slide / Appendix |
|---|---|
| Why hedonic, not discrete choice or ML? | Methodology appendix (A8 in the deck) |
| Why log-linear, not Box-Cox or quantile? | Slide 9 + speak from memory |
| Are the three brand dummies separately identified? | Appendix A1 (VIF table) |
| Robust to influential observations / time period? | Appendix A2 |
| Is the WinEco result reliable with n=21? | Appendix A3 + acknowledge suggestive |
| Why is R² low in Confectionery / Processed / Instant? | Appendix A4 |
| Why Jevons, not Laspeyres or Törnqvist? | Appendix A5 |
| Brand dictionary — could it misclassify? | Appendix A6 + attenuation argument |
| Is `is_premium` endogenous? | Slide 18 + speak from memory |
| Why no formal Tết event study? | Appendix A7 |
| Why a single retailer? | Slide 18 — design choice, multi-retailer is future work |
| What would change your mind? | Three things — multi-retailer null on brand erosion, transaction data showing demand insensitive to channel, WinEco non-replication |

When the council asks something you didn't anticipate: *"That is a question I have not addressed in this thesis — let me think aloud about it,"* and then think aloud. Do not invent.
