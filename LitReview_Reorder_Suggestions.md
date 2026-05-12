# Literature Review — Reorder Suggestions

Reviewing Chapter 1 (Literature Review and Theoretical Framework) of `Thesis_Draft_Comprehensive_Formatted.docx`. The guiding principle from your request: **where you currently present sources in an order that ignores chronology, check whether a later study actually resolves or supersedes an earlier one, and re-sequence so the reader sees the development of the problem → its resolution.**

Below is a section-by-section audit. For each problematic passage I list (a) the current order of citations, (b) why the order is confusing, and (c) a proposed reorder with a one-line rationale.

---

## Section 1.1 — Hedonic Pricing Theory: Goods as Attribute Bundles

**Current order of citations in the body text:**
Lancaster (1966) → Rosen (1974) → Ekeland, Heckman & Nesheim (2004) → Lucas (1975)

**Problem.** Lucas (1975) appears *after* Ekeland et al. (2004), framed as "reinforcing this point." Historically it is the reverse: Lucas (1975) gave the earliest clean statement of the single-market identification problem, and Ekeland, Heckman & Nesheim (2004) formalised and generalised that insight nearly three decades later. As written, the paragraph makes Lucas look like a footnote to Ekeland, when in fact Ekeland resolves/formalises what Lucas first flagged.

**Suggested order:**

1. Lancaster (1966) — goods are bundles of attributes (foundation).
2. Rosen (1974) — equilibrium hedonic price function; two-stage framework.
3. **Lucas (1975)** — early recognition that in a single market, the hedonic schedule jointly reflects demand and supply (problem identified).
4. **Ekeland, Heckman & Nesheim (2004)** — formal identification results confirming and extending Lucas; motivates the reduced-form interpretation this thesis adopts (later study resolves earlier concern).

**Concrete edit suggestion.** Move the Lucas (1975) paragraph (currently lines 630–642 of the extracted text, beginning "Lucas (1975) reinforced this point…") to *before* the Ekeland paragraph, and rephrase the transition so Ekeland et al. (2004) are introduced as having formalised Lucas's point.

---

## Section 1.2 — Hedonic Methods in Food and Agricultural Markets

### 1.2 opening paragraph

**Current order:** Costanigro & McCluskey (2011) appears at the very top of the section as a framing review.

**Assessment.** This is defensible (reviews often open a section), but the placement creates a cascade problem inside §1.2.2 because Costanigro & McCluskey (2011) already surveys Nerlove, Schamel, Malpezzi, etc., and the subsection then re-introduces those same authors individually. Consider adding a forward-reference sentence ("…the specific studies Costanigro and McCluskey survey are discussed in §1.2.2 below") so the reader understands the nesting.

### §1.2.1 — Search, Experience, and Credence Attributes

**Current order:** Nelson (1970) → Darby & Karni (1973). ✓ Chronological and logical.

**No change needed.** This is already presented in the right sequence (Nelson introduces the dichotomy; Darby & Karni extend it with a third category).

### §1.2.2 — Methodological Precedents in Food Hedonics

**Current order of citations:**
Nerlove (1995) → Schamel (2006) → Malpezzi (2002) → Ballco & Gracia (2020) → Xuan (2021) → Lusk (2002)

**Problems.**

1. **Malpezzi (2002) is placed *after* Schamel (2006).** Malpezzi is the methodological source justifying the log-linear functional form; this belongs *before* the applied studies that already use it, or at the top of the subsection.
2. **Lusk (2002) appears *after* Xuan (2021).** The current paragraph uses Lusk to undermine Xuan's stated-preference WTP estimate. But Lusk's caution was published two decades before Xuan's study, so Xuan's study is an *example of a study subject to Lusk's critique*, not a target that Lusk answered retrospectively. Presenting Lusk last makes the chronology read backwards.

**Suggested order:**

1. **Malpezzi (2002)** — functional form guidance; justifies log-linear (move up; this is the methodological anchor).
2. **Nerlove (1995)** — wine hedonic (brand + origin separability, earliest applied precedent).
3. **Schamel (2006)** — extends Nerlove; confirms origin premium independent of brand across regions.
4. **Lusk (2002)** — methodological caution: stated-preference WTP suffers hypothetical bias (problem stated upfront).
5. **Ballco & Gracia (2020)** — hedonic vs. experimental WTP estimates diverge (extends Lusk's concern to food, using market data).
6. **Xuan (2021)** — Vietnamese stated-preference WTP study. Frame this as "illustrative of the stated-preference approach that Lusk (2002) and Ballco & Gracia (2020) caution against," then note the present thesis avoids the bias by using revealed-preference prices.

**Net effect.** The subsection would then read as: methodological rule (Malpezzi) → two canonical wine studies (Nerlove, Schamel) → the stated-preference problem (Lusk) → its empirical confirmation in food markets (Ballco & Gracia) → a Vietnamese instance of a study affected by the problem (Xuan) → how this thesis avoids it.

---

## Section 1.3 — Brand Equity, Product Differentiation, and Price Premiums

### Keller vs. Aaker ordering

**Current order:** §1.3.1 Keller (1993) → §1.3.2 Aaker (1991) → §1.3.3 Four-Quadrant Typology.

**Problem.** Aaker (1991) was published *before* Keller (1993). In the brand equity literature, Aaker's 1991 book is the foundational text; Keller's (1993) CBBE paper is generally understood as building on Aaker's perceived-quality work and extending it with the awareness/image architecture. Presenting Keller first, then introducing Aaker as "complementing Keller," inverts the historical and conceptual order.

**Suggested order:**

1. **§1.3.1 — Perceived Quality as Brand Equity: Aaker (1991)** (foundational; price-tier positioning dimension).
2. **§1.3.2 — Customer-Based Brand Equity: Keller (1993)** (builds on Aaker; adds the awareness/recognition dimension via the CBBE model).
3. **§1.3.3 — The Four-Quadrant Brand Positioning Typology** (crosses Aaker's perceived quality × Keller's awareness; add a short explicit mention of Kapferer (2008) here as the *most recent* justification for multidimensional brand identity).

**Concrete edit suggestion.** Swap the two subsections (Aaker first, Keller second) and adjust the connective sentences in the second subsection so Keller is introduced as extending Aaker, not being complemented by him. In §1.3.3, surface Kapferer (2008) slightly more prominently so the "later study resolves earlier" logic (Kapferer's multidimensionality argument rules out collapsing Keller + Aaker into a single dummy) is explicit.

### §1.3 — Other Attribute Premiums: Origin, Quality Signals, and Versioning

**Current order:**
Schamel (2006) → Mergenthaler et al. (2009) → Darby & Karni (1973) → Varian (1997) → MacDonald (2000)

**Problems.**

1. **Darby & Karni (1973)** is re-introduced in the middle of the paragraph, between 2009 and 1997 studies. Since they were already covered in §1.2.1, this re-insertion is disruptive and non-chronological. Either replace with a cross-reference to §1.2.1, or move the Darby & Karni sentence to the head of the "credence attributes" mini-paragraph.
2. **Varian (1997) → MacDonald (2000)** is chronological and logical. ✓
3. **Schamel (2006) → Mergenthaler et al. (2009)** for origin premiums is chronological and logical. ✓

**Suggested order:**

1. *Origin.* Schamel (2006) → Mergenthaler et al. (2009). ✓ Keep as is.
2. *Credence attributes.* Open with a cross-reference: "As established in §1.2.1, Darby & Karni (1973) classify these as credence attributes…" — no re-citation needed.
3. *Versioning and promotional pricing.* Varian (1997) → MacDonald (2000). ✓ Keep as is.

---

## Section 1.4 — Online Retail Pricing and Web-Scraped Price Data

**Current order of citations:**
Cavallo (2017) → Hülten (2002) → Tran et al. (2025) → Singh et al. (2020) → Schipmann & Qaim (2011)

**Problems.**

1. **Tran et al. (2025) appears before Singh et al. (2020).** The paragraph uses the phrase "Singh et al. (2020) further find…" as if Singh extends Tran, but Singh was published five years earlier. Reverse chronological with a "further find" connector is misleading.
2. **Schipmann & Qaim (2011) is pushed to the very end** as a "finally" coda, even though it is one of the oldest and most load-bearing sources (it justifies the single-retailer design that runs through the whole thesis). Its placement at the end reads as an afterthought.
3. **Hülten (2002) is buried between Cavallo (2017) and the Vietnamese-context sources**; consider whether it fits more naturally as part of the opening methodological justification chain.

**Suggested order (topical grouping with chronological order inside each topic):**

1. **Cavallo (2017)** — headline evidence: 72% of prices identical online vs. offline. (Keep as the lead result.)
2. **Schipmann & Qaim (2011)** — retail format creates systematic price variation in Southeast Asian food markets (justifies single-retailer design). *Move up from last position.*
3. **Hülten (2002)** — daily price data avoids temporal aggregation bias (methodological justification for the 88-day panel). *Keep in methodological cluster.*
4. **Singh et al. (2020)** — Vietnamese-context evidence: price transparency drives digital grocery adoption (earlier).
5. **Tran et al. (2025)** — extends Singh; Vietnamese online grocery shoppers are price-aware and actively comparison-shop (most recent; "further finds" connector now works forward in time).

---

## Section 1.5 — Vietnamese Food Market Context and Research Gap

**Current order of citations in the consumer-behavior paragraph:**
Bairagi et al. (2020) → Mergenthaler et al. (2009) → Bell et al. (2021) → Trinh et al. (2020)

**Problem.** Trinh et al. (2020) appears *after* Bell et al. (2021), even though it was published earlier. Bell et al. (2021) is the most recent and extends the category-heterogeneity argument; it reads more naturally as the capstone.

**Suggested order:**

1. **Bairagi et al. (2020)** — structural transformation from wet markets to modern trade. ✓ Keep as the opening scene-setter.
2. **Mergenthaler, Weinberger & Qaim (2009)** — earliest Vietnamese WTP evidence (up to 60% for food safety). ✓ Keep second.
3. **Trinh et al. (2020)** — quality perception dominates price sensitivity in Vietnamese supermarket purchasing. *Move up from last position.*
4. **Bell et al. (2021)** — category-level heterogeneity of food values; most recent and most directly motivates the per-category regression in Ch. 4. *Move to the end.*

This reordering turns the paragraph into a cleaner narrative: market transition (2020) → foundational WTP evidence for food safety (2009) → quality-over-price in supermarket choice (2020) → category-level heterogeneity refining both prior findings (2021).

---

## Summary Table of Recommended Moves

| Section | Move this citation | From (current position) | To (proposed position) | Reason |
|---|---|---|---|---|
| 1.1 | Lucas (1975) | After Ekeland et al. (2004) | Before Ekeland et al. (2004) | Lucas identified the identification problem first; Ekeland formalised it |
| 1.2.2 | Malpezzi (2002) | After Schamel (2006) | Before or at opening of §1.2.2 | Methodological rule precedes applied studies that use it |
| 1.2.2 | Lusk (2002) | After Xuan (2021) | Before Ballco & Gracia (2020) | Lusk's critique is foundational, not a response to Xuan |
| 1.3 | §1.3.1 Aaker ↔ §1.3.2 Keller | Keller first, Aaker second | Aaker first, Keller second | Aaker (1991) predates Keller (1993); Keller builds on Aaker |
| 1.4 | Schipmann & Qaim (2011) | Last (after Singh 2020) | Second (after Cavallo 2017) | Load-bearing source for single-retailer design; deserves earlier placement |
| 1.4 | Singh (2020) ↔ Tran (2025) | Tran first, Singh second | Singh first, Tran second | Restores chronological order; fixes misleading "further finds" wording |
| 1.5 | Trinh (2020) ↔ Bell (2021) | Bell first, Trinh second | Trinh first, Bell second | Restores chronological order; makes the category-heterogeneity capstone land properly |

---

## Note on the four-quadrant typology (§1.3.3)

The current subsection correctly cites Kapferer (2008) as the most recent source arguing brand identity is multidimensional, but this justification is one sentence buried near the end. Consider opening §1.3.3 with Kapferer's point — that a single "branded" dummy collapses too many dimensions — as the *motivation* for crossing Aaker's perceived quality with Keller's awareness. This would make the "later literature resolves a limitation of earlier literature" logic explicit and would strengthen the theoretical pedigree of the typology.

---

## What I did *not* recommend moving

- The opening paragraph of Chapter 1 (section overview) — the sequence of forward references mirrors the section numbering and should not be resequenced independently.
- §1.2 opening — Costanigro & McCluskey (2011) as the framing review is a defensible rhetorical choice. A one-sentence forward reference to §1.2.2 is enough.
- §1.2.1 (Nelson → Darby & Karni) — already chronological and logical.
- The research gap numbering (Gaps 1–3 in §1.5) — structural, not chronological.

---

## Next step

If you want me to apply any or all of these reorders to `Thesis_Draft_Comprehensive_Reordered.docx`, tell me which items from the summary table to execute. I can make the changes as **tracked-change edits** (moves appear as deletions + insertions, authored by "Claude") so you can accept or reject each one individually in Word.
