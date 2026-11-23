# Prototype Feedback Log and Response
Mini-Project 2 · NYC Film Permits dashboard

**Strengths noted by the reviewer (kept):** deliberate encodings (position for counts and duration, square-root area for
streets held, hue for category, ordered grey ramp for duration), colour-blind-safe palette checked in greyscale, log x-axis
for skewed counts, linked filtering across all three views, filter chips, and the documented cleaning note.

| # | What the reviewer said | What I planned | What I actually changed (final) |
|---|---|---|---|
| 1 | Scatter y-axis runs 0–20 h but the dots sit at 12–18 h, so the plot is mostly empty. "Episodic series" / "Feature" labels overlap. | Fit the y-domain to the data and say it does not start at 0. Nudge labels apart with leader lines. | The y-domain is fitted to the medians with padding (11–19 h) and only widens if a filter pushes a dot outside. The axis title reads "axis starts at 11 h". Labels are placed by a collision-checking routine that tries positions around each dot, avoids other labels, captions and guide text, and draws a leader line when a label has to move away. |
| 2 | Navy, purple and maroon are hard to tell apart at small dot sizes. | Colours that differ in lightness as well as hue; white dot outline; larger minimum dot size. | New palette: navy #08306B / brick #A82F1C / teal #1E9A80 / amber #E8A21E / pale blue #C9E6F7. Lightness L\* 21 / 39 / 57 / 72 / 90 (every step ≥ 14.6). Worst-case pair under simulated protan/deutan/tritan vision went from ΔE 14.1 to 34.9. Dots have a white outline (dark for the pale "Other"), and the minimum radius is 5 px. |
| 3 | In the borough bars the 12–24 h bin is 80–90 %, so the minor grey shades are barely visible. | Counts / Share (100 %) toggle, keep absolute totals as labels, widen the grey steps. | Fixed the root cause: the bins are now <12 / 12–14 / 14–16 / ≥16 h (about 11 / 22 / 36 / 31 % of permits, from the real duration quantiles), so every shade is visible even in Counts view. Added the **Counts / Share %** toggle with % labels inside segments; totals stay as labels in both modes. Wider grey ramp, plus a data-driven takeaway under the bars. |
| 4 | The claim that Television is both "frequent and short" and "rare and long" needs a clearer cue, e.g. labels on the extremes. | Label the extremes, add median guide lines with quadrant captions, add a one-line takeaway, check the claim against the data. | The extremes (most permits, shortest, longest, most streets) are labelled directly with what makes them extreme. Dashed median lines and four quadrant captions (rare/frequent × short/long) were added. **Checking the data changed the claim:** Episodic series is the most frequent subcategory but not short (15 h). The accurate statement is that Television spans the whole range: busiest (Episodic series, 4,731), joint shortest (News, 12 h) and longest (Special/Awards Show, 18 h, 57 permits). The takeaway is computed from the data, so it stays correct under any filter. |
| 5 | The second submission was only a cover page; link the live dashboard and repository. | Link both in the hand-in. | The live dashboard (GitHub Pages) and repo are linked at the top of the README, in the dashboard footer, and in the report and reflection. |

**Biggest fix before the final:** the scatter and bars are now readable at a glance. The scatter's y-axis is fitted to the data
with the extremes labelled, and the duration bins are rebalanced with a Share % view, so the minor bins show.

Before/after evidence: [`screenshots/before_after_scatter.png`](screenshots/before_after_scatter.png),
[`screenshots/before_after_bars.png`](screenshots/before_after_bars.png).
