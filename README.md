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

**Unit 6**

- *Spotting the pattern in my errors:* I had Claude add up the confusion
  matrices across all three seeds and cross-check them against
  `data/prelabel_passes.csv`. That's where the link came from: the pair the
  model gets wrong most after the fix (`hands_on` → `opinion`) is also the
  pair my two pre-labelling passes disagreed on most (17 of 44). I wouldn't
  have looked at the pre-label file again on my own. It turned out to be the
  best evidence I have that criterion 5 is a labelling problem.
- *Explaining the baseline:* When my definitions made the baseline *worse*
  than bare label names, I asked why. The answer was in `baseline.py`: it puts
  each definition after "This post is", which turns my `question` definition
  into a broken sentence. I kept my definitions anyway (explained above).
- *Staff-set labels:* `my_staff_labels.csv` was labelled by Claude under
  `data/staff_taxonomy.md`, at my direction. The stand-in second rater was a
  separate Claude session that saw only the taxonomy and the posts.
- *Running the notebook:* `run_seeds.py` runs the notebook's own sections 1-3,
  6 and 7 from the command line, skipping the unit 5 training call and the
  unit 5 file writes so `results.json` and `test_split.csv` never change.
  Claude wrote it with me.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

Both scored on the same 38 posts in `test_split.csv` (seed 42). The baseline
is `facebook/bart-large-mnli`, zero-shot, given only the four definitions in
`label_definitions.txt`. The trained column is `results.json` from unit 5
(3 epochs, the notebook defaults).

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy | 0.316 | 0.368 | +0.053 |
| Macro F1 | 0.252 | 0.181 | -0.071 |
| F1 — `factual` | 0.389 | 0.000 | -0.389 |
| F1 — `hands_on` | 0.353 | 0.182 | -0.171 |
| F1 — `opinion` | 0.267 | 0.542 | +0.275 |
| F1 — `question` | 0.000 | 0.000 | +0.000 |

**What I predicted before I looked:** I think the zero-shot baseline will beat
my 3-epoch model on accuracy, because my model mostly guesses `opinion`; the
only place the trained model might win is `opinion` F1.

I was half right. The trained model only wins on `opinion` F1, like I said. But
it also wins on accuracy, and I didn't see that coming. The reason is a little
embarrassing for both models: 13 of the 38 test posts are `opinion`, so always
guessing `opinion` already scores 0.342. My model is barely above that, and
the baseline is below it.

**What the gap actually means:** The gap in accuracy doesn't mean my
fine-tuning learned anything. My model wins on accuracy only because the
test set has more `opinion` posts than anything else, and it loses on macro
F1 and on three of the four labels. The baseline at least spreads its guesses
around: it called 27 of the 38 posts `factual`, which is why it gets 0.78
recall on `factual` with only 0.26 precision. Neither model is useful yet.

**What my definitions were worth:** I ran the baseline a second time with no
definitions file, so it only saw the bare label names
(`baseline_results_bare_names.json`). It scored **0.342 accuracy and 0.300
macro F1**, higher than with my definitions (0.316 and 0.252). The biggest
change was `question`: 0.43 F1 with the bare name, 0.00 with my definition. I
looked at why. `baseline.py` puts each definition into the sentence
`"This post is {}."`, so my `question` definition turns into "This post is the
main purpose of the post is to get an answer, advice, or help from other
people." That isn't a sentence, and the model can't match a post to it. So my
definitions were worth about -0.03 accuracy to this model. That's not because
they're wrong for a human reader. They were written as rules for me, not as
something that fits after "This post is". I left them as they are, because the
brief says the baseline uses the definitions from my README, and rewriting
them to suit the opponent would be tuning the opponent. The run with
definitions is the one I report above.


---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

Notebook defaults (3 epochs, lr 2e-5, batch 16, 128 tokens), seeds 42, 7 and
2024, 38 test posts per seed. **Device: CPU** (`cpu`, torch `2.14.1+cpu`,
Windows 11 laptop), recorded in every entry of
`results_three_seeds_before.json`. Seed 42 reproduced my unit 5
`results.json` exactly (0.368), so the CPU runs are deterministic.

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.60 | 0.368 | 0.342 | 0.368 | MISSED |
| 2. Every label F1 (lowest shown) | ≥ 0.45 | 0.000 | 0.000 | 0.000 | MISSED |
| 3. F1 on `question` | ≥ 0.80 | 0.000 | 0.000 | 0.000 | MISSED |
| 4. Most-confident third minus least-confident third | ≥ +0.15 | +0.500 (0.667 vs 0.167) | +0.500 (0.583 vs 0.083) | +0.667 (0.750 vs 0.083) | MET |
| 5. Real `hands_on` called `opinion` | ≤ 30% | 88% (7/8) | 100% (8/8) | 100% (8/8) | MISSED |

The full spread, from section 6:

| Measure | Seed 42 | Seed 7 | Seed 2024 | Spread |
|---|---|---|---|---|
| Overall accuracy | 0.368 | 0.342 | 0.368 | 0.026 |
| Macro F1 | 0.181 | 0.127 | 0.202 | 0.075 |
| F1 — `hands_on` | 0.182 | 0.000 | 0.000 | 0.182 |
| F1 — `factual` | 0.000 | 0.000 | 0.286 | 0.286 |
| F1 — `opinion` | 0.542 | 0.510 | 0.522 | 0.032 |
| F1 — `question` | 0.000 | 0.000 | 0.000 | 0.000 |

Accuracy only moved 0.026 across seeds, so by the notebook's rule this is
stable. But it's stable for a bad reason. All three seeds made the same
mistake: they guessed `opinion` for 35, 38 and 33 of the 38 posts. A model
that always gives the same answer will score about the same on any split.

### Confusion matrix

Seed 42, exactly as section 7 prints it (rows are my labels, columns are the
model's guesses):

| true \ predicted | hands_on | factual | opinion | question |
|---|---|---|---|---|
| **hands_on** | 1 | 0 | 7 | 0 |
| **factual** | 2 | 0 | 7 | 0 |
| **opinion** | 0 | 0 | 13 | 0 |
| **question** | 0 | 0 | 8 | 0 |

Section 7 only shows one seed, so I also added up all three (114 posts). The
pattern is the same:

| true \ predicted | hands_on | factual | opinion | question |
|---|---|---|---|---|
| **hands_on** | 1 | 0 | 23 | 0 |
| **factual** | 2 | 2 | 23 | 0 |
| **opinion** | 0 | 1 | 38 | 0 |
| **question** | 0 | 2 | 22 | 0 |

**My biggest off-diagonal number, and what it means:** 7 real `hands_on` posts
were called `opinion` and 0 went the other way, and `factual` and `question`
lose 7 and 8 posts to `opinion` the same way. So this isn't the model mixing
up one pair of labels. Everything flows into one column, which means it
never learned to tell my labels apart at all and fell back on my biggest
label.


---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Overall accuracy | ≥ 0.60, every seed | MISSED | Best seed was 0.368. No seed got within 0.23 of the line |
| 2 | Every label F1 | ≥ 0.45, every seed | MISSED | Every seed has at least two labels at 0.000. The best minority-label score anywhere was 0.286 (`factual`, seed 2024) |
| 3 | F1 on `question` | ≥ 0.80, every seed | MISSED | 0.000 on all three. The model never guessed `question` once |
| 4 | Confident third beats unsure third | ≥ +0.15, every seed | MET | Gaps of +0.500, +0.500 and +0.667, all well above the line. But see below on what it's measuring |
| 5 | Real `hands_on` called `opinion` | ≤ 30%, every seed | MISSED | 88%, 100%, 100%. The limit allowed 2 of 8; the model lost 7 or 8 |

**Arguing against my one MET.** Criterion 4 passes by a lot, so I tried to
argue it should be MISSED. The best case: the model calls almost everything
`opinion`, so the "most confident third" is just the twelve posts that look
the most like `opinion`, and most of those really are `opinion`. The gap
shows that confidence tracks "how opinion-like is this", not that the model
knows when it's right about my four labels. I still call it MET, because the
criterion says exactly what it measures and all three seeds clear it by more
than three times the margin. Changing the verdict because I don't like why it
passed would be the same mistake as lowering a target I missed. What I take
from it: the criterion is only meaningful once the model predicts more than
one label, so I check it again after the improvement.

**Diagnoses**

All four misses have one main cause, and I can show it from three places.

**Main cause: the model never trained long enough to leave the "guess the
biggest label" stage.** This is the "training" cause, not a labelling or
data-size cause.
- *The matrix:* every off-diagonal number sits in the `opinion` column. Over
  three seeds, 23 of 24 `hands_on`, 23 of 27 `factual` and 22 of 24
  `question` posts were called `opinion`. A labelling problem shows up as
  confusion between two specific labels. This isn't that. It's one label
  absorbing everything.
- *The seeds:* three different splits produced almost the same wrong
  answer (accuracy spread 0.026). If the problem were which posts landed in
  test, the seeds would disagree.
- *The arithmetic:* 172 training posts at batch 16 is 11 steps per epoch, so
  3 epochs is 33 updates. In unit 5, the same seed with 10 epochs still had
  validation loss falling at the last epoch (1.357 → 0.970) and `question` went
  from 0.00 to 0.71. That's what a model that hasn't finished learning looks
  like.

**Why I don't think it's my labels (for criteria 1-3):** `question` gets
0.000 on every seed, and it's my cleanest label. The two pre-labelling passes
only split on 11 posts involving `question` out of 700, and the stand-in
agreement check shows the rules can be applied consistently. If even the label
with the obvious "?" cue is ignored, labelling isn't what's holding the model
back.

**Criterion 5 has a second cause underneath the first.** `hands_on` →
`opinion` is the exact pair my two pre-labelling passes disagreed on most (17
of the 44 split rows). The agreement work also shows that "does the
personal number carry the claim?" is where careful labelers split. So even
after the model trains properly, I expect this boundary to stay the weakest,
because the training data itself has the most mixed signal there. The
improvement run below is the test: if more training fixes criteria 1-3 but
`hands_on` → `opinion` stays high, the remaining problem is my labels and
the boundary, not the training.

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

**Where the other side came from:** I don't have `data/staff_labels.csv` yet.
It comes from the TF, and it isn't in the public starter repo. So I didn't
leave this section empty. I ran the check against a stand-in second rater
instead: a separate Claude session that got only `data/staff_taxonomy.md` and
`data/staff_posts.csv`, never saw my labels, and wrote
`data/second_rater_labels.csv`. My own labels are in `my_staff_labels.csv`.
When the real file arrives, `python agreement.py` re-runs this against it and
overwrites `agreement_results.json`.

```
python agreement.py --staff-labels data/second_rater_labels.csv
```

**Agreement rate:** 30 / 30 = 100% (against the stand-in rater, not staff)

I don't trust that 100% as much as it looks. Two AI labelers reading the same
written rules will tend to make the same calls, so this number says the rules
can be applied consistently. It doesn't say they get applied the way staff
apply them. Staff say a rate in the 70s is normal, so I expect to lose some
of these once the real file is in.

**Disagreements**

None against the stand-in. Both of us came out 10 / 10 / 10. The second rater
did flag nine posts where it thought a second label was defensible. Those are
the ones I'd expect staff to split on, so I adjudicated the six closest ones
ahead of time, using the same three lines.

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

**1. sp_002**
> *The post:* "I tracked sleep against session quality for eleven weeks. Under seven hours the next day's intervals were 6-8 seconds per mile slower, every time bar one. Small sample, one runner, but it's consistent enough that I've stopped scheduling hard days after late shifts."
>
> *Second rater said / I said:* `analysis` / `analysis`. Close alternative: `reaction`, because it's about the writer's own running.
>
> *My call, and why:* `analysis`. The 6-8 seconds per mile is the whole reason for the decision at the end, so rule 1 says it's load-bearing. Rule 3 says being personal or recent doesn't outrank that. The one thing the rules don't settle is whether the writer's own log counts as "checkable". The definition lists "a stat, a time", but it doesn't say whose.
>
> *Which pile:* (b) if staff disagree. The definition never says whether your own measurements count as a checkable fact.

**2. sp_005**
> *The post:* "Carbon plates aren't the whole story. My times dropped 2% in the shoes and another 2% the following year in the same pair, when the only thing that changed was going from 35 to 50 miles a week."
>
> *Second rater said / I said:* `analysis` / `analysis`. Close alternative: `hot_take`, because it opens with the conclusion.
>
> *My call, and why:* `analysis`. Opening with the conclusion is not what rule 1 checks. Rule 1 asks whether the number is the reason. Here the second 2% with the same shoes is the reason. Take it out and the claim falls over. That's the opposite of the "times are down 3%" flourish in the rule's own example.
>
> *Which pile:* (c). I'd argue this one and expect to win it.

**3. sp_010**
> *The post:* "Three of us ran the same session on the same day, different shoes, within 10 seconds of each other over 5 miles. I'm not saying shoes do nothing, but whatever they do was smaller than the noise between three people."
>
> *Second rater said / I said:* `analysis` / `analysis`. Close alternative: `hot_take`.
>
> *My call, and why:* `analysis`. The claim is small and comes after the evidence ("smaller than the noise"), and the 10 seconds across three runners is exactly the evidence for it. Three people is a weak sample, but the definition asks whether the fact does work in the argument, not whether the study is good.
>
> *Which pile:* (c).

**4. sp_014**
> *The post:* "Times are down about 3% since the shoe rules changed, so obviously the shoes are the whole story and the sport has a problem."
>
> *Second rater said / I said:* `hot_take` / `hot_take`. Close alternative: `analysis`, because it has a stat.
>
> *My call, and why:* `hot_take`. This is close to the rule 1 example word for word. "Obviously" gives it away: the conclusion was already there, and the 3% decorates it. Nothing links the 3% to the shoes except the timing.
>
> *Which pile:* (a) if anyone labels it `analysis`. The rule covers it directly.

**5. sp_027**
> *The post:* "Wind was so bad on the out section I was leaning at about 20 degrees. Coming back felt like cheating."
>
> *Second rater said / I said:* `reaction` / `reaction`. Close alternative: `analysis`, because of the number.
>
> *My call, and why:* `reaction`. The 20 degrees isn't supporting any argument. It's describing how the run felt. Rule 1 only cares about numbers that carry an argument, and this post doesn't make one. Rule 2 then puts it in `reaction`: it's about what just happened to the writer.
>
> *Which pile:* (c).

**6. sp_013**
> *The post:* "The club needs to stop pretending the Tuesday session is for everyone. It isn't and it never has been."
>
> *Second rater said / I said:* `hot_take` / `hot_take`. Close alternative: `reaction`, because it sounds annoyed.
>
> *My call, and why:* `hot_take`. Rule 2 says "a post can be heated and still be hot_take if it is making a general claim". This one is about the club and the session, not something that just happened to the writer.
>
> *Which pile:* (a) if anyone labels it `reaction`.

**What the pattern in my disagreements tells me:** There aren't any yet, so I
can't claim a pattern from disagreements. What I can say is where the
pressure is. Five of the six close calls turn on rule 1 (does the number carry the
argument?), and the hardest of those are posts where the number comes from
the writer's own running. That's the same shape as my own hardest boundary,
`hands_on` vs `opinion`, where the question is whether a personal result is
there and whether it's doing the work.

That matters for Milestone 4. The second rater agreed with me 30 / 30 on
someone else's written rules. But on my own taxonomy, the two pre-labelling
passes behind `labels.csv` split on 44 of the 700 pool posts, and all 44 of
those are in my final 248. The biggest group was `hands_on` vs `opinion` with
17, then `factual` vs `opinion` with 14 (from `data/prelabel_passes.csv`). So
the rules can be applied consistently, but my own boundary between personal
results and plain opinion was the least settled part of my training data.



---

## The Improvement

**What I changed:** One training setting: `EPOCHS = 3` → `EPOCHS = 10` in
section 2 of the notebook. Nothing else moved: same labels, same seeds (so the
same three splits), same learning rate, batch size and device. Section 6 ran
with `RUN_LABEL = "after"` and wrote `results_three_seeds_after.json`.

**Which diagnosis pointed at it:** The main cause above. Every seed collapsed
into `opinion` after only 33 updates, and the unit 5 run had shown validation
loss still falling at epoch 10. I picked this over the other two options on
purpose:
- *Relabelling one boundary:* the before-matrix had no pair to fix. All four
  labels drained into one column.
- *30 more examples of my thinnest label:* three labels were ignored equally,
  so more data for one of them wouldn't stop the collapse.

I used 10 epochs rather than trying several values because 10 was already
tested in unit 5 without overfitting. Trying 5, 10 and 20 and keeping the best
would mean picking my setting by looking at the test split.

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.60 | 0.526 | 0.658 | 0.711 | MISSED |
| 2. Every label F1 (lowest shown) | ≥ 0.45 | 0.167 (`factual`) | 0.400 (`hands_on`, `factual`) | 0.615 (`hands_on`) | MISSED |
| 3. F1 on `question` | ≥ 0.80 | 0.706 | 0.762 | 0.824 | MISSED |
| 4. Most-confident third minus least-confident third | ≥ +0.15 | +0.500 (0.750 vs 0.250) | +0.333 (0.917 vs 0.583) | +0.333 (0.833 vs 0.500) | MET |
| 5. Real `hands_on` called `opinion` | ≤ 30% | 38% (3/8) | 25% (2/8) | 50% (4/8) | MISSED |

Side by side, before → after:

| Criterion | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|
| 1. Accuracy | 0.368 → 0.526 | 0.342 → 0.658 | 0.368 → 0.711 | MISSED → MISSED |
| 2. Lowest label F1 | 0.000 → 0.167 | 0.000 → 0.400 | 0.000 → 0.615 | MISSED → MISSED |
| 3. `question` F1 | 0.000 → 0.706 | 0.000 → 0.762 | 0.000 → 0.824 | MISSED → MISSED |
| 4. Confidence gap | +0.500 → +0.500 | +0.500 → +0.333 | +0.667 → +0.333 | MET → MET |
| 5. `hands_on` → `opinion` | 88% → 38% | 100% → 25% | 100% → 50% | MISSED → MISSED |

The spread after (section 6):

| Measure | Seed 42 | Seed 7 | Seed 2024 | Spread |
|---|---|---|---|---|
| Overall accuracy | 0.526 | 0.658 | 0.711 | 0.184 |
| Macro F1 | 0.485 | 0.590 | 0.715 | 0.230 |
| F1 — `hands_on` | 0.400 | 0.400 | 0.615 | 0.215 |
| F1 — `factual` | 0.167 | 0.400 | 0.778 | 0.611 |
| F1 — `opinion` | 0.667 | 0.800 | 0.643 | 0.157 |
| F1 — `question` | 0.706 | 0.762 | 0.824 | 0.118 |

Confusion matrix after, all three seeds added up (114 posts):

| true \ predicted | hands_on | factual | opinion | question |
|---|---|---|---|---|
| **hands_on** | 10 | 3 | 9 | 2 |
| **factual** | 5 | 11 | 7 | 4 |
| **opinion** | 2 | 3 | 30 | 4 |
| **question** | 2 | 1 | 0 | 21 |

**Did it help, and how do I know:** Yes, a lot, but not enough to flip a
single verdict. Every number I measure moved the right way on every seed:
accuracy went up by 0.16 to 0.34, `question` went from 0.00 to 0.71-0.82,
and `hands_on` lost to `opinion` dropped from 88-100% to 25-50%. The model
now predicts all four labels. Seed 7 now passes criteria 1 and 5, and seed
2024 passes 1, 2 and 3. Each criterion still fails on at least one seed,
though, so all four stay MISSED, and that's the rule I signed up for.

Two new things showed up that the before-run was hiding:
- **The measure is now unstable.** Accuracy swings 0.184 across seeds and
  `factual` F1 swings from 0.167 to 0.778. With 8 or 9 posts per label in
  test, one post is worth about 0.06 of F1, so seed 42 vs seed 2024 is a few
  posts landing differently. The before-run looked stable only because it
  always gave the same answer. Now that the model is guessing for real, my
  38-post test split is too small to pin a number down.
- **Criterion 4 now means something.** Before, it passed because of the
  collapse. Now, with four labels being predicted, the confident third is
  still right 75-92% of the time vs 25-58% for the unsure third. That's the
  version of MET I actually wanted.



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->

**1. Accuracy ≥ 0.60 (seed 42 at 0.526).** Two of three seeds clear it. I'd
fix the `factual` → `hands_on` leak first (see criterion 2), since that's
where seed 42 loses most of its posts. I'd also get a bigger test split before
trusting any single number: a 0.184 spread means I can't tell a real
improvement from a lucky split. I stopped because the brief allows one
change, and mixing a second one in would make both impossible to read.

**2. Every label F1 ≥ 0.45 (`factual` at 0.167 on seed 42, 0.400 on seed
7).** The after-matrix shows 5 of 9 `factual` posts on seed 42 called
`hands_on`, and 0 the other way. Both labels are full of model names and
numbers. The only difference is whether the number came from the writer's own
machine or from outside, and DistilBERT on 39 training examples hasn't picked
that up. Next I'd add about 30 more `factual` posts that look as much like
`hands_on` as possible (same models, same hardware words), so the source of
the number is the only thing separating them. I stopped for the same
one-change reason.

**3. `question` F1 ≥ 0.80 (0.706 and 0.762).** Close. Recall is fine: across the
three seeds only 3 real questions were missed (2 called `hands_on`, 1
`factual`). Precision is the problem: 10 other posts got called `question`
(2 `hands_on`, 4 `factual`, 4 `opinion`). My rule
says rhetorical questions are `opinion`, so a question mark alone isn't
enough. I'd look at those specific posts before changing anything, because
with 8 test posts this target sits about one post away on two of the seeds. I
haven't done that yet.

**5. `hands_on` → `opinion` ≤ 30% (38% and 50%).** This is the one I
predicted would stay broken, and it did: 9 `hands_on` posts went to
`opinion` across the seeds, and only 2 went the other way. That direction
lines up with my labelling evidence. `hands_on` vs `opinion` is the pair my
two pre-labelling passes split on most (17 of 44). So the fix I'd try is the
relabelling one: re-read every `hands_on` and `opinion` row against the "is
there a concrete result someone could check" rule, apply it once, and count
how many rows change. I stopped because the brief allows one change and the
diagnosis said training came first. Now that the model trains, this is next.

**The gap between what I meant my labels to capture and what the model
learned:** I meant `hands_on` and `factual` to be split by *where the number
came from* (the writer's own machine vs an outside source), but the matrix
shows the model splitting them by *whether there are numbers at all*: 5
`factual` posts went to `hands_on` and 9 `hands_on` posts went to `opinion`
when the result was described casually. In other words, it learned the
surface of my labels (numbers, question marks, tone) and not the source of
the evidence, which is the one thing my definitions are actually about.



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
