#!/usr/bin/env python3
"""
Car Seat Finder / Ranker
------------------------

A beginner-friendly command-line program that helps a user narrow down and
rank child restraints based on:

1) Whether the child fits the seat in the appropriate mode
2) Keeping a young child rear-facing when appropriate and within seat limits
3) Remaining growth room in the current mode
4) Installation / everyday-use features
5) Vehicle-space constraints
6) Practical features and travel needs
7) Price / value
8) Recall awareness

IMPORTANT:
- This program is a shopping/research aid, not a substitute for the car-seat
  manual, vehicle manual, state law, NHTSA guidance, or a Child Passenger
  Safety Technician (CPST).
- NHTSA Ease-of-Use ratings are NOT crash-safety ratings.
- Product specifications and prices change. Always verify the current manual,
  labels, fit limits, manufacture/expiration date, and recall status before use.
- Never use this program to decide that a recalled, expired, crashed, or
  otherwise unsafe seat is acceptable.

Starter catalog research date: September 2026.
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Tuple
import webbrowser

NHTSA_CAR_SEATS_URL = "https://www.nhtsa.gov/vehicle-safety/car-seats-and-booster-seats"
NHTSA_RECALLS_URL = "https://www.nhtsa.gov/recalls"
NHTSA_INSPECTION_URL = "https://www.nhtsa.gov/equipment/car-seats-and-booster-seats#installation-help-inspection"

# ---------------------------------------------------------------------------
# DATA MODEL
# ---------------------------------------------------------------------------

@dataclass
class ModeLimits:
    min_weight: float
    max_weight: float
    min_height: Optional[float] = None
    max_height: Optional[float] = None
    min_age_years: Optional[float] = None

    def fits(self, weight: float, height: float, age_years: float) -> bool:
        if weight < self.min_weight or weight > self.max_weight:
            return False
        if self.min_height is not None and height < self.min_height:
            return False
        if self.max_height is not None and height > self.max_height:
            return False
        if self.min_age_years is not None and age_years < self.min_age_years:
            return False
        return True


@dataclass
class CarSeat:
    brand: str
    model: str
    price: float
    width: float
    depth: float
    seat_weight: float

    rear_facing: Optional[ModeLimits] = None
    forward_facing: Optional[ModeLimits] = None
    booster: Optional[ModeLimits] = None

    # Ease / installation features
    belt_tensioner_or_lockoff: bool = False
    no_rethread_harness: bool = False
    level_indicator: bool = False
    rotating: bool = False
    easy_latch: bool = False
    ready_to_ride_indicator: bool = False

    # Practical / design features
    machine_washable: bool = False
    aircraft_approved: bool = False
    anti_rebound: bool = False
    load_leg: bool = False
    fr_free_materials: bool = False
    lifespan_years: int = 8

    # Optional metadata
    notes: str = ""
    source: str = ""

    @property
    def full_name(self) -> str:
        return f"{self.brand} {self.model}"


# ---------------------------------------------------------------------------
# STARTER CATALOG
# ---------------------------------------------------------------------------
# Reference specs were taken from manufacturer pages during September 2026
# research. Prices are reference prices / MSRP-like values and can change.
#
# For a production app, move these records into JSON/CSV and update them
# regularly from manufacturer manuals and official product pages.

SEATS: List[CarSeat] = [
    CarSeat(
        brand="Graco",
        model="Extend2Fit 3-in-1 with Anti-Rebound Bar",
        price=339.99,
        width=19.0,
        depth=26.75,
        seat_weight=21.9,
        rear_facing=ModeLimits(4, 50),
        forward_facing=ModeLimits(26.5, 65, max_height=49, min_age_years=2),
        booster=ModeLimits(40, 100, min_height=43, max_height=57, min_age_years=4),
        no_rethread_harness=True,
        level_indicator=True,
        easy_latch=True,
        machine_washable=True,
        anti_rebound=True,
        lifespan_years=10,
        notes="Strong extended rear-facing value; converts to high-back booster.",
        source="Graco manufacturer specifications"
    ),
    CarSeat(
        brand="Britax",
        model="Poplar S",
        price=349.99,
        width=17.0,
        depth=20.5,
        seat_weight=28.0,
        rear_facing=ModeLimits(5, 50, min_height=18, max_height=49),
        forward_facing=ModeLimits(30, 65, min_height=35, max_height=49),
        belt_tensioner_or_lockoff=True,
        no_rethread_harness=True,
        ready_to_ride_indicator=False,
        machine_washable=True,
        anti_rebound=True,
        fr_free_materials=True,
        lifespan_years=10,
        notes="Slim 17-inch convertible seat with ClickTight installation.",
        source="Britax manufacturer specifications"
    ),
    CarSeat(
        brand="Evenflo",
        model="Revolve360 Slim 2-in-1",
        price=399.99,
        width=16.9,
        depth=21.0,
        seat_weight=28.2,
        rear_facing=ModeLimits(4, 50, min_height=17, max_height=48),
        forward_facing=ModeLimits(30, 65, min_height=35, max_height=49, min_age_years=2),
        belt_tensioner_or_lockoff=True,
        no_rethread_harness=True,
        level_indicator=True,
        rotating=True,
        machine_washable=True,
        lifespan_years=10,
        notes="Very narrow rotating convertible seat; extended rear-facing to 50 lb.",
        source="Evenflo manufacturer specifications"
    ),
    CarSeat(
        brand="Chicco",
        model="Fit360 ClearTex",
        price=439.99,
        width=18.25,
        depth=32.25,  # rear-facing footprint; forward-facing is shorter
        seat_weight=31.25,
        rear_facing=ModeLimits(4, 40, max_height=43),
        forward_facing=ModeLimits(26.5, 65, max_height=49, min_age_years=2),
        belt_tensioner_or_lockoff=True,
        no_rethread_harness=True,
        rotating=True,
        ready_to_ride_indicator=True,
        machine_washable=True,
        aircraft_approved=True,
        fr_free_materials=True,
        lifespan_years=10,
        notes="360-degree rotation, LeverLock installation, magnetic chest clip.",
        source="Chicco manufacturer specifications"
    ),
    CarSeat(
        brand="Clek",
        model="Fllo",
        price=429.99,
        width=16.9,
        depth=32.5,
        seat_weight=28.0,
        rear_facing=ModeLimits(14, 50, min_height=25, max_height=43),
        forward_facing=ModeLimits(26.5, 65, min_height=30, max_height=49, min_age_years=2),
        aircraft_approved=True,
        anti_rebound=True,
        lifespan_years=9,
        notes="Very narrow; 5-lb newborn use requires the separately sold Infant-Thingy.",
        source="Clek manufacturer specifications"
    ),
    CarSeat(
        brand="Nuna",
        model="RAVA",
        price=399.99,
        width=19.0,
        depth=16.0,
        seat_weight=27.9,
        rear_facing=ModeLimits(5, 50, min_height=18, max_height=49),
        forward_facing=ModeLimits(30, 65, min_height=34, max_height=49, min_age_years=2),
        belt_tensioner_or_lockoff=True,
        no_rethread_harness=True,
        machine_washable=True,
        fr_free_materials=True,
        lifespan_years=10,
        notes="Convertible seat with tensioning doors and 50-lb rear-facing limit.",
        source="Nuna manufacturer specifications"
    ),
    CarSeat(
        brand="Graco",
        model="Extend2Fit 3-in-1",
        price=269.99,
        width=19.0,
        depth=20.75,
        seat_weight=20.6,
        rear_facing=ModeLimits(4, 50),
        forward_facing=ModeLimits(26.5, 65, max_height=49, min_age_years=2),
        booster=ModeLimits(40, 100, min_height=43, max_height=57, min_age_years=4),
        no_rethread_harness=True,
        level_indicator=True,
        easy_latch=True,
        machine_washable=True,
        lifespan_years=10,
        notes="Lower-cost extended rear-facing option; high-back booster mode.",
        source="Graco manufacturer specifications"
    ),
    # Dedicated infant-seat examples
    CarSeat(
        brand="Chicco",
        model="KeyFit 35 ClearTex",
        price=269.99,
        width=16.5,
        depth=28.75,
        seat_weight=10.0,
        rear_facing=ModeLimits(4, 35, max_height=32),
        belt_tensioner_or_lockoff=True,
        level_indicator=True,
        easy_latch=True,
        machine_washable=True,
        aircraft_approved=True,
        anti_rebound=True,
        lifespan_years=6,
        notes="Rear-facing infant carrier; convenient if a removable carrier is important.",
        source="Chicco manufacturer specifications"
    ),
    CarSeat(
        brand="Graco",
        model="SnugRide SnugFit DLX",
        price=239.99,
        width=17.5,
        depth=27.5,
        seat_weight=9.8,
        rear_facing=ModeLimits(4, 30, max_height=32),
        no_rethread_harness=True,
        level_indicator=True,
        easy_latch=True,
        machine_washable=True,
        aircraft_approved=True,
        anti_rebound=True,
        lifespan_years=7,
        notes="Rear-facing infant carrier; current Graco page lists 4-30 lb and up to 32 in.",
        source="Graco manufacturer specifications"
    ),
    # Booster-focused examples
    CarSeat(
        brand="Graco",
        model="TurboBooster 2.0 Highback",
        price=59.99,
        width=19.84,
        depth=10.51,
        seat_weight=10.76,
        booster=ModeLimits(40, 100, min_height=43, max_height=57, min_age_years=4),
        machine_washable=True,
        aircraft_approved=False,
        lifespan_years=10,
        notes="Budget high-back booster. Confirm belt fit in the actual vehicle.",
        source="Graco manufacturer specifications"
    ),
    CarSeat(
        brand="Britax",
        model="Highpoint",
        price=199.99,
        width=21.0,
        depth=16.0,
        seat_weight=12.0,
        booster=ModeLimits(40, 120, min_height=44, max_height=63, min_age_years=4),
        machine_washable=True,
        lifespan_years=10,
        notes="High-back belt-positioning booster; verify lap/shoulder belt fit.",
        source="Starter catalog reference; verify current Britax manual"
    ),
]


# ---------------------------------------------------------------------------
# INPUT HELPERS
# ---------------------------------------------------------------------------

def ask_float(prompt: str, minimum: float = 0, allow_blank: bool = False) -> Optional[float]:
    while True:
        raw = input(prompt).strip()
        if allow_blank and raw == "":
            return None
        try:
            value = float(raw)
            if value < minimum:
                print(f"Please enter a number >= {minimum}.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")


def ask_yes_no(prompt: str, default: Optional[bool] = None) -> bool:
    suffix = " [Y/n]: " if default is True else " [y/N]: " if default is False else " [y/n]: "
    while True:
        raw = input(prompt + suffix).strip().lower()
        if raw == "" and default is not None:
            return default
        if raw in ("y", "yes"):
            return True
        if raw in ("n", "no"):
            return False
        print("Please enter y or n.")


def ask_choice(prompt: str, choices: Dict[str, str]) -> str:
    print(prompt)
    for key, label in choices.items():
        print(f"  {key}. {label}")
    while True:
        raw = input("Choice: ").strip()
        if raw in choices:
            return raw
        print("Please choose one of:", ", ".join(choices))


# ---------------------------------------------------------------------------
# SAFETY-STAGE LOGIC
# ---------------------------------------------------------------------------

def choose_stage(age_years: float, booster_mature: bool) -> str:
    """
    Conservative automatic stage selection.

    - Under 4: prefer rear-facing when the child still fits a rear-facing seat.
    - 4 to under 5: forward-facing harness.
    - 5+: booster only if caregiver says child can sit correctly for the whole ride;
      otherwise continue a harnessed seat if one still fits.

    The program still checks each individual seat's manufacturer limits.
    """
    if age_years < 4:
        return "rear"
    if age_years < 5:
        return "forward"
    return "booster" if booster_mature else "forward"


def get_limits(seat: CarSeat, stage: str) -> Optional[ModeLimits]:
    return {
        "rear": seat.rear_facing,
        "forward": seat.forward_facing,
        "booster": seat.booster,
    }.get(stage)


# ---------------------------------------------------------------------------
# SCORING
# ---------------------------------------------------------------------------

def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def score_growth_room(limits: ModeLimits, weight: float, height: float) -> Tuple[float, List[str]]:
    reasons = []

    weight_room = max(0.0, limits.max_weight - weight)
    weight_span = max(1.0, limits.max_weight - limits.min_weight)
    weight_score = 18 * clamp(weight_room / weight_span, 0, 1)

    if limits.max_height is not None:
        height_room = max(0.0, limits.max_height - height)
        if limits.min_height is None:
            height_span = max(1.0, limits.max_height)
        else:
            height_span = max(1.0, limits.max_height - limits.min_height)
        height_score = 12 * clamp(height_room / height_span, 0, 1)
    else:
        height_score = 7.0  # unknown exact max; don't over-reward or punish

    if weight_room >= 15:
        reasons.append(f"{weight_room:.0f} lb of weight room in this mode")
    elif weight_room >= 7:
        reasons.append(f"{weight_room:.0f} lb of remaining weight room")

    return weight_score + height_score, reasons


def score_installation(seat: CarSeat) -> Tuple[float, List[str]]:
    score = 0.0
    reasons = []

    if seat.belt_tensioner_or_lockoff:
        score += 6
        reasons.append("built-in belt tensioner/lockoff")
    if seat.no_rethread_harness:
        score += 4
        reasons.append("no-rethread harness")
    if seat.level_indicator:
        score += 3
        reasons.append("level/recline indicator")
    if seat.easy_latch:
        score += 2
        reasons.append("easy LATCH attachment")
    if seat.ready_to_ride_indicator:
        score += 2
        reasons.append("ready-to-ride indicator")
    if seat.rotating:
        score += 3
        reasons.append("rotation can make daily loading easier")

    return min(score, 20), reasons


def score_vehicle_fit(
    seat: CarSeat,
    three_across: bool,
    compact_backseat: bool,
    stage: str,
) -> Tuple[float, List[str]]:
    score = 0.0
    reasons = []

    if three_across:
        if seat.width <= 17.0:
            score += 10
            reasons.append(f"very narrow at {seat.width:.1f} in")
        elif seat.width <= 18.0:
            score += 7
            reasons.append(f"relatively narrow at {seat.width:.1f} in")
        elif seat.width <= 19.0:
            score += 3
        else:
            score -= 3
    else:
        # Width still matters, just less.
        score += clamp((21.0 - seat.width) / 4.0 * 5.0, 0, 5)

    if compact_backseat:
        # Depth values are approximate catalog dimensions and not a substitute
        # for an actual vehicle fit test.
        if seat.depth <= 23:
            score += 5
            reasons.append("shorter catalog front-to-back dimension")
        elif seat.depth <= 28:
            score += 2
        else:
            score -= 2
    else:
        score += 2

    return clamp(score, 0, 15), reasons


def score_practical(
    seat: CarSeat,
    travel_often: bool,
    wants_rotation: bool,
    wants_fr_free: bool,
) -> Tuple[float, List[str]]:
    score = 0.0
    reasons = []

    if seat.machine_washable:
        score += 3
        reasons.append("machine-washable fabrics")

    # Long usable life gets a small ownership-value bonus.
    score += clamp((seat.lifespan_years - 6) / 4 * 2, 0, 2)

    if travel_often:
        if seat.aircraft_approved:
            score += 2
            reasons.append("aircraft approved")
        # Lighter seats are easier to move.
        if seat.seat_weight <= 12:
            score += 3
            reasons.append("relatively light for travel")
        elif seat.seat_weight <= 22:
            score += 1
    else:
        score += 1

    if wants_rotation:
        if seat.rotating:
            score += 3
        else:
            score -= 1

    if wants_fr_free and seat.fr_free_materials:
        score += 2
        reasons.append("manufacturer lists FR-free materials")

    return clamp(score, 0, 10), reasons


def score_design_features(seat: CarSeat, stage: str) -> Tuple[float, List[str]]:
    """
    Deliberately modest weighting.

    Added design features are not treated as a universal crash-test ranking.
    Correct fit, correct installation, correct use, and staying within the
    appropriate restraint stage matter more.
    """
    score = 0.0
    reasons = []

    if stage == "rear" and seat.anti_rebound:
        score += 4
        reasons.append("anti-rebound feature")
    if stage == "rear" and seat.load_leg:
        score += 3
        reasons.append("load leg")
    if seat.rotating:
        # Daily ease can indirectly help correct use, but it is not a crash
        # performance score.
        score += 1
    if seat.fr_free_materials:
        score += 1

    return min(score, 8), reasons


def score_value(seat: CarSeat, max_budget: Optional[float]) -> Tuple[float, List[str]]:
    score = 0.0
    reasons = []

    if max_budget is not None:
        if seat.price > max_budget:
            return -999, ["over budget"]
        # Better value when well below the user's ceiling.
        remaining = max_budget - seat.price
        score = 12 * clamp(0.35 + remaining / max(max_budget, 1), 0, 1)
    else:
        if seat.price <= 100:
            score = 12
        elif seat.price <= 250:
            score = 10
        elif seat.price <= 350:
            score = 8
        elif seat.price <= 450:
            score = 6
        else:
            score = 4

    if seat.price <= 300:
        reasons.append(f"stronger price value (${seat.price:.0f} reference price)")

    return score, reasons


def rank_seats(
    age_years: float,
    weight: float,
    height: float,
    stage: str,
    max_budget: Optional[float],
    three_across: bool,
    compact_backseat: bool,
    travel_often: bool,
    wants_rotation: bool,
    wants_fr_free: bool,
    wants_infant_carrier: bool,
) -> List[Tuple[float, CarSeat, List[str]]]:

    results = []

    for seat in SEATS:
        limits = get_limits(seat, stage)
        if limits is None:
            continue

        if not limits.fits(weight, height, age_years):
            continue

        # The current Clek Fllo rear-facing instructions require a child using
        # the seat without the optional Infant-Thingy to be able to sit upright
        # alone. Because this program does not assess developmental readiness,
        # do not auto-rank that configuration for children under 1 year.
        if stage == "rear" and seat.brand == "Clek" and seat.model == "Fllo" and age_years < 1:
            continue

        if max_budget is not None and seat.price > max_budget:
            continue

        # If the user specifically wants an infant carrier, favor light,
        # infant-only rear-facing seats. This is a convenience preference,
        # not a safety ranking.
        carrier_bonus = 0.0
        carrier_reason = []
        if stage == "rear" and wants_infant_carrier:
            is_likely_carrier = seat.forward_facing is None and seat.booster is None and seat.seat_weight <= 15
            if is_likely_carrier:
                carrier_bonus = 8
                carrier_reason = ["matches removable infant-carrier preference"]
            else:
                carrier_bonus = -4

        growth, r1 = score_growth_room(limits, weight, height)
        install, r2 = score_installation(seat)
        vehicle, r3 = score_vehicle_fit(seat, three_across, compact_backseat, stage)
        practical, r4 = score_practical(seat, travel_often, wants_rotation, wants_fr_free)
        design, r5 = score_design_features(seat, stage)
        value, r6 = score_value(seat, max_budget)

        # 100-ish point scale.
        total = growth + install + vehicle + practical + design + value + carrier_bonus

        reasons = r1 + r2 + r3 + r4 + r5 + r6 + carrier_reason
        results.append((round(total, 1), seat, reasons))

    results.sort(key=lambda x: x[0], reverse=True)
    return results


# ---------------------------------------------------------------------------
# DISPLAY
# ---------------------------------------------------------------------------

def stage_label(stage: str) -> str:
    return {
        "rear": "rear-facing",
        "forward": "forward-facing 5-point harness",
        "booster": "belt-positioning booster",
    }[stage]


def print_seat_detail(rank: int, score: float, seat: CarSeat, reasons: List[str], stage: str):
    print("\n" + "=" * 76)
    print(f"#{rank}: {seat.full_name}")
    print(f"Match score: {score:.1f}")
    print(f"Reference price: ${seat.price:,.2f}")
    print(f"Width: {seat.width:.1f} in | Seat weight: {seat.seat_weight:.1f} lb")
    print(f"Mode evaluated: {stage_label(stage)}")
    print(f"Why it ranked well:")
    for reason in reasons[:7]:
        print(f"  • {reason}")
    if seat.notes:
        print(f"Notes: {seat.notes}")
    print(f"Data source note: {seat.source}")


def print_methodology():
    print("""
SCORING PHILOSOPHY
------------------
Hard filter first:
  • The child must fit the manufacturer's listed limits for the evaluated mode.
  • The seat must be within budget if a maximum budget is supplied.

Then the remaining seats are ranked using:
  1. Growth room in the appropriate mode
  2. Installation / everyday-use features
  3. Width and front-to-back vehicle-space considerations
  4. Practical ownership and travel features
  5. A small bonus for selected design features
  6. Price / value

What this program deliberately DOES NOT do:
  • It does not call NHTSA's Ease-of-Use stars a crash-safety score.
  • It does not claim one compliant U.S. seat is universally "safer" than another
    based only on marketing features.
  • It does not guarantee vehicle fit.
  • It does not replace a recall check, product manual, vehicle manual, or CPST.

For boosters, actual lap-and-shoulder belt fit in the specific vehicle is critical.
""")


# ---------------------------------------------------------------------------
# MAIN SEARCH FLOW
# ---------------------------------------------------------------------------

def find_best_seat():
    print("\nCHILD INFORMATION")
    print("-----------------")
    age = ask_float("Child age in years (examples: 0.5, 2, 6): ", 0)
    weight = ask_float("Child weight in pounds: ", 1)
    height = ask_float("Child height in inches: ", 10)

    booster_mature = False
    if age >= 5:
        booster_mature = ask_yes_no(
            "Can the child sit upright with the belt correctly positioned for the entire ride?",
            default=False,
        )

    stage_mode = ask_choice(
        "\nChoose restraint stage:",
        {
            "1": "Auto (recommended for this search)",
            "2": "Rear-facing",
            "3": "Forward-facing 5-point harness",
            "4": "Belt-positioning booster",
        },
    )

    if stage_mode == "1":
        stage = choose_stage(age, booster_mature)
    else:
        stage = {"2": "rear", "3": "forward", "4": "booster"}[stage_mode]

    if stage == "booster" and not booster_mature:
        booster_mature = ask_yes_no(
            "For booster use, can the child remain properly seated with the lap/shoulder belt correctly positioned for the ENTIRE ride?",
            default=False,
        )
        if not booster_mature:
            print("\nThis program will not rank boosters for a child who cannot yet stay properly positioned.")
            print("Searching forward-facing harness seats instead.")
            stage = "forward"

    print(f"\nSearching in: {stage_label(stage)} mode")

    max_budget = ask_float(
        "Maximum budget in dollars (press Enter for no maximum): $",
        0,
        allow_blank=True,
    )

    print("\nVEHICLE / PREFERENCE INFORMATION")
    print("--------------------------------")
    three_across = ask_yes_no("Do you need a narrow seat / possible 3-across setup?", default=False)
    compact_backseat = ask_yes_no("Is front-to-back space limited in the vehicle?", default=False)
    travel_often = ask_yes_no("Will you frequently move/fly with this seat?", default=False)
    wants_rotation = ask_yes_no("Is a rotating seat important to you?", default=False)
    wants_fr_free = ask_yes_no("Do you prefer materials marketed as free of added flame-retardant chemicals?", default=False)

    wants_infant_carrier = False
    if stage == "rear" and age < 2:
        wants_infant_carrier = ask_yes_no(
            "Do you specifically want a removable infant-carrier style seat?",
            default=False,
        )

    results = rank_seats(
        age_years=age,
        weight=weight,
        height=height,
        stage=stage,
        max_budget=max_budget,
        three_across=three_across,
        compact_backseat=compact_backseat,
        travel_often=travel_often,
        wants_rotation=wants_rotation,
        wants_fr_free=wants_fr_free,
        wants_infant_carrier=wants_infant_carrier,
    )

    if not results:
        print("\nNo seats in the starter catalog match all of those hard filters.")
        print("Try increasing the budget or manually choosing another appropriate stage.")
        print("Always confirm any stage transition against current NHTSA guidance and the seat manual.")
        return

    print("\nTOP MATCHES")
    print("-----------")
    for i, (score, seat, reasons) in enumerate(results[:5], start=1):
        print_seat_detail(i, score, seat, reasons, stage)

    print("\n" + "-" * 76)
    print("FINAL CHECKS BEFORE BUYING/USING ANY SEAT")
    print("1. Verify current manufacturer height/weight/age limits and the seat's manual.")
    print("2. Verify the seat physically fits your vehicle and can be installed correctly.")
    print("3. Check NHTSA recall information using the exact model/model number.")
    print("4. Check manufacture date / expiration date.")
    print("5. For a used seat, confirm crash history and that all original parts are present.")
    print("6. Consider a CPST inspection after installation.")
    print("-" * 76)


def search_catalog():
    term = input("\nEnter brand or model text: ").strip().lower()
    matches = [s for s in SEATS if term in s.full_name.lower()]
    if not matches:
        print("No starter-catalog matches.")
        return

    for seat in matches:
        print("\n" + seat.full_name)
        print(f"  Reference price: ${seat.price:,.2f}")
        print(f"  Width: {seat.width:.1f} in")
        modes = []
        if seat.rear_facing:
            modes.append("rear-facing")
        if seat.forward_facing:
            modes.append("forward-facing harness")
        if seat.booster:
            modes.append("booster")
        print("  Modes:", ", ".join(modes))
        print("  Notes:", seat.notes)


def compare_two():
    print("\nAvailable seats:")
    for i, seat in enumerate(SEATS, start=1):
        print(f"{i:2}. {seat.full_name}")

    def get_index(label: str) -> int:
        while True:
            raw = input(f"{label} number: ").strip()
            if raw.isdigit():
                idx = int(raw)
                if 1 <= idx <= len(SEATS):
                    return idx - 1
            print("Invalid selection.")

    a = SEATS[get_index("First seat")]
    b = SEATS[get_index("Second seat")]

    print("\n" + "=" * 76)
    print(f"{'FIELD':30} | {a.full_name[:20]:20} | {b.full_name[:20]:20}")
    print("=" * 76)
    rows = [
        ("Reference price", f"${a.price:.2f}", f"${b.price:.2f}"),
        ("Width", f"{a.width:.1f} in", f"{b.width:.1f} in"),
        ("Seat weight", f"{a.seat_weight:.1f} lb", f"{b.seat_weight:.1f} lb"),
        ("Rear-facing max", f"{a.rear_facing.max_weight} lb" if a.rear_facing else "No",
                            f"{b.rear_facing.max_weight} lb" if b.rear_facing else "No"),
        ("Forward-facing max", f"{a.forward_facing.max_weight} lb" if a.forward_facing else "No",
                               f"{b.forward_facing.max_weight} lb" if b.forward_facing else "No"),
        ("Booster max", f"{a.booster.max_weight} lb" if a.booster else "No",
                        f"{b.booster.max_weight} lb" if b.booster else "No"),
        ("Rotates", "Yes" if a.rotating else "No", "Yes" if b.rotating else "No"),
        ("Anti-rebound", "Yes" if a.anti_rebound else "No", "Yes" if b.anti_rebound else "No"),
        ("Machine washable", "Yes" if a.machine_washable else "No",
                             "Yes" if b.machine_washable else "No"),
        ("Aircraft approved", "Yes" if a.aircraft_approved else "No",
                              "Yes" if b.aircraft_approved else "No"),
    ]
    for field, av, bv in rows:
        print(f"{field:30} | {av:20} | {bv:20}")
    print("=" * 76)


def open_safety_resources():
    choice = ask_choice(
        "\nOpen an official safety resource:",
        {
            "1": "NHTSA Car Seats & Booster Seats",
            "2": "NHTSA Recalls",
            "3": "NHTSA Car Seat Inspection / CPST help",
            "4": "Cancel",
        },
    )

    url = {
        "1": NHTSA_CAR_SEATS_URL,
        "2": NHTSA_RECALLS_URL,
        "3": NHTSA_INSPECTION_URL,
    }.get(choice)

    if url:
        print("Opening:", url)
        webbrowser.open(url)


def main():
    print("""
============================================================
                 CAR SEAT FINDER / RANKER
============================================================
Research-informed shopping tool. Always verify current
manufacturer specifications, recalls, and real-world vehicle fit.
""")

    while True:
        choice = ask_choice(
            "\nWhat would you like to do?",
            {
                "1": "Find the best match for a child",
                "2": "Search starter catalog by brand/model",
                "3": "Compare two seats",
                "4": "Explain scoring methodology",
                "5": "Open official NHTSA safety/recall resources",
                "6": "Exit",
            },
        )

        if choice == "1":
            find_best_seat()
        elif choice == "2":
            search_catalog()
        elif choice == "3":
            compare_two()
        elif choice == "4":
            print_methodology()
        elif choice == "5":
            open_safety_resources()
        elif choice == "6":
            print("Goodbye.")
            break


if __name__ == "__main__":
    main()
