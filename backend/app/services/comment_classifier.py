import re


# Constraint di DB: hanya boleh
# unclassified, question, praise, spam, toxic, neutral

SPAM_PATTERNS = [
    r"\bslot\b", r"\bjudi\b", r"\btogel\b", r"\bcasino\b",
    r"\bgacor\b", r"\bjackpot\b", r"\bmaxwin\b",
    r"\bpromo\b.*\bklik\b", r"\bklik link\b", r"\bcek bio\b",
    r"\bobat kuat\b", r"\bjamu\b", r"\bviagra\b",
    r"\bfree money\b", r"\beasy money\b",
    r"\binvestasi\b.*\bprofit\b.*\bpersen\b",
]

TOXIC_PATTERNS = [
    r"\bbodoh\b", r"\bgoblok\b", r"\bidiot\b", r"\bstupid\b",
    r"\bbego\b", r"\bbangsat\b", r"\bkampret\b",
    r"\bbajingan\b", r"\bkontol\b", r"\bmemek\b",
    r"\bfuck\b", r"\bshit\b", r"\bbitch\b",
]

LEAD_PATTERNS = [
    r"\bberapa\b", r"\bharga\b", r"\bpricelist\b", r"\bprice list\b",
    r"\bbiaya\b", r"\bfee\b", r"\bminat\b", r"\btertarik\b",
    r"\bpesan\b", r"\border\b", r"\bbeli\b", r"\bbuatkan\b",
    r"\bbikinin\b", r"\bkerjasama\b", r"\bkerja sama\b",
    r"\bwa\b", r"\bwhatsapp\b", r"\bkontak\b", r"\bcontact\b",
    r"\bdeal\b", r"\bnego\b", r"\bnegoisasi\b",
]

QUESTION_PATTERNS = [
    r"\bapa\b", r"\bapakah\b", r"\bkenapa\b", r"\bmengapa\b",
    r"\bgimana\b", r"\bbagaimana\b", r"\bkok\b", r"\bkapan\b",
    r"\bdimana\b", r"\bsiapa\b",
    r"\bboleh tanya\b", r"\bboleh minta\b", r"\bmau nanya\b",
    r"\bshare dong\b", r"\bjelasin\b", r"\bjelaskan\b",
]

PRAISE_PATTERNS = [
    r"\bkeren\b", r"\bmantap\b", r"\bbagus\b", r"\brelate\b",
    r"\bsetuju\b", r"\bsuka\b", r"\bhebat\b", r"\bluar biasa\b",
    r"\bterbaik\b", r"\bjoss\b", r"\bgokil\b",
    r"\bsip\b", r"\bnice\b", r"\bgreat\b", r"\bawesome\b",
    r"\blove\b", r"\bmakasih\b", r"\bterima kasih\b",
    r"\bthanks\b", r"\bthank you\b", r"\bappreciate\b",
    r"\bwkwk\b", r"\bwkwkwk\b", r"\bhaha\b",
]

GREETING_PATTERNS = [
    r"\bhalo\b", r"\bhai\b", r"\bhi\b", r"\bhello\b",
    r"\bselamat pagi\b", r"\bselamat siang\b", r"\bselamat malam\b",
    r"\bpagi\b", r"\bsiang\b", r"\bmalam\b",
    r"\bkak\b", r"\bmin\b", r"\bbang\b", r"\bbro\b", r"\bsis\b",
]


def _match_any(text: str, patterns: list) -> list:
    matched = []
    for p in patterns:
        if re.search(p, text):
            matched.append(p.strip(r"\b"))
    return matched


def classify_comment(comment: str) -> dict:
    """
    Return: { category, is_lead, matched_signals, confidence }
    Category harus salah satu dari:
    unclassified, question, praise, spam, toxic, neutral
    """
    if not comment or not comment.strip():
        return {
            "category": "unclassified",
            "is_lead": False,
            "matched_signals": [],
            "confidence": "low",
        }

    text = comment.lower()

    # 1. Spam
    spam_hits = _match_any(text, SPAM_PATTERNS)
    if spam_hits:
        return {
            "category": "spam",
            "is_lead": False,
            "matched_signals": spam_hits,
            "confidence": "high" if len(spam_hits) >= 2 else "medium",
        }

    # 2. Toxic
    toxic_hits = _match_any(text, TOXIC_PATTERNS)
    if toxic_hits:
        return {
            "category": "toxic",
            "is_lead": False,
            "matched_signals": toxic_hits,
            "confidence": "high",
        }

    # 3. Lead (is_lead flag TRUE, category tetap question)
    lead_hits = _match_any(text, LEAD_PATTERNS)
    if lead_hits:
        return {
            "category": "question",
            "is_lead": True,
            "matched_signals": lead_hits,
            "confidence": "high" if len(lead_hits) >= 2 else "medium",
        }

    # 4. Question biasa
    question_hits = _match_any(text, QUESTION_PATTERNS)
    if question_hits:
        return {
            "category": "question",
            "is_lead": False,
            "matched_signals": question_hits,
            "confidence": "high" if len(question_hits) >= 2 else "medium",
        }

    # 5. Praise
    praise_hits = _match_any(text, PRAISE_PATTERNS)
    if praise_hits:
        return {
            "category": "praise",
            "is_lead": False,
            "matched_signals": praise_hits,
            "confidence": "high" if len(praise_hits) >= 2 else "medium",
        }

    # 6. Greeting
    greeting_hits = _match_any(text, GREETING_PATTERNS)
    if greeting_hits:
        return {
            "category": "neutral",
            "is_lead": False,
            "matched_signals": greeting_hits,
            "confidence": "medium",
        }

    # 7. Fallback
    return {
        "category": "neutral",
        "is_lead": False,
        "matched_signals": [],
        "confidence": "low",
    }
