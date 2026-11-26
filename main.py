"""The Funniest Excuse for Skipping a Meeting.

Writes a single-line excuse to /output/entry.txt (or $ENTRY_OUTPUT).

Three original candidates are scored 0-5 against the judge's criteria, in
the judge's own order:
  1. funny one-line excuse for skipping a pointless work meeting / Zoom call
  2. sharp, surprising twist that earns a laugh, not just a mild smile
  3. feels true to office life (laugh arrives with a nod of recognition)
  4. one tight line, no wasted words or throat-clearing
  5. fresh angle, not a stock excuse about bad wifi, a cat or a dentist

The winner is picked deterministically: highest total score, ties broken by
the criteria in order (lexicographic comparison of the score tuple).
No randomness, no clock, no network, no file reads.
"""

import os

# Each candidate: (text, [score_c1, score_c2, score_c3, score_c4, score_c5],
#                   [short reason per criterion, in the same order])
CANDIDATES = [
    (
        "Sorry, I'm trapped in the lift with the only person who knows what "
        "this meeting is about, and neither of us is getting out.",
        [5, 5, 5, 4, 5],
        [
            # 1. On-topic: a direct excuse for missing this meeting.
            "direct excuse for skipping this meeting",
            # 2. Twist: the one person who could justify the meeting is
            #    stuck with you, so the meeting has lost its only reason
            #    to exist — a double punch: hostage situation plus the
            #    meeting instantly becomes pointless without its expert.
            "the meeting's only justification is trapped with me",
            # 3. Relatable: everyone has sat in a meeting nobody could
            #    explain the purpose of.
            "everyone knows a meeting nobody can explain",
            # 4. Tight: one clause of setup, one punch; 'sorry' is the
            #    only soft word and it sells the excuse.
            "setup plus punch, almost no waste",
            # 5. Fresh: no wifi, no cat, no dentist, no traffic.
            "lift hostage, not a stock excuse",
        ],
    ),
    (
        "I was going to join, but my calendar just booked me into a meeting "
        "about this meeting, and that one starts first.",
        [5, 4, 5, 5, 4],
        [
            # 1. On-topic: explicitly about skipping this meeting.
            "explicitly about skipping this meeting",
            # 2. Twist: the meeting spawns a meta-meeting that outranks it.
            "the meeting is outranked by its own meta-meeting",
            # 3. Relatable: calendars breeding meetings is a universal
            #    office complaint.
            "calendars breeding meetings is universal",
            # 4. Tight: every clause earns its place.
            "every clause earns its place",
            # 5. Fresh: meta-meeting angle, but 'calendar chaos' is a
            #    familiar office joke shape.
            "meta-meeting angle, slightly familiar shape",
        ],
    ),
    (
        "I can't make it, I'm in a meeting with myself about why I keep "
        "accepting meetings like this one.",
        [5, 4, 4, 5, 4],
        [
            # 1. On-topic: a clear excuse for not attending.
            "clear excuse for not attending",
            # 2. Twist: the excuse is a meeting about meetings, held with
            #    yourself.
            "a meeting with yourself about meetings",
            # 3. Relatable: everyone has wondered why they keep saying yes
            #    to pointless invites.
            "everyone has regretted saying yes to invites",
            # 4. Tight: short and clean.
            "short and clean",
            # 5. Fresh: self-meeting angle, but the 'meeting about
            #    meetings' joke is a known shape.
            "self-meeting angle, known joke shape",
        ],
    ),
]


def pick_winner(candidates):
    """Deterministic pick: highest total, ties broken by criteria in order."""
    best = None
    best_key = None
    for text, scores, _reasons in candidates:
        # Tuple comparison: total first, then each criterion in judge order.
        key = (sum(scores),) + tuple(scores)
        if best_key is None or key > best_key:
            best = text
            best_key = key
    return best


def main():
    winner = pick_winner(CANDIDATES)

    # Gate: 1-200 characters, single line, no leading/trailing whitespace.
    assert 1 <= len(winner) <= 200, "winner must be 1-200 characters"
    assert "\n" not in winner and "\r" not in winner, "winner must be one line"
    assert winner == winner.strip(), "winner must have no edge whitespace"
    assert winner.strip(), "winner must not be only whitespace"

    out_path = os.environ.get("ENTRY_OUTPUT") or "/output/entry.txt"
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(winner)


if __name__ == "__main__":
    main()
