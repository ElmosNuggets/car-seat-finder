import streamlit as st
from car_seat_finder import (
    SEATS,
    choose_stage,
    rank_seats,
    stage_label,
    get_limits,
    NHTSA_CAR_SEATS_URL,
    NHTSA_RECALLS_URL,
    NHTSA_INSPECTION_URL,
)

st.set_page_config(
    page_title="Car Seat Finder",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------
# Small UI helpers
# ------------------------------

def yes_no(value: bool) -> str:
    return "Yes" if value else "No"


def mode_text(seat) -> str:
    modes = []
    if seat.rear_facing:
        modes.append("Rear-facing")
    if seat.forward_facing:
        modes.append("Forward-facing harness")
    if seat.booster:
        modes.append("Booster")
    return " · ".join(modes)


def max_limit(limits, attr):
    if limits is None:
        return "—"
    value = getattr(limits, attr)
    if value is None:
        return "See manual"
    unit = " lb" if attr == "max_weight" else " in"
    return f"{value:g}{unit}"


def render_result(rank, result, stage):
    score, seat, reasons = result
    limits = get_limits(seat, stage)

    medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(rank, f"#{rank}")

    with st.container(border=True):
        title_col, price_col = st.columns([4, 1])
        with title_col:
            st.subheader(f"{medal} {seat.full_name}")
            st.caption(seat.notes)
        with price_col:
            st.metric("Reference price", f"${seat.price:,.0f}")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Match score", f"{score:.1f}")
        c2.metric("Width", f'{seat.width:.1f}"')
        c3.metric("Mode max weight", max_limit(limits, "max_weight"))
        c4.metric("Mode max height", max_limit(limits, "max_height"))

        st.markdown("**Why it matched**")
        if reasons:
            st.markdown("\n".join(f"- {reason.capitalize()}" for reason in reasons[:7]))
        else:
            st.write("This seat passed the hard fit filters for the selected mode.")

        with st.expander("Seat details"):
            d1, d2, d3 = st.columns(3)
            with d1:
                st.write(f"**Modes:** {mode_text(seat)}")
                st.write(f"**Seat weight:** {seat.seat_weight:.1f} lb")
                st.write(f"**Front-to-back catalog dimension:** {seat.depth:.1f} in")
            with d2:
                st.write(f"**Rotates:** {yes_no(seat.rotating)}")
                st.write(f"**Anti-rebound feature:** {yes_no(seat.anti_rebound)}")
                st.write(f"**Belt tensioner / lockoff:** {yes_no(seat.belt_tensioner_or_lockoff)}")
            with d3:
                st.write(f"**Machine washable:** {yes_no(seat.machine_washable)}")
                st.write(f"**Aircraft approved:** {yes_no(seat.aircraft_approved)}")
                st.write(f"**Listed lifespan:** {seat.lifespan_years} years")

            st.caption(f"Catalog source note: {seat.source}")


# ------------------------------
# Header
# ------------------------------

st.title("🚗 Car Seat Finder")
st.markdown(
    """
**Find compatible car seats based on your child, vehicle needs, budget, and preferences.**

This tool filters out seats that do not fit the entered child in the selected restraint mode,
then ranks the remaining options using growth room, installation features, vehicle fit,
practical features, and value.
"""
)

st.warning(
    "Shopping/research aid only. Always verify the current manufacturer manual, labels, "
    "height/weight limits, vehicle fit, manufacture/expiration date, and recall status before use."
)

tab_find, tab_compare, tab_catalog, tab_method = st.tabs(
    ["🔎 Find a Seat", "⚖️ Compare", "📚 Catalog", "ℹ️ Methodology"]
)

# ------------------------------
# FIND
# ------------------------------

with tab_find:
    st.header("Tell us about the child")

    with st.form("seat_search_form"):
        a1, a2, a3 = st.columns(3)
        with a1:
            age = st.number_input(
                "Age (years)",
                min_value=0.0,
                max_value=15.0,
                value=1.5,
                step=0.1,
                help="Examples: 0.5 = 6 months, 1.5 = 18 months.",
            )
        with a2:
            weight = st.number_input(
                "Weight (lb)",
                min_value=1.0,
                max_value=150.0,
                value=25.0,
                step=0.5,
            )
        with a3:
            height = st.number_input(
                "Height (inches)",
                min_value=10.0,
                max_value=80.0,
                value=33.0,
                step=0.5,
            )

        booster_mature = False
        if age >= 5:
            booster_mature = st.checkbox(
                "The child can sit upright with the lap/shoulder belt correctly positioned for the entire ride",
                value=False,
                help="Booster readiness depends on both size and behavior.",
            )

        stage_choice = st.selectbox(
            "Restraint stage",
            [
                "Auto — choose an appropriate stage for this search",
                "Rear-facing",
                "Forward-facing 5-point harness",
                "Belt-positioning booster",
            ],
            index=0,
        )

        st.divider()
        st.subheader("Vehicle and preferences")

        p1, p2 = st.columns(2)
        with p1:
            use_budget = st.checkbox("Set a maximum budget", value=True)
            max_budget = st.number_input(
                "Maximum budget ($)",
                min_value=25.0,
                max_value=1500.0,
                value=400.0,
                step=25.0,
                disabled=not use_budget,
            )
            three_across = st.checkbox(
                "Need a narrow seat / possible 3-across setup",
                value=False,
            )
            compact_backseat = st.checkbox(
                "Front-to-back space is limited",
                value=False,
            )
        with p2:
            travel_often = st.checkbox(
                "Frequently move or fly with the seat",
                value=False,
            )
            wants_rotation = st.checkbox(
                "Rotating seat is important",
                value=False,
            )
            wants_fr_free = st.checkbox(
                "Prefer materials marketed as free of added flame-retardant chemicals",
                value=False,
            )
            wants_infant_carrier = st.checkbox(
                "Prefer a removable infant-carrier style seat",
                value=False,
                disabled=age >= 2,
            )

        submitted = st.form_submit_button(
            "Find my best matches",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        if stage_choice.startswith("Auto"):
            stage = choose_stage(age, booster_mature)
        elif stage_choice.startswith("Rear"):
            stage = "rear"
        elif stage_choice.startswith("Forward"):
            stage = "forward"
        else:
            stage = "booster"

        if stage == "booster" and not booster_mature:
            st.error(
                "This search will not rank boosters unless the child can remain correctly "
                "positioned for the entire ride. Choose a harnessed mode or confirm booster readiness."
            )
        else:
            budget = float(max_budget) if use_budget else None

            results = rank_seats(
                age_years=float(age),
                weight=float(weight),
                height=float(height),
                stage=stage,
                max_budget=budget,
                three_across=three_across,
                compact_backseat=compact_backseat,
                travel_often=travel_often,
                wants_rotation=wants_rotation,
                wants_fr_free=wants_fr_free,
                wants_infant_carrier=wants_infant_carrier,
            )

            st.session_state["last_results"] = results
            st.session_state["last_stage"] = stage

            if not results:
                st.error(
                    "No seats in the starter catalog passed all hard filters. "
                    "Try increasing the budget or reviewing the selected restraint stage."
                )
            else:
                st.success(
                    f"Found {len(results)} compatible starter-catalog seat(s) in "
                    f"**{stage_label(stage)}** mode."
                )
                st.caption(
                    "A higher match score means a better fit for the preferences entered — "
                    "it is not a crash-test safety score."
                )

                for idx, result in enumerate(results[:5], start=1):
                    render_result(idx, result, stage)

                st.divider()
                st.subheader("Before you buy or use any seat")
                st.markdown(
                    """
1. Verify the **current manufacturer manual and labels** for the exact model.
2. Confirm the seat can be **installed correctly in your actual vehicle**.
3. Check **NHTSA recalls** using the exact model/model number.
4. Check the **manufacture and expiration dates**.
5. For a used seat, verify its **crash history and missing/replacement parts**.
6. Consider a **Child Passenger Safety Technician (CPST)** inspection.
"""
                )

                r1, r2, r3 = st.columns(3)
                r1.link_button("NHTSA car-seat guidance", NHTSA_CAR_SEATS_URL, use_container_width=True)
                r2.link_button("Check NHTSA recalls", NHTSA_RECALLS_URL, use_container_width=True)
                r3.link_button("Find installation help", NHTSA_INSPECTION_URL, use_container_width=True)

# ------------------------------
# COMPARE
# ------------------------------

with tab_compare:
    st.header("Compare two seats")

    names = [seat.full_name for seat in SEATS]
    c1, c2 = st.columns(2)
    with c1:
        seat_a_name = st.selectbox("Seat A", names, index=0, key="seat_a")
    with c2:
        default_b = 1 if len(names) > 1 else 0
        seat_b_name = st.selectbox("Seat B", names, index=default_b, key="seat_b")

    seat_a = next(s for s in SEATS if s.full_name == seat_a_name)
    seat_b = next(s for s in SEATS if s.full_name == seat_b_name)

    fields = [
        ("Reference price", f"${seat_a.price:,.2f}", f"${seat_b.price:,.2f}"),
        ("Width", f'{seat_a.width:.1f}"', f'{seat_b.width:.1f}"'),
        ("Seat weight", f"{seat_a.seat_weight:.1f} lb", f"{seat_b.seat_weight:.1f} lb"),
        ("Rear-facing max", max_limit(seat_a.rear_facing, "max_weight"), max_limit(seat_b.rear_facing, "max_weight")),
        ("Forward-facing max", max_limit(seat_a.forward_facing, "max_weight"), max_limit(seat_b.forward_facing, "max_weight")),
        ("Booster max", max_limit(seat_a.booster, "max_weight"), max_limit(seat_b.booster, "max_weight")),
        ("Rotates", yes_no(seat_a.rotating), yes_no(seat_b.rotating)),
        ("Anti-rebound feature", yes_no(seat_a.anti_rebound), yes_no(seat_b.anti_rebound)),
        ("Belt tensioner / lockoff", yes_no(seat_a.belt_tensioner_or_lockoff), yes_no(seat_b.belt_tensioner_or_lockoff)),
        ("Machine washable", yes_no(seat_a.machine_washable), yes_no(seat_b.machine_washable)),
        ("Aircraft approved", yes_no(seat_a.aircraft_approved), yes_no(seat_b.aircraft_approved)),
        ("Listed lifespan", f"{seat_a.lifespan_years} years", f"{seat_b.lifespan_years} years"),
    ]

    st.table({
        "Feature": [row[0] for row in fields],
        seat_a.full_name: [row[1] for row in fields],
        seat_b.full_name: [row[2] for row in fields],
    })

    st.caption(
        "Comparison values come from the starter catalog. Verify exact current specifications "
        "with the manufacturer before making a purchase or use decision."
    )

# ------------------------------
# CATALOG
# ------------------------------

with tab_catalog:
    st.header("Starter catalog")
    search = st.text_input("Search brand or model", placeholder="Example: Graco, rotating, Poplar")

    filtered = [
        seat for seat in SEATS
        if not search.strip()
        or search.lower() in seat.full_name.lower()
        or search.lower() in seat.notes.lower()
    ]

    st.caption(f"{len(filtered)} seat(s) shown")

    for seat in filtered:
        with st.expander(f"{seat.full_name} — ${seat.price:,.0f}"):
            st.write(f"**Modes:** {mode_text(seat)}")
            st.write(f"**Width:** {seat.width:.1f} in")
            st.write(f"**Seat weight:** {seat.seat_weight:.1f} lb")
            st.write(f"**Notes:** {seat.notes}")
            st.caption(seat.source)

# ------------------------------
# METHODOLOGY
# ------------------------------

with tab_method:
    st.header("How the ranking works")

    st.markdown(
        """
### 1. Hard filters come first

A seat must fit the entered child within the catalog's manufacturer limits for the selected
mode. If a maximum budget is supplied, seats above that budget are removed.

### 2. Compatible seats are ranked

The current score considers:

- **Growth room:** remaining weight and height capacity in the selected mode.
- **Installation / everyday use:** belt tensioners or lockoffs, no-rethread harnesses,
  level indicators, easier LATCH hardware, and similar usability features.
- **Vehicle fit:** especially width for narrow/3-across situations and approximate
  front-to-back dimensions when space is limited.
- **Practical ownership:** washable covers, travel weight, aircraft approval, rotation,
  and listed usable lifespan.
- **Selected design features:** modest weighting for features such as anti-rebound
  equipment.
- **Value:** reference price relative to the user's budget.

### What the score does **not** mean

The match score is **not a crash-safety rating**. It is a recommendation score for the
criteria entered.

NHTSA's Ease-of-Use ratings should not be treated as a universal crash-performance
ranking, and this app intentionally does not do that.

### Important limitations

The starter catalog is intentionally small and should be expanded before treating this
as a comprehensive consumer product. Prices and model specifications change. Vehicle fit
cannot be guaranteed from catalog dimensions alone. Recall status must be checked using
the exact model/model number.
"""
    )

    st.info("Starter catalog research date: September 2026.")

    m1, m2, m3 = st.columns(3)
    m1.link_button("NHTSA guidance", NHTSA_CAR_SEATS_URL, use_container_width=True)
    m2.link_button("NHTSA recalls", NHTSA_RECALLS_URL, use_container_width=True)
    m3.link_button("Installation help", NHTSA_INSPECTION_URL, use_container_width=True)

# ------------------------------
# Sidebar
# ------------------------------

with st.sidebar:
    st.header("About this project")
    st.write(
        "A research-informed car-seat matching prototype built in Python and Streamlit."
    )
    st.caption(
        "Version 1 uses a starter catalog. Before broad public promotion, expand and "
        "regularly maintain the product database."
    )
    st.divider()
    st.link_button("NHTSA car-seat guidance", NHTSA_CAR_SEATS_URL, use_container_width=True)
    st.link_button("NHTSA recalls", NHTSA_RECALLS_URL, use_container_width=True)
