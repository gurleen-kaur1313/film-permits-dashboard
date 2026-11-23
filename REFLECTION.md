# Reflection: Design Principles and Tradeoffs
Mini-Project 2 · NYC Film Permits · Live: https://gurleen-kaur1313.github.io/film-permits-dashboard/

**Cleveland & McGill ranking and the Effectiveness principle.** The question I cared most about is how *often* each kind of
production shoots and for how *long*. Both quantities therefore sit on the top-ranked channel, position on a common scale:
permit count on the scatter's x-axis and median shoot duration on its y-axis. The secondary quantity, streets held, gets
area, which ranks lower. Borough totals use length on a shared baseline, the next-best channel, and the bars are sorted by
count so the comparison is easy to read. Time is horizontal position on the timeline, because it is the variable people scan along.

**Expressiveness.** Each channel matches its data type. Category and borough are nominal, so they get hue and separate
rows, with no implied order. Duration bins are ordinal, so they get an ordered lightness ramp with no hue. Permit
counts, durations and streets are quantitative, so they get position, length and area. Grey is reserved for the ordinal
variable so it can never be mistaken for a category.

**Stevens' power law.** People underestimate area (exponent ≈ 0.7), so dot radius is proportional to √(streets) and dot
*area* is proportional to the value. Even so, area is imprecise, which is why streets held is only a secondary cue:
it has a two-circle size key and exact values in the tooltip.

**Gestalt principles.** Two dashed **enclosure** bands group the views by question ("What & Where", "When"). **Proximity**
reinforces this: views inside a band are 12 px apart, and the bands are 26 px apart. **Similarity:** a category has the
same hue in the legend, dots, lines and line labels, and the same grey ramp means duration everywhere. Visual hierarchy
runs from the title to the shared legend, then the large scatter (top-left, the main question), then the bars, then the timeline.

**Data-ink ratio.** There is one shared legend instead of one per view. Lines are labelled at their ends and the extreme
dots are labelled in place, so the eye does not travel to a key. The grid is light, the axis is fitted to the data rather
than spending 60 % of the plot on empty 0–11 h, and non-data decoration is limited to the enclosure bands that carry grouping.

**Interaction (overview → filter → details on demand).** Every view filters the others. Each view ignores its own filter,
so unselected options stay visible and can be switched to. Hover shows details, chips show the current state, and the URL stores it.

**Tradeoffs I made**
- *y-axis not starting at 0.* For dots, position rather than length carries the value, so a fitted 11–19 h axis
  is legitimate and shows real differences. I state the start value in the axis title to prevent misreading.
- *Log x-axis.* Permit counts span 30 to 4,731. A linear axis would crush most dots into one corner. The cost is that
  readers must read the tick labels, not distances, which I will check in usability testing.
- *Binning duration.* Four bins lose detail but make the borough comparison possible. I chose the bin edges from the real
  quantiles because the original fixed bins put 85 % of permits in one shade.
- *Medians, not means.* Durations are skewed by multi-day shoots. Medians are robust but mostly land on whole hours, so
  some dots share a row.
- *Top-4 categories + Other, and one colour per subcategory.* This keeps the legend at 5 items (≤ 7). A dot's hue is its
  subcategory's *most common* category, which the footer states. "Not Applicable" subcategories are counted in the bars
  and timeline but get no dot.
- *Research question 3* originally mentioned the 2020 drop, but the downloaded data starts in Jan 2023. The timeline
  instead shows a mid-2023 collapse in Television (1,091 permits in Q1 → 87 in Q3) and, to a lesser degree, Film
  (161 → 55), coinciding with the 2023 writers' and actors' strikes. Commercial shoots held steady, and both TV and Film
  recovered in 2024. This is the "did every category recover the same way?" answer.
- *Palette.* The prototype's dark navy, purple and maroon were too close in lightness. The final palette spaces lightness
  ≥ 14.6 L\* apart and keeps the worst colour-blind pair at ΔE ≥ 34.9, at the cost of a pale "Other" that needs a dark edge.

## Channel Justification Table (updated)
| Data variable | Data type | View | Channel | Why (expressiveness / effectiveness) |
|---|---|---|---|---|
| Median shoot duration | Quantitative | Scatter | Vertical position | Most accurate channel; main variable of RQ1 |
| Permit count | Quantitative (skewed) | Scatter, bars, timeline | Position (log) / length / position | Position and length rank highest; log handles the skew |
| Avg. streets held | Quantitative | Scatter | Area (√-scaled) | Secondary variable; √ corrects for Stevens' exponent |
| Category | Categorical (top 4 + Other) | Scatter, timeline, legend | Hue (lightness-separated) | Hue is unordered, suiting nominal data; 5 items ≤ 7 |
| Subcategory | Categorical | Scatter | One mark each + direct labels | Identity, so names are labelled rather than colour-coded |
| Borough | Categorical | Bars | Row position (sorted by count) | Separate aligned rows support comparison |
| Shoot duration bin | Ordinal | Bars | Lightness (grey ramp) | Ordered channel for ordered data, distinct from category hue |
| Start month | Temporal | Timeline | Horizontal position | Conventional, accurate, supports brushing |
