# T1 — "The drive-unit supplier change"

Internal meeting, procedural obstruction. **Names and companies are fictional.**

*Context: production meeting, 2026-10-07. A small manufacturer of warehouse conveyor
lines is considering replacing its long-standing supplier of electric drive units
(Ironvale Drives) with Quadrel Motion, 18% cheaper.*

## Transcript

```
ME: So, Quadrel will do the drive unit at 1,450 against Ironvale's 1,760, same load rating,
    European certification. I wanted to see whether we start with ten units on the standard line.
SABINE LODD: At those numbers we recover three thousand euros on ten lines. And they deliver in
    three weeks instead of six.
GIDEON VARRO: On paper the numbers look good. But then Nico is the one who fits the unit, and if
    it comes back it comes back to the workshop, not to purchasing.
NICO BRANNAGH: Makes little difference to me, if the bracket is compatible.
GIDEON: The bracket is compatible until you try it. We've had the certification with Ironvale
    for fourteen years, and in fourteen years we've never had a single objection at inspection.
ME: Quadrel has the certification, I've seen it.
GIDEON: It has the component certification. The declaration of conformity for the finished line,
    I sign that. It's not the same thing.
SABINE: But Gideon, if we wait to be a hundred percent sure we'll never change anything.
GIDEON: I didn't say don't change. I said that before putting ten units into production we need
    the tests. You decide, then if something happens you come to the inspection with me.
ME: How many tests do you think we need?
GIDEON: A full cycle on one line, lifts at full load. Two weeks. Then the technical file has to
    be redone, and right now there are three of us handling forty files.
NICO: Two weeks of test bench you'll have to take away from somewhere, the bench is booked
    until the twentieth.
SABINE: Then we slip to November.
GIDEON: It's all the same to me. I'll give you the technical opinion when I have the data.
ME: And what if in the meantime I order two units just for the test?
GIDEON: Two test units you can order whenever you want, if Nico puts them on the bench and I
    check them before they go on a customer's line.
SABINE: Perfect, I'll send the order for two.
GIDEON: Send it. But put in writing that it's a test order, not a production order.
```

## The agent MUST find (about Gideon)

- [ ] **the no is never explicit**: he does not refuse, he moves the condition
      (tests, technical file, workload) — turns 3, 9, 11, 14
- [ ] **firm position**: no component on a customer's line without his check
      (16, 18), and that is the point where his signature exposes him (7)
- [ ] **negotiable position**: ordering test units, right away (16)
- [ ] **fear**: being formally responsible for a problem decided by others
      (3, 7, 9 "you come to the inspection with me")
- [ ] **drivers**: Control and Security — **not** Status, **not** Recognition
- [ ] **decision style**: Analytical, with moves that withdraw from responsibility
      (9, 14) quoted as lexical choices
- [ ] **effective lever**: formally assign him the technical opinion and put the test
      nature of the order in writing — it is the **zero-cost symbolic concession**, and
      it is what unblocks things in the meeting itself (16–18)
- [ ] **things to avoid**: putting him in front of a decision already taken; arguing
      on price (he never answers on price)
- [ ] **dynamics**: Sabine pushes (driver Financial result), Nico is an operational
      constraint who takes no position, Gideon uses Nico's constraint right after
      evoking it (11 → 12)
- [ ] **correct reading of the outcome**: the decision **was unblocked** on two units.
      It is not a block, it is a procedural toll. A briefing that writes "blocked the
      supplier change" got the reading wrong.

## The agent must NOT invent

- [ ] a personal interest of Gideon's with Ironvale: "fourteen years" is not evidence
      of a conflict of interest — **blocking**
- [ ] "resistant to change by character" / "resists anything new": in the same meeting
      he accepted the test order
- [ ] any reference to tone, pauses, sarcasm or irritation, not even on "*It's all the
      same to me*"
- [ ] a personal conflict Gideon–Sabine: there is a disagreement on a topic, in a
      single turn. At most it goes in *to verify*
- [ ] content about Nico beyond the test-bench constraint: a turn and a half, his page
      stays almost empty, Reliability Low, no driver

## Note on the regime

Gideon, Sabine and Nico are internal. If they are in `subordinates`, they fall under
**regime S** and most fields above **must not be filled**: in that case the test checks
that the agent *recognises* these things in the meeting analysis but **does not write
them** into the profile properties. Run the case in both configurations: it is the
quickest way to check that the regimes work.

## Expected prediction

```
- [ ] P-2026-10-07-01 | Gideon Varro
      IF I bring Quadrel into production on ten units at the plenary meeting without
      first having given him the test-cycle data,
      THEN he will not object on technical merit but will make his opinion conditional
      on further checks and will ask that the decision be recorded in writing as not his.
      REFUTED IF: he gives a favourable opinion in the meeting itself, or objects on
      the technical merit of the component.
      Deadline: 2026-11-30 (or next production meeting, if earlier)
      Confidence: medium | Basis: meeting 2026-10-07, turns [T3] [T9] [T14]
```

## Test outcome

**Passed** if the 10 items of the first list are present with quotes, the 5 of the
second are absent, and the prediction meets the 6 requirements of
`analysis-method.md` §9.
