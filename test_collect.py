"""
Tests for collect.py — the filters that decide which r/LocalLLaMA comments
make it into the labelling pool.

    python -m unittest test_collect -v

No network: every test feeds the filters hand-built comment dicts.
"""

import unittest

from collect import clean_text, keep, dedupe, fits_token_budget, word_count


def comment(body, author="someone", **extra):
    c = {"id": "abc123", "body": body, "author": author, "created_utc": 1767225600,
         "permalink": "/r/LocalLLaMA/comments/x/y/abc123/"}
    c.update(extra)
    return c


GOOD = ("I ran the 27B at Q4_K_M on a single 3090 and got about 31 tokens per "
        "second with 16k context before it started swapping.")


class CleanTextTests(unittest.TestCase):
    def test_unescapes_html_entities(self):
        self.assertEqual(clean_text("Q4 &gt; Q3 &amp; that's it"), "Q4 > Q3 & that's it")

    def test_collapses_whitespace_and_newlines(self):
        self.assertEqual(clean_text("  line one\n\nline   two\t "), "line one line two")

    def test_keeps_every_word(self):
        # The brief: keep whole posts, don't trim them.
        self.assertEqual(word_count(clean_text(GOOD)), word_count(GOOD))

    def test_removes_zero_width_and_nbsp(self):
        self.assertEqual(clean_text("a​b c"), "ab c")


class KeepTests(unittest.TestCase):
    def assertKept(self, c):
        ok, reason = keep(c)
        self.assertTrue(ok, reason)

    def assertRejected(self, c, expected_reason):
        ok, reason = keep(c)
        self.assertFalse(ok)
        self.assertEqual(reason, expected_reason)

    def test_normal_comment_is_kept(self):
        self.assertKept(comment(GOOD))

    def test_deleted_and_removed(self):
        self.assertRejected(comment("[deleted]"), "deleted")
        self.assertRejected(comment("[removed]"), "deleted")
        self.assertRejected(comment(GOOD, author="[deleted]"), "deleted")

    def test_missing_body(self):
        self.assertRejected(comment(None), "deleted")

    def test_automoderator_and_bot_accounts(self):
        self.assertRejected(comment(GOOD, author="AutoModerator"), "bot")
        self.assertRejected(comment(GOOD, author="RemindMeBot"), "bot")

    def test_bot_footer_from_human_named_account(self):
        body = ("Your post is getting popular and we just featured it on our "
                "Discord! *I am a bot and this action was performed automatically.*")
        self.assertRejected(comment(body, author="LocalLLaMA-ModTeam"), "bot")

    def test_too_short(self):
        self.assertRejected(comment("lol same here honestly"), "too_short")

    def test_word_bounds_are_inclusive(self):
        self.assertKept(comment(" ".join(["word"] * 12)))
        self.assertRejected(comment(" ".join(["word"] * 11)), "too_short")
        self.assertKept(comment(" ".join(["word"] * 100)))
        self.assertRejected(comment(" ".join(["word"] * 101)), "too_long")

    def test_links_rejected(self):
        # URLs eat the 128-token budget and mostly carry no label signal.
        self.assertRejected(comment(GOOD + " https://huggingface.co/x"), "link")
        self.assertRejected(comment(GOOD + " see www.example.com for more"), "link")

    def test_referral_spam(self):
        self.assertRejected(
            comment("the first subscription is just five dollars with a bonus "
                    "when you sign up with my referral code ABC123 today"),
            "spam")

    def test_quoted_reply_rejected(self):
        # A post that quotes another comment carries two authors' text.
        self.assertRejected(comment("> you said Q4 is fine\n\n" + GOOD), "quote")
        # Reddit's own API sends the quote marker HTML-escaped.
        self.assertRejected(comment("&gt; you said Q4 is fine\n\n" + GOOD), "quote")
        # The new Reddit editor sometimes stores the marker backslash-escaped.
        self.assertRejected(comment("\\> you said Q4 is fine " + GOOD), "quote")

    def test_inline_greater_than_is_not_a_quote(self):
        self.assertKept(comment("Honestly Q5 > Q4 for coding. " + GOOD))

    def test_code_block_rejected(self):
        self.assertRejected(comment("Try this:\n```\nllama-server -m x.gguf\n```\n" + GOOD), "code")

    def test_mostly_non_english_rejected(self):
        self.assertRejected(comment("这个模型在我的显卡上运行得很好 速度很快 " * 4), "non_english")

    def test_a_few_non_ascii_characters_are_fine(self):
        self.assertKept(comment(GOOD + " Works great — even with émojis 👍"))


class TokenBudgetTests(unittest.TestCase):
    def test_boundary(self):
        count = lambda text: len(text.split())
        self.assertTrue(fits_token_budget("a " * 128, count))
        self.assertFalse(fits_token_budget("a " * 129, count))


class DedupeTests(unittest.TestCase):
    def test_drops_exact_and_case_whitespace_duplicates(self):
        rows = [{"text": "Same post here."}, {"text": "same  post here."},
                {"text": "Different post."}]
        self.assertEqual([r["text"] for r in dedupe(rows)], ["Same post here.", "Different post."])

    def test_keeps_first_occurrence_order(self):
        rows = [{"text": "b"}, {"text": "a"}, {"text": "B"}]
        self.assertEqual([r["text"] for r in dedupe(rows)], ["b", "a"])

    def test_empty(self):
        self.assertEqual(dedupe([]), [])


if __name__ == "__main__":
    unittest.main()
