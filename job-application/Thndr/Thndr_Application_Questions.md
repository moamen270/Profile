# Thndr — application form questions

## Q: Why Thndr? Share why you want to work at Thndr.

### Answer (use this)

I've been building a paper-trading and backtesting framework for the EGX in my own
time. Getting the cost model right meant working through commission, exchange, FRA
and MCDR fees, stamp duty and the Sun–Thu 10:00–14:30 session — and one of the first
things I ran into was that there is essentially no retail order API for the Egyptian
market. That is the gap Thndr closed for four million people, and it's why 82% of
newly registered EGX investors in 2024 came through an app rather than a broker's
office.

Money Movements is the part of that I actually want to work on. Deposits,
withdrawals, settlement and reconciliation are the class of problem where "mostly
works" is a failure. That's what I've spent the last two years on — I replaced an
MS DTC distributed-transaction design with Temporal Saga orchestration, compensating
steps and all, because the old design couldn't survive partial failure without
forcing every service onto one shared database. Doing that where the money is real,
across Egypt and the UAE, is a better version of the same problem.

_(~190 words)_

### Short version — if the field caps around 500–700 characters

I've been building an EGX paper-trading and backtesting framework in my own time,
and modelling the costs — commission, exchange, FRA and MCDR fees, stamp duty —
made it obvious how little retail access to the Egyptian market exists. Thndr closed
that gap for four million people. Money Movements is the part I want to work on:
deposits, withdrawals, settlement and reconciliation are where "mostly works" is a
failure, and that's the problem I've spent two years on — replacing an MS DTC design
with Temporal Saga orchestration so it could survive partial failure.

_(~600 characters)_

---
---

## NOT PART OF THE ANSWER — notes

### Facts used, and where they came from

| Claim | Source | Safe to assert? |
|---|---|---|
| "more than 4,000,000 Thndr users today" | thndr.app homepage | Yes — their own number |
| 82% of newly registered EGX investors in 2024 came via Thndr; 190.1K new investors added | Thndr 2024 press / funding coverage | Yes — their own published figure |
| Expanding into UAE and Saudi; $15.7M round led by Prosus Ventures (May 2025), $37.76M total | Wamda, Disrupt Africa, Fintech News UAE | Yes, but **not used** — funding talk reads as flattery |
| Mission: "democratise investing and improve financial literacy across MENA" | Thndr | Yes — **deliberately not quoted.** Quoting a company's mission statement back at them is the most common and most obviously generic move in a "why us" answer |
| Egypt's #1 investing app for stocks, gold and funds | thndr.app | Yes |

### Why this answer is built the way it is

Nearly every answer they receive will paraphrase the mission statement. This one
leads with a thing you actually did that almost no other applicant will have done,
and that happens to prove the interest rather than assert it. The EGX cost model is
the detail that makes it credible — commission, FRA and MCDR fees and stamp duty are
not things you know unless you have sat down with the mechanics of the Egyptian
market.

Then it pivots to the squad, because "why Thndr" and "why this squad" are the same
question when the squad is named in the job title.

### Before you send this — two things

1. **The EGX framework is at `F:\PoCs\egx-trading-bot` and is not a git repo yet.**
   If you name it in an application, be ready for "can you show it?" Push it to
   GitHub first, even private, so you can share a link on request. 20 passing tests
   and a real cost model is a perfectly respectable thing to show.
2. **Be honest about timeline if asked.** It's a recent project. The answer above
   doesn't claim otherwise — it says "have been building", not "have been building
   for years." Don't upgrade that in conversation.

### If they ask about it in interview

You found there's no verified retail order API for the EGX, so the framework ships a
self-contained simulated paper broker with SQLite state, plus an optional,
off-by-default adapter for an unverified sandbox that is hard-blocked from live
trading. Backtest and live paths share one engine and one cost model — which is the
same "don't let the test path and the real path diverge" instinct that matters in
money movement.
