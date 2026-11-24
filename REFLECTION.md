# Reflection: Design Principles and Tradeoffs
Mini-Project 2 · NYC Film Permits · Live: https://gurleen-kaur1313.github.io/film-permits-dashboard/

**Cleveland & McGill ranking and Effectiveness.** The main question is how *often* each kind of production shoots and for
how *long*, so both quantities use the top-ranked channel, position on a common scale: permit count on the scatter's x-axis
and median duration on its y-axis. The secondary variable, streets held, gets the lower-ranked area channel. Borough totals use
length on a shared baseline, sorted by count, and time is horizontal position on the timeline.

**Expressiveness.** Each channel matches its data type. Category and borough are nominal, so they get distinct hues and
separate rows, with no implied order. Duration bins are ordinal, so they get a sequential pink-to-plum ramp whose lightness
falls in order. Its hues appear nowhere in the category palette, so duration cannot be mistaken for a category.

**Stevens' power law.** People underestimate area (exponent ≈ 0.7), so dot radius is √(streets) and *area* is proportional
to the value. Area is still imprecise, so streets held is only a secondary cue, backed by a size key and exact tooltip values.

**Gestalt.** Two dashed **enclosure** bands group the views by question ("What & Where", "When"). **Proximity** reinforces
this: views inside a band are 12 px apart, and the bands are 26 px apart. **Similarity:** a category has the same hue in the
legend, dots and lines, and the same ramp means duration everywhere. The hierarchy runs title → legend → large scatter (main
question, top-left) → bars → timeline.

**Data-ink ratio.** One shared legend replaces per-view legends. Lines and extreme dots are labelled directly, and the grid
is light. The y-axis is fitted to the data instead of spending 60 % of the plot on an empty 0–11 h.

**Interaction (overview → filter → details on demand).** Every view filters the others but ignores its own filter, so
unselected options stay visible. Hover gives details, and chips plus the URL show the current state.

**Tradeoffs**
- *y-axis not at 0:* dots encode position, not length, so a fitted 11–19 h axis is valid. The title states where it starts.
- *Log x-axis:* counts span 30–4,731, which a linear axis would crush. The cost is that readers must read the tick labels.
- *Binned duration:* four bins lose detail but make boroughs comparable. The edges come from the data's quantiles,
  because the prototype's fixed bins put 85 % of permits in one shade.
- *Medians, not means:* robust to multi-day outliers, but they mostly land on whole hours, so some dots share a row.
- *Top 4 + Other:* keeps the legend at 5 items (≤ 7). A dot takes its subcategory's most common category colour.
- *Colour:* the prototype's navy, purple and maroon were too close in lightness. The final blue, crimson, teal, golden orange
  and light green differ in hue *and* lightness (steps ≥ 12.8 L\*). They pass the greyscale test, and every pair stays
  ΔE ≥ 38 under simulated colour-blindness. Red and orange were pushed apart in hue and lightness after they looked alike in the timeline. A peer asked for bright colours instead of grey duration shades. Four unrelated
  hues would imply categories, so I used one bright *sequential* ramp instead. Light orange and green get darker edges on white.
- *RQ3:* the proposal mentioned the 2020 drop, but the data starts in 2023. The timeline instead shows Television collapsing
  in mid-2023 (1,091 permits in Q1 → 87 in Q3; Film 161 → 55), during the writers' and actors' strikes. Commercial held
  steady, and both TV and Film recovered in 2024.

## Channel Justification Table (updated)
| Data variable | Data type | View | Channel | Why |
|---|---|---|---|---|
| Median shoot duration | Quantitative | Scatter | Vertical position | Most accurate channel; main variable of RQ1 |
| Permit count | Quantitative (skewed) | Scatter, bars, timeline | Position (log) / length | Highest-ranked channels; log handles skew |
| Avg. streets held | Quantitative | Scatter | Area (√-scaled) | Secondary; √ corrects for Stevens' exponent |
| Category | Categorical (top 4 + Other) | Scatter, timeline | Hue + distinct lightness | Unordered hue suits nominal data; 5 items |
| Subcategory | Categorical | Scatter | One mark each + labels | Identity is labelled, not colour-coded |
| Borough | Categorical | Bars | Row position (sorted) | Aligned rows support comparison |
| Shoot duration bin | Ordinal | Bars | Sequential ramp (lightness) | Ordered channel for ordered data |
| Start month | Temporal | Timeline | Horizontal position | Accurate; supports brushing |
