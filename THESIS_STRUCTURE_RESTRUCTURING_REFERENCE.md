# THESIS STRUCTURE RESTRUCTURING REFERENCE GUIDE
**Date:** 2026-04-09  
**Task:** Identify all chapter/section references requiring updates for restructuring

---

## EXECUTIVE SUMMARY

**Total Files Scanned:** 9  
**Files Requiring Changes:** 2 primary, 1 secondary  
**Primary Change Locations:** 
1. `generate_ch1_v2.py` — Lines 465-484 (Section 1.6 Thesis Structure)
2. `Thesis_Chapter1.docx` — Similar thesis structure description paragraph
3. `thesis_summary_for_professor.md` — Lines 11-52 (Chapter Outline)

**Good News:** Most cross-chapter references (Ch3→methodology, Ch4→results, Ch5→conclusions) remain valid in the new structure.

---

## DETAILED FILE-BY-FILE ANALYSIS

### FILE 1: `/sessions/adoring-elegant-mccarthy/generate_ch1_v2.py`

#### PRIMARY LOCATION REQUIRING CHANGE
**Location:** Lines 465-484 in Section 1.6 "Thesis Structure"

**Current Text (OLD STRUCTURE):**
```python
add_rich_para([
    'The remainder of this thesis is organized as follows. ',
    ('Chapter 2', True),
    ' reviews the theoretical foundations of hedonic pricing, brand equity, and '
    'online retail pricing, and identifies the specific research gaps this study '
    'addresses. ',
    ('Chapter 3', True),
    ' presents the methodology—the hedonic price model, functional form and '
    'estimation strategy, dual-price design, feature extraction pipeline, and '
    'brand positioning typology—with each methodological choice justified '
    'against alternative approaches. ',
    ('Chapter 4', True),
    ' applies the methodology to the data: it describes the data source and '
    'collection process, defines variables, reports descriptive statistics, and '
    'presents the pooled and per-category hedonic regression results, the '
    'promotional erosion analysis, and diagnostic checks. ',
    ('Chapter 5', True),
    ' discusses the implications of the empirical findings in the context of '
    'Vietnamese grocery markets, addresses the Tët holiday period, '
    'acknowledges limitations, draws conclusions, and offers recommendations '
    'for consumers, retailers, and future research.'
], style_name='NoIndent')
```

**Needs Rewriting To Match NEW Structure:**
```
Ch2: Literature Review (no change)
Ch3: Methodology (pure methods + comparison to alternatives) — REWRITE
Ch4: Empirical Application (data + variables + results + diagnostics) — REWRITE  
Ch5: Conclusions and Recommendations (discussion + Tet + limitations + conclusions + recommendations) — REWRITE
```

**Action Required:** Complete replacement of the Chapter 3-5 descriptions

---

#### SECONDARY LOCATION: Validation Cross-Reference
**Location:** Line 349

**Current Text:**
```python
'The NLP pipeline has been validated against manual coding '
'on a subset of products (see Chapters 3 and 4).'
```

**Status:** Still valid in new structure if validation content appears in both:
- Ch3 (Methodology) — methodological validity/validation
- Ch4 (Empirical Application) — empirical application validation

**Action Required:** CHECK whether validation is discussed in both chapters; no text change needed if it is.

---

#### TERTIARY LOCATION: Chapter 5 Reference (No Change Needed)
**Location:** Line 401

**Current Text:**
```python
'The external validity implications of this design choice are discussed in '
'Chapter 5.'
```

**Status:** VALID in both old and new structures — Ch5 contains discussion/limitations/conclusions in both

**Action Required:** None ✓

---

### FILE 2: `/sessions/adoring-elegant-mccarthy/generate_ch2.py`

#### Overview
Most references in this file are INTERNAL to Chapter 2 (§2.1-§2.5) and require no changes.

#### Cross-Chapter References (All Valid)

| Line | Reference | Context | Status |
|------|-----------|---------|--------|
| 241  | "Chapters 4 and 5" | Empirical claims made in results and discussion | VALID ✓ |
| 497  | "Chapter 3" | Brand typology operationalization | VALID ✓ |
| 549  | "Chapter 3" | Single-retailer design justification | VALID ✓ |
| 678  | "Chapter 4" | Results presentation | VALID ✓ |
| 745  | "Chapter 5" | Trade-off discussion | VALID ✓ |
| 749  | "Chapter 4" | Results reference | VALID ✓ |
| 784  | "Chapter 4" | Results reference | VALID ✓ |
| 838  | "The following chapter" | Forward reference to Ch3 | VALID ✓ |

**Action Required:** None — all still reference correct chapters ✓

---

### FILE 3: `/sessions/adoring-elegant-mccarthy/mnt/Online Food Price/Thesis_Chapter1.docx`

#### PRIMARY LOCATION: Section 1.6 "Thesis Structure"

**Location:** Final paragraph of Chapter 1 (docx paragraph ~39)

**Current Description Matches generate_ch1_v2.py** — Same content as above

**Action Required:** Complete rewrite to match new structure (mirror the changes made to generate_ch1_v2.py)

**New Text Should Describe:**
```
Ch2: Literature Review — theoretical foundations, research gaps
Ch3: Methodology — hedonic model, functional form, dual-price design, 
                   feature extraction, brand typology, with justification 
                   vs. alternative approaches
Ch4: Empirical Application — data collection, variables, descriptive 
                             statistics, regression results (marked & final),
                             erosion analysis, diagnostics
Ch5: Conclusions and Recommendations — discussion of findings, Tet context,
                                       limitations, conclusions, recommendations
```

---

### FILE 4: `/sessions/adoring-elegant-mccarthy/mnt/Online Food Price/Thesis_Chapter2.docx`

#### Status: NO CHANGES REQUIRED ✓

All cross-chapter references in Chapter 2 point to chapters that still contain the same content:
- "Chapter 3" → still Methodology (valid)
- "Chapter 4" → still results & empirical content (valid)
- "Chapter 5" → still discussion & conclusions (valid)

**Action Required:** None ✓

---

### FILE 5: `/sessions/adoring-elegant-mccarthy/mnt/Online Food Price/Thesis_Draft_Comprehensive.docx`

#### Status: MOSTLY VALID — Already reflects new structure

**Header Line 2:** "COMPREHENSIVE CHAPTER OUTLINE — Chapters 1–4"
- Note: Update to "Chapters 1–5" to reflect complete outline

**Chapter Headers:** Already present:
- CHAPTER 1: INTRODUCTION ✓
- CHAPTER 2: LITERATURE REVIEW ✓
- CHAPTER 3: METHODOLOGY ✓ (NEW)
- CHAPTER 4: EMPIRICAL APPLICATION ✓ (NEW)

**Section References:** All §3.x and §4.x references are internal and valid ✓

**Action Required:** 
- Update header from "Chapters 1–4" to "Chapters 1–5"
- Add missing §5.x sections if not present
- All substantive content appears compatible ✓

---

### FILE 6: `/sessions/adoring-elegant-mccarthy/mnt/Online Food Price/Thesis_Draft_Ch3_4_Bullets.docx`

#### Status: VALID — Already uses new structure ✓

**Structure Presented:**
```
CHAPTER 1: INTRODUCTION
CHAPTER 2: LITERATURE REVIEW
CHAPTER 3: METHODOLOGY
CHAPTER 4: EMPIRICAL APPLICATION
```

**Section References:** §2.1-2.5, §3.1-3.5, §4.1-4.7 all valid ✓

**Action Required:** None ✓

---

### FILE 7: `/sessions/adoring-elegant-mccarthy/mnt/Online Food Price/thesis_outline_ch1_4.docx`

#### Status: VALID — Reflects new structure ✓

**Chapter Headers:**
```
CHAPTER 1: INTRODUCTION
CHAPTER 2: LITERATURE REVIEW
CHAPTER 3: METHODOLOGY
CHAPTER 4: EMPIRICAL APPLICATION
```

**Critical Organizational Statements:**

| Line | Statement | Interpretation |
|------|-----------|-----------------|
| 90   | "→ Data source and collection described. §4.2 addresses known gaps" | Data now in §4.2 (Empirical Application) ✓ |
| 98   | "→ Limitations documented. §4.3 describes how product attributes are extracted" | Feature extraction now in Ch4 ✓ |
| 109  | "→ Features extracted. §3.4 organizes the brand features into a typology" | Brand typology in Ch3 methodology ✓ |
| 116  | "→ Typology defined. §3.2 specifies the hedonic regression model" | Regression in Ch3 methodology ✓ |
| 130  | "→ Methodology complete. Chapter 4 applies this framework" | Clean separation: Ch3 methods, Ch4 applies ✓ |
| 184  | "→ Diagnostics complete. §5.1 interprets the findings" | Discussion in Ch5 ✓ |

**Action Required:** None ✓

---

### FILE 8: `/sessions/adoring-elegant-mccarthy/mnt/Online Food Price/.claude/thesis_brainstorm.md`

#### Status: CANONICAL REFERENCE — Already correct ✓

**Structure (Lines 11-111):**
```
Chapter 1  Introduction (§1.1-1.6)
Chapter 2  Literature Review (§2.1-2.5)
Chapter 3  Methodology (§3.1-3.5)
Chapter 4  Empirical Application (§4.1-4.7)
Chapter 5  Conclusions and Recommendations (§5.1-5.5)
Appendix A-D
```

**All Cross-References Valid:**
- §3.1-3.5: Methodology sections
- §4.1-4.7: Empirical application sections
- §5.1-5.5: Conclusions and recommendations sections

**Action Required:** None — use this as the reference template ✓

---

### FILE 9: `/sessions/adoring-elegant-mccarthy/mnt/Online Food Price/thesis_summary_for_professor.md`

#### Status: REQUIRES RESTRUCTURING ✗

**Current Structure (OLD):**
```
**Chapter 1 — Introduction**
**Chapter 2 — Literature Review**
**Chapter 3 — Data & Methods**        ← Needs consolidation
**Chapter 4 — Results**                ← Needs consolidation
**Chapter 5 — Discussion**             ← Needs consolidation
**Chapter 6 — Conclusion**             ← DELETE, merge into Ch5
```

**Specific Lines Requiring Changes:**

| Line | Current Text | Change To | Action |
|------|--------------|-----------|--------|
| 13   | **Chapter 1 — Introduction** | Keep as is | No change ✓ |
| 18   | **Chapter 2 — Literature Review** | Keep as is | No change ✓ |
| 24   | **Chapter 3 — Data & Methods** | **Chapter 3 — Methodology** | Rewrite subsections |
| 32   | **Chapter 4 — Results** | **Chapter 4 — Empirical Application** | Restructure content |
| 39   | **Chapter 5 — Discussion** | **Chapter 5 — Conclusions and Recommendations** | Rename & reorganize |
| 45   | **Chapter 6 — Conclusion** | DELETE | Remove entire section |

**Additional Content Updates Required:**

- **Lines 25-30** (Ch3 subsections): Update from "Data collection, limitations, feature extraction" to pure methodology (model, alternatives, functional form, dual-price design)
- **Lines 33-37** (Ch4 subsections): Restructure to include "4.1 Data source and collection" alongside "4.2-4.7 results/diagnostics"
- **Lines 40-43** (Ch5 subsections): Rename from "Discussion" sections to "5.1 Discussion, 5.2 Tet context, 5.3 Limitations, 5.4 Conclusions, 5.5 Recommendations"

**Action Required:** Complete restructuring of this file to consolidate 6 chapters into 5

---

## REFERENCE TABLE: CHANGE REQUIREMENTS BY SEVERITY

### HIGH PRIORITY (Must Change)
| File | Location | Change Type | Complexity |
|------|----------|-------------|-----------|
| generate_ch1_v2.py | Lines 465-484 | Full rewrite | High — maintain voice/formatting |
| Thesis_Chapter1.docx | §1.6 paragraph | Full rewrite | High — mirror Python changes |
| thesis_summary_for_professor.md | Lines 11-52 | Restructure | High — content reorganization |

### MEDIUM PRIORITY (Verify Content)
| File | Location | Action | Complexity |
|------|----------|--------|-----------|
| generate_ch1_v2.py | Line 349 | Check validation location | Low — text likely OK |
| Thesis_Draft_Comprehensive.docx | Line 2 header | Update "1–4" to "1–5" | Low — single word |

### LOW PRIORITY (No Changes Needed)
| File | Status | Reason |
|------|--------|--------|
| generate_ch2.py | ✓ Valid | All cross-refs still point to correct chapters |
| Thesis_Chapter2.docx | ✓ Valid | Internal §2.x + valid cross-refs |
| Thesis_Draft_Ch3_4_Bullets.docx | ✓ Valid | Already uses new structure |
| thesis_outline_ch1_4.docx | ✓ Valid | Already reflects new structure |
| thesis_brainstorm.md | ✓ Valid | Canonical reference — already correct |

---

## SECTION NUMBERING REFERENCE

### Chapter 3: Methodology (§3.1-3.5)
Based on thesis_brainstorm.md and thesis_outline_ch1_4.docx:
```
§3.1  Hedonic price model
§3.2  Functional form and estimation strategy
§3.3  Dual-price design
§3.4  Feature extraction and brand positioning typology
§3.5  Price index methodology
```

### Chapter 4: Empirical Application (§4.1-4.7)
Based on thesis_outline_ch1_4.docx:
```
§4.1  Data source, collection, and single-retailer design
§4.2  Data limitations and coverage
§4.3  Variable definitions and descriptive statistics
§4.4  Pooled hedonic regression results
§4.5  Per-category heterogeneity
§4.6  Promotional erosion analysis
§4.7  Diagnostics and robustness
```

### Chapter 5: Conclusions and Recommendations (§5.1-5.5)
Based on thesis_brainstorm.md:
```
§5.1  Discussion
§5.2  Tet context
§5.3  Limitations
§5.4  Conclusions
§5.5  Recommendations
```

---

## CROSS-REFERENCE VALIDITY MATRIX

### Does "Chapter 3" still work in new structure?
| Old Content | New Location | Status |
|------------|--------------|--------|
| Methodology | Still Ch3 | VALID ✓ |
| Data collection | Now Ch4 | Check references! |

### Does "Chapter 4" still work?
| Old Content | New Location | Status |
|------------|--------------|--------|
| Results | Still Ch4 | VALID ✓ |
| Data & Methods | Ch3 + Ch4 | VALID ✓ |

### Does "Chapter 5" still work?
| Old Content | New Location | Status |
|------------|--------------|--------|
| Discussion | Still Ch5 | VALID ✓ |
| Limitations | Still Ch5 | VALID ✓ |
| Conclusions | Still Ch5 | VALID ✓ |
| Recommendations | Still Ch5 | VALID ✓ |

---

## IMPLEMENTATION CHECKLIST

- [ ] Rewrite `generate_ch1_v2.py` lines 465-484
- [ ] Verify `generate_ch1_v2.py` line 349 validation reference (check content placement)
- [ ] Update `Thesis_Chapter1.docx` §1.6 to match rewritten Python script
- [ ] Restructure `thesis_summary_for_professor.md` lines 11-52
  - [ ] Update Chapter 3 heading and subsections
  - [ ] Update Chapter 4 heading and subsections
  - [ ] Update Chapter 5 heading and subsections
  - [ ] Delete Chapter 6 section
- [ ] Update `Thesis_Draft_Comprehensive.docx` header line 2
- [ ] Cross-check all other files for any missed references

---

## NOTES

1. **thesis_brainstorm.md is the canonical reference** — it already reflects the complete new structure correctly. Use it as the template.

2. **Most cross-chapter references are stable** because:
   - Ch2 (Literature) hasn't changed
   - Ch3 is still methodology (was "Data & Methods", now pure "Methodology")
   - Ch4 is still results/empirical (was "Results/Discussion", now "Empirical Application")
   - Ch5 is still discussion/conclusions (unchanged)

3. **The main narrative change is in Section 1.6 of Chapter 1**, which explicitly describes what each chapter contains. This is the "roadmap" that readers use, so it must be rewritten clearly.

4. **Data references in Chapter 2** (e.g., "see Chapter 3 for operationalization") are still valid because methodology (including data treatment) is still in Chapter 3.

5. **No section numbers (§3.1, §3.2, etc.) need to change** — they align correctly with the new structure as shown in thesis_brainstorm.md and thesis_outline_ch1_4.docx.
