# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Your community, and what your classifier sorts posts into. Three or four
     sentences. -->

TakeMeter sorts comments from r/LocalLLaMA, the subreddit where people run
language models on their own hardware, into four kinds: `hands_on` (the writer
ran something and reports a concrete result), `factual` (the point rests on a
checkable outside fact), `opinion` (a claim or reaction with nothing behind
it) and `question`. When I read that sub, the posts worth my time are the ones
with a real result or a real fact in them, and they're buried under a lot of
confident takes. The model is DistilBERT fine-tuned on 248 posts I collected
and labelled, and it trains on my laptop's CPU in a few minutes.



---

## Label Taxonomy

<!-- Each label: a one-sentence definition and two real examples from your
     reading. Then your decision rule for the hardest boundary.

     The decision rule is worth a point on its own and it's the thing most
     people leave out. Every taxonomy has a hardest boundary. Name yours. -->

Four labels. I started from what I actually saw while reading (see
[reading_notes.md](reading_notes.md)), not from the example taxonomy. The
example posts below come from that first reading sample (four days in March,
May, July and September 2026), which I pulled before building the labelling
pool, so they aren't rows in `labels.csv`.

### `hands_on`

**Definition:** The writer reports something they ran, tested, or built
themselves, and gives a concrete result someone else could check (a speed, a
memory number, an error, a specific thing the model did or failed to do).

**Example 1:**
> Hmm, i tried with gpt oss, I asked it to output the full reasoning of
> earlier turns exactly, eord for word, and it was able to do that

**Example 2:**
> Flash Next is now gated from tensor because it was causing a test to fail.
> Not sure if that helps. Prior to that I had it running and it was odd how
> it loaded making it too inefficient for my cards to get reasonable context
> size. I forget what it was doing precisely, but every other card had a copy
> of the same thing piled on top of the rest of the assigned weights. Someone
> smarter than me might know what that was.

### `factual`

**Definition:** The writer backs a point with a checkable fact from outside
their own setup (a spec, version, release date, price, published benchmark,
documentation, or a quoted source), and the fact is what the point rests on.

**Example 1:**
> GLM-5 training began in December 2025. The researchers can't pull data from
> the future.

**Example 2:**
> I think you got the colors mixed up (understandably) - the 9B is almost as
> good as the 35B-A3B, not the 122.

### `opinion`

**Definition:** A claim, prediction, judgment, or reaction with no support
offered. Strength of feeling is not support, and neither is "I've used a lot
of models".

(I added "reaction" after the cold pass. Posts like "LOL i didnt know that and
been using opencode for months" aren't claims, but they aren't anything else
either, and I'd rather have one clear home for them than argue each one.)

**Example 1:**
> OpenAI should be held legally accountable. I know they won't be, but they
> should be

**Example 2:**
> this is just a pedantic nerd argument. u both believe the same thing,
> because spoiler alert, it's COMMON SENSE

### `question`

**Definition:** The main purpose of the post is to get an answer, advice, or
help from other people.

**Example 1:**
> How do you define distillation? I always assumed parent/teacher training
> where the student was trained off the logits of the parent. It seems most
> just mean fine tuning off some output.

**Example 2:**
> this model looks like it's a little to small for a macbook air m4 24gb of
> ram, right? but the 27 and 30B version seems too heavy

### The hardest boundary

**Which two labels:** `hands_on` vs `opinion`.

The post that made me write this rule:

> Both 27B and 35B v3.5 models seem to be more focused than the v3.6 models.
> I've spent countless hours (hobby) tinkering with params, different quants
> and quant providers and I've just settled on the conclusion that 3.5 is just
> generally better for me. Hell, I've found that v3.5 9B is a beast for most
> text processing and general chat.

It names real models and says the writer spent hours on them, so it feels like
`hands_on`. But the only results it gives are "more focused", "better" and "a
beast", which are verdicts, not results.

**The decision rule I used every time:**

Naming the model, the quant, or the hardware is not enough. If the post gives a
concrete result from the writer's own run (a number, an error, a specific thing
the model did or didn't do), it's `hands_on`, even if it ends with a strong
verdict. If the only "result" is a verdict like better, smarter, faster, more
focused, or a beast, it's `opinion`, no matter how many hours of tinkering it
mentions. So the post above is `opinion`.

**Three smaller rules for the other boundaries:**

- **`question` vs anything:** if the post asks something and the writer
  actually wants the answer, it's `question`, even if it opens with a
  paragraph about their setup. That paragraph is context for the question.
  Rhetorical questions ("who even uses Ollama anymore?") don't count.
- **`hands_on` vs `factual`:** where does the support come from? The writer's
  own run means `hands_on`. A spec sheet, a release note, a published number
  or someone else's benchmark means `factual`. If a post has both, I go with
  whichever one the conclusion rests on.
- **`factual` vs `opinion`:** the fact has to carry the point. If a number is
  decoration on a conclusion the writer already had, it's `opinion` with a
  number in it. A technical explanation counts as `factual` when the point
  rests on specific mechanics you could check in docs ("hot experts go in
  VRAM, cold ones on the SSD, so random read speed is the bottleneck"). A
  bare assertion like "lower quants run faster but with lower quality" is
  `opinion`, even if it's true, because nothing in the post supports it. I
  added this one after the cold pass too, since explanations turned out to be
  a big chunk of this sub.



---

## The Dataset

<!-- Where you collected from, how you labelled, your counts, and three hard
     cases. -->

**Where the posts came from:** Public r/LocalLLaMA comments from January to
September 2026. Reddit blocks its own JSON pages without a login now, so
[collect.py](collect.py) reads the Arctic Shift archive, a public mirror of
Reddit data. It samples 24 short windows spread across those nine months, so
no single model launch takes over the data. Then it throws out what I couldn't
label fairly: bots, referral spam, posts with links, quoted replies, code
blocks, non-English text, posts under 12 words, and posts the model couldn't
read whole (over 100 words or over 128 tokens). That left 1,242 posts in
[data/raw_pool.csv](data/raw_pool.csv), with the comment id and permalink for
each one so any row can be traced back. No usernames are stored.
`python -m unittest test_collect` runs the 22 tests on those filters.

**How I labelled them:**

1. **Cold pass, 20 posts.** I labelled the first one myself. Then I stopped,
   because I was worried my own takes on which models are good would leak
   into my labels, and asked Claude to label the other 19 in a single pass
   with only my definitions, no tools and no second opinion. The note column
   says which is which (`cold` for mine, `cold, labelled by Claude...` for the
   rest). That pass is also where I found two gaps and changed my definitions
   (see the notes under `opinion` and the `factual` vs `opinion` rule).
2. **AI pre-labelling, 700 posts.** Two separate Claude (Sonnet) sessions
   labelled the same 700 random posts from the pool, each with my definitions
   and decision rules and without seeing the other's answers. They agreed on
   656 of 700 (93.7%).
3. **The 44 splits** were decided one by one against my rules. Most of them
   were rule 2 (is a verdict a result?) or rule 4 (is this a mechanism or a
   bare assertion?).
4. **Agreed rows were read too.** Two passes agreeing doesn't make them right.
   Reading the agreed rows in my final set turned up 12 where both passes broke
   a rule, mostly calling a post `hands_on` when it named a setup but gave no
   result. Those 12 were changed, and the note column says what each one was
   before. Two rows got dropped: one started with an escaped Reddit quote my
   filter missed (fixed in `collect.py`, with a test), and one was French.
5. **Picking 248 from the labelled pool.** About 61% of real r/LocalLLaMA
   comments are `opinion` (both passes' raw labels are in
   [data/prelabel_passes.csv](data/prelabel_passes.csv)), so I kept every hard row and filled each label from
   the agreed rows up to a target, with `opinion` deliberately the biggest.
   The tradeoff: this file is more balanced than the sub itself, so on raw
   threads the model will probably call too few posts `opinion`.

**Counts per label:**

| Label | Count | Share |
|---|---|---|
| `opinion` | 88 | 35.5% |
| `factual` | 57 | 23.0% |
| `question` | 53 | 21.4% |
| `hands_on` | 50 | 20.2% |
| **Total** | 248 | 100% |

**Three hard cases**

<!-- Any post that made you pause: what it was, which two labels it could have
     been, and what you chose. These are worth more than the easy 190. -->

**1.**
> *The post:* "21Gbps/8(gigabyte)=2.625GB/s for RTX 4090. Qwen3.6 27B
> IQ4_NL = 16.1GB (Isn't an Active Weight model). So... 16.1/2.625=6.1
> Tokens/s. 6.1*8= 48.8Tokens/s. Oh wow it's right I get around 50t/s with
> that model. It's a joke."
>
> *Could have been:* `factual` or `hands_on`. It has a spec-sheet calculation
> and a number from the writer's own machine.
>
> *I chose, because:* `factual`. My rule for this boundary is "whichever the
> conclusion rests on". Almost the whole post is the bandwidth math, and the
> 50 t/s from their own run only confirms it. If they had led with "I get 50
> t/s" and then explained it, I'd have gone the other way.

**2.**
> *The post:* "The old functionality in the chat UI only transcribed text, if
> you gave it an image of something other than a document it wouldn't be able
> to describe it. From the other user's post above it looks like it's
> changed?"
>
> *Could have been:* `question`, `hands_on` (it describes how the tool
> behaved for them) or `opinion`. This one could go three ways.
>
> *I chose, because:* `question`. Rule 1 comes first: the writer actually
> wants to know whether it changed. The first sentence is the context for the
> question, not a result being reported.

**3.**
> *The post:* "This is the top open weight model. Still weak on code reviews
> (same for other Chinese models). Lots of false positives and over
> exaggeration on severity. It’s like all these models were optimized for
> beating benchmarks."
>
> *Could have been:* `hands_on` or `opinion`. That's my hardest boundary.
> "False positives and over exaggeration on severity" sounds like something
> they saw.
>
> *I chose, because:* `opinion`. The post never says the writer ran anything,
> and there's no specific result, just a general description of how the model
> behaves. The two AI passes split on this one too.

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Base model:** `distilbert-base-uncased`

**Settings:** 3 epochs, learning rate 2e-5, batch size 16, 128 tokens per
post, seed 42.

**Where it ran:** CPU (`device: cpu`, torch `2.14.1+cpu`, Windows 11 laptop).
`results.json` records the same thing.

**Anything I changed from the defaults, and why:** Nothing for the main run.
`results.json` and `test_split.csv` come from the notebook exactly as given,
with only `LABELS` set to my four. The second run below is a stretch, kept in
its own file.

**Split sizes:** 172 train / 38 val / 38 test.

| Label | Train | Val | Test |
|---|---|---|---|
| `hands_on` | 34 | 8 | 8 |
| `factual` | 39 | 9 | 9 |
| `opinion` | 62 | 13 | 13 |
| `question` | 37 | 8 | 8 |

No label is under 8 in test, but `hands_on` and `question` sit right at 8.
For those two, one post is worth about 0.06 of F1, so I expect them to move
the most between seeds next unit.

### Stretch features

What I'm adding, and what I'm skipping:

- **A fourth label (done).** `question` came straight out of the reading.
  About one post in seven in the pool is a question, and forcing those into
  `opinion` would have made `opinion` meaningless.
- **A second run with one hyperparameter changed (done).** Epochs 3 → 10,
  same seed, same split. [run2_epochs.py](run2_epochs.py) runs the notebook in
  memory with that one change, checks the test split didn't move, and writes
  [results_run2_epochs10.json](results_run2_epochs10.json).
- **50 extra examples for the thinnest label (skipped).** My thinnest label
  has 50 rows, and the pool already has more of each label. Adding them would
  mean another labelling round for a label that isn't my real problem yet.
  The run below says the problem is training steps, not data.

**What moved in the second run:**

| | 3 epochs | 10 epochs |
|---|---|---|
| Accuracy | 0.368 | 0.526 |
| Macro F1 | 0.181 | 0.485 |
| F1 `hands_on` | 0.182 | 0.400 |
| F1 `factual` | 0.000 | 0.167 |
| F1 `opinion` | 0.542 | 0.667 |
| F1 `question` | 0.000 | 0.706 |

With 3 epochs the model called 35 of the 38 test posts `opinion`. It never
left the "guess the biggest label" stage. 172 posts at batch 16 is 11 steps
an epoch, so 3 epochs is only 33 steps. With 10 epochs `question` went from
0.00 to 0.71, which is what I expected from a label with such obvious surface
cues. Validation loss was still dropping at epoch 10 (1.357 → 0.970), so it
wasn't overfitting yet. The new weak spot surprised me: 5 of the 9 `factual`
posts got called `hands_on`. Both are full of numbers and model names, and the
model hasn't learned that what matters is where the number came from. I'm
keeping the notebook on its defaults for now. Changing the epochs is a better
fit for next unit's improvement step, where I can do it on purpose.



---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

**Moment 1**

- *What I asked for:* I gave Claude my four definitions and asked for eight
  r/LocalLLaMA-style posts sitting right on the boundaries, without saying
  which label was right.
- *What came back:* Two of them broke my `hands_on` definition as I'd first
  written it: "Ran Qwen3 32B Q4 on my 3090 for a week of coding tasks.
  Honestly it's just the best local coder right now" and "I tried a bunch of
  quants and settled on Q5_K_M. It just feels smarter to me." Both name a real
  setup, so my first definition (report something you ran and what happened)
  let them in. But "best" and "feels smarter" aren't results.
- *What I changed:* I rewrote `hands_on` to require a concrete result someone
  could check, and wrote my hardest-boundary rule around that: naming the
  hardware isn't enough. The same check decided my borderline post. I also
  asked for the strongest case for `hands_on` and for `opinion` on it, and the
  `opinion` case ("the tinkering is mentioned only as credentials") was the
  stronger one under the rewritten definition.

**Moment 2**

- *What I asked for:* For my five criteria, one reason each target might be
  too easy and one it might be too hard, and whether a stranger could check
  each one from `results.json` alone.
- *What came back:* The numbers were fine, but criterion 5 wasn't checkable.
  I wrote "measured from the confusion counts" without saying which way the
  matrix runs or what the denominator is. It also pointed out that criterion
  4's thirds move in steps of about 0.083 with 12 posts each, so 0.15 really
  means "at least two more right".
- *What I changed:* I kept every number. I rewrote criterion 5 with the exact
  formula (`confusion["hands_on"]["opinion"] / sum(confusion["hands_on"].values())`),
  pinned criterion 4 to the notebook's own thirds, and said at the top which
  file holds the per-seed numbers.

**Pre-labelling disclosure:** 228 of my 248 rows were pre-labelled by AI
(two independent Claude Sonnet sessions over the same 700 posts). The 44
posts where the two disagreed were decided against my written rules, and the
agreed rows in the final set were read, with 12 corrected. All of that review
was done with Claude as my coding assistant, working from my definitions and
decision rules. 19 of the 20 cold rows were also labelled by Claude, at my
request. Every row's note says how it was labelled.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy |  |  |  |
| Macro F1 |  |  |  |
| F1 — `label_one` |  |  |  |
| F1 — `label_two` |  |  |  |

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted |  |  |  |
|---|---|---|---|
| **** |  |  |  |
| **** |  |  |  |
| **** |  |  |  |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** ___ / 30 = ___%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
