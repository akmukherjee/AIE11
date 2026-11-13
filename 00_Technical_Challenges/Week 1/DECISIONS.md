# Decisions

One row one decision. This week is the first one. By Week 5 this file will explain what decisions you made during this bootcamp.

## Retrieval, week 1

**What I changed**

> Rewrote the system prompt so the model either answers fully, answers partly and says what's missing, or says it doesn't know. Also told it not to guess beyond the context or go along with claims the guide doesn't make.

**Why**

> - Baseline was 3/10. Most failures (Q4, Q5, Q6, Q8) were the model making stuff up, not bad retrieval. The chunks were on topic, so a score threshold wouldn't have helped.
> - After: 6/10, nothing got worse. Q4, Q6 and Q8 now say what the guide covers and what it doesn't.
> - Being honest: Q4 passes partly because I now allow partial answers, and Q8 is borderline. Strictly it's more like 4/10.
> - Still failing: Q5 (the model still guesses, just more politely) and Q1, Q2, Q9, which are retrieval problems a prompt can't fix.

**What would change my mind**

> - If I keep seeing polite guesses like Q5, I'd drop the partial-answer option. Maybe a plain "I don't know" beats a confident "might".
> - If people find the longer answers less useful than a short no.
> - If retrieval misses turn out to be the bigger problem, I'd change k or chunking next instead of the prompt.
