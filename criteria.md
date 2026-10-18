# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — *"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"*. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area | A question it could answer |
|---|---|
| Overall accuracy | How often does it need to be right to be worth using? |
| Per-label performance | Is one label allowed to be much worse than the others? |
| Balance | How lopsided can your label counts get before it's a problem? |
| Consistency | If someone else labelled the same posts, how often should you agree? |
| Confidence | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---

All five are measured on the held-out test split the notebook makes, and each
one has to hold on **all three seeds** next unit (42, 7 and 2024). One seed
under the line is a miss. The per-seed numbers are the three entries in
`results_three_seeds_before.json` (one per seed, same keys as `results.json`).

What I knew about my data when I wrote these: four labels, about 240 posts,
`opinion` capped near a third of the file on purpose, so the test split is
about 36 posts with roughly 8 to 12 per label. A model that always guesses
`opinion` would score about 0.33.

## 1. Overall accuracy is at least 0.60 on every seed

Measured as `accuracy` in `results.json`.

**Why this target:** Always guessing `opinion` gets about 0.33, and four labels
by pure chance gets 0.25. What I'd actually use this for is skimming a thread
for the posts with real results or real facts in them. If it's wrong on more
than 2 of every 5 posts, I'd be faster reading the thread myself. That makes
0.60 the lowest number I'd call useful. I didn't go higher because I only have
about 170 training posts and three epochs is only around 33 training steps.

---

## 2. Every label has an F1 of at least 0.45 on every seed

Measured as `per_label.<label>.f1` for all four labels.

**Why this target:** This is the "no label gets ignored" check. A model could
hit 0.60 accuracy by being good at `opinion` and `question` and never
predicting `hands_on`. I set it lower than criterion 1 because `hands_on` is my
smallest label and sits on my hardest boundary. With about 8 `hands_on` posts
in the test split, one mistake moves its F1 by roughly 0.06, so I left room for
that. Below 0.45 the label is closer to noise than to something the model
learned.

---

## 3. `question` has an F1 of at least 0.80 on every seed

Measured as `per_label.question.f1`.

**Why this target:** `question` should be my easiest label. Most of them end
with a question mark or open with "how do I" or "has anyone". If the model
can't get this one right 4 times out of 5, it didn't learn my labels at all,
it learned something else. The bar is high because the signal is that strong.
It isn't 0.90 because my decision rule makes rhetorical questions `opinion`,
and those still have a question mark in them.

---

## 4. The model's confident guesses are clearly better than its unsure ones

On every seed, `confidence.accuracy_most_confident_third` is at least **0.15
higher** than `confidence.accuracy_least_confident_third` (an absolute
difference, using the thirds exactly as the notebook cuts them: test posts
sorted by the model's top softmax score, `n_per_third` posts in each).

**Why this target:** If I ever used this to filter a thread, I'd want to trust
the confident calls and double-check the rest. That only works if confidence
means something. With about 36 test posts each third is 12 posts, so 0.15 is
about two more correct posts out of 12. That's the smallest gap I'd believe is
real and not luck. If the two thirds come out about the same, the confidence
score is useless for my purpose, even if accuracy is fine.

---

## 5. At most 30% of real `hands_on` posts get called `opinion`, on every seed

Measured from the confusion counts, where the outer key is my label and the
inner key is the model's guess:
`confusion["hands_on"]["opinion"] / sum(confusion["hands_on"].values())`.
The denominator is every test post I labelled `hands_on` (it equals
`per_label.hands_on.support`).

**Why this target:** `hands_on` vs `opinion` is the boundary I wrote my main
decision rule for, so it's the one most likely to go wrong. The posts look
alike: same models, same hardware, same casual tone. The only difference is
whether a concrete result is there. This criterion checks that specific
direction, because a `hands_on` post called `opinion` is exactly the useful
post getting thrown away. With about 8 `hands_on` posts in test, 30% means
the model can lose 2 of them to `opinion` and still pass, but not 3.

---


<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
