"""Run every question in a CSV through the pipeline and save the results.

    uv run python tests/run_questions.py                  # writes tests/results/before.md
    uv run python tests/run_questions.py --tag after      # after your Step 4 change
    uv run python tests/run_questions.py -k 5 --tag k5

The index is built once and reused for every question, so the corpus is
embedded once per run, not once per question. The output file has an empty
"pass" and "what went wrong, where" column for you to fill in by hand.
"""

import argparse
import csv
import sys
from pathlib import Path

from dotenv import load_dotenv

# The Week 1 folder (one level above tests/). Everything else is found relative
# to it, so the script works no matter which directory you run it from.
ROOT = Path(__file__).resolve().parent.parent

# tests/ isn't a package, so Python can't see retrieval_app from here by
# default. Putting ROOT on the import path fixes that. The imports below have
# to come after this line, hence the noqa comments silencing the linter.
sys.path.insert(0, str(ROOT))

from retrieval_app import answer as answer_stage  # noqa: E402
from retrieval_app import corpus as corpus_stage  # noqa: E402
from retrieval_app import index as index_stage  # noqa: E402


def read_questions(path: Path) -> list[dict]:
    """Read the CSV, tolerating spaces around header names and values."""
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    cleaned = []
    for row in rows:
        # A header like "id, question" would otherwise give the key " question".
        # Stripping and lowercasing every key and value makes the CSV forgiving.
        row = {(k or "").strip().lower(): (v or "").strip() for k, v in row.items()}
        # Skip blank lines or rows with no question.
        if row.get("question"):
            cleaned.append(row)
    return cleaned


def one_line(text: str) -> str:
    """Collapse whitespace and escape pipes so text fits in a markdown table cell."""
    # A newline or a "|" inside a cell would break the markdown table.
    return " ".join(text.split()).replace("|", "\\|")


def main() -> int:
    # Command-line options. The defaults match this repo, so a plain run needs none.
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--questions", type=Path, default=ROOT / "tests" / "manual_questions.csv")
    parser.add_argument("--corpus", type=Path, default=ROOT / "data" / "HealthWellnessGuide.txt")
    parser.add_argument("-k", type=int, default=3, help="chunks to retrieve per question (default: 3)")
    parser.add_argument("--tag", default="before", help="name of the results file (default: before)")
    args = parser.parse_args()

    # Load OPENAI_API_KEY from .env, the same way the app does.
    load_dotenv(ROOT / ".env")

    # Stages 1 to 3, run once: load the text, split it, and embed every chunk.
    # This is the only time the corpus gets embedded in this run.
    questions = read_questions(args.questions)
    text = corpus_stage.load_corpus(args.corpus)
    chunks = corpus_stage.split_corpus(text)
    matrix = index_stage.build_index(chunks)
    print(f"{args.corpus.name}: {len(chunks)} chunks, {len(questions)} questions, k={args.k}\n")

    # Stages 4 and 5, once per question: retrieve chunks, then ask the model.
    # Each question costs one small embedding call and one chat call.
    results = []
    for row in questions:
        hits = index_stage.search(row["question"], chunks, matrix, k=args.k)
        reply = answer_stage.answer(row["question"], hits)
        results.append((row, hits, reply))

        # Print as we go, so you can watch progress and spot problems early.
        print(f"--- Q{row.get('id', '?')}: {row['question']}")
        if row.get("expected"):
            print(f"expected: {row['expected']}")
        print(reply)
        for hit in hits:
            print(f"  {hit.citation()}")
        if not hits:
            print("  (none retrieved)")
        print()

    # Only add an "Expected" column if the CSV actually has expected answers.
    has_expected = any(row.get("expected") for row, _, _ in results)

    # Results go to tests/results/<tag>.md. Running again with the same tag
    # overwrites that file, including any notes you added by hand.
    out_dir = ROOT / "tests" / "results"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / f"{args.tag}.md"

    lines = [
        f"# Results: {args.tag}",
        "",
        f"Corpus `{args.corpus.name}`, {len(chunks)} chunks, k={args.k}.",
        "",
    ]

    # Summary table: one row per question. Pass and "what went wrong" are left
    # empty on purpose, because judging the answers is your job, not the script's.
    header = "| # | Question |" + (" Expected |" if has_expected else "") + " Chunks (score) | Pass | What went wrong, where |"
    # The separator row needs one "---|" per column, i.e. one fewer than the pipes.
    lines += [header, "|" + "---|" * (header.count("|") - 1)]
    for row, hits, _ in results:
        sources = ", ".join(f"{h.chunk_id} ({h.score:.2f})" for h in hits) or "none"
        cells = [row.get("id", ""), one_line(row["question"])]
        if has_expected:
            cells.append(one_line(row.get("expected", "")))
        cells += [sources, "", ""]
        lines.append("| " + " | ".join(cells) + " |")

    # Full detail below the table: each answer in full, plus what was retrieved.
    lines += ["", "## Answers", ""]
    for row, hits, reply in results:
        lines += [f"### Q{row.get('id', '?')}: {row['question']}", ""]
        if row.get("expected"):
            lines += [f"**Expected:** {row['expected']}", ""]
        lines += [reply.strip(), "", "**Retrieved:**", ""]
        # An empty list is falsy, so "or" swaps in a placeholder when nothing was retrieved.
        lines += [f"- `{hit.citation()}`" for hit in hits] or ["- (none retrieved)"]
        lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"saved {out_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
