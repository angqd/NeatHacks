# BM25 sanity check on the original LiveMCPBench tasks

This is a sanity check against an unverified self-reported number: 31.68 Recall@5 (toolrank README). It is not a gate. No variant was chosen or tuned to hit that number, and no winner is declared.

## Protocol

- Tasks: `data/processed/tasks_resolved.jsonl`, 95 original tasks. Query text is the task `question` only. Gold is the bench reference tool names (`gold_names`), no server.
- Name view: a returned tool counts for a gold name if `tool.name` equals it, on any server. Gold names that appear nowhere in the catalog are dropped from that task's denominator.
- Id view: a gold name counts only when uniquely resolved in the catalog, and then the returned tool id must equal the exact id from `gold_ids`. Ambiguous and missing names are skipped.
- Per task Recall@k = distinct gold names matched in the top k / distinct gold names. Reported as the mean over kept tasks, in percent. Tasks with zero gold names are dropped.
- Document variants: every entry of `toolprune.text.VARIANTS`, scored with `BM25Retriever(load_tools(), variant)` at k1=1.5, b=0.75.
- Not known about the reference: its document text, its query set (the self-reported figure is over 94 queries, here 95 tasks), and its gold matching rule. The gap is documented, not tuned away.

## Results (percent, mean Recall@k over kept tasks)

| Variant | Name R@5 | Name R@10 | Id R@5 | Id R@10 | Name kept | Id kept | Name dropped gold | Id dropped gold |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `name_desc_server` | 36.06 | 44.16 | 41.44 | 50.76 | 94 | 91 | 5 | 34 |
| `name_desc` | 36.41 | 42.56 | 40.16 | 48.75 | 94 | 91 | 5 | 34 |
| `desc_only` | 29.44 | 35.47 | 31.82 | 38.82 | 94 | 91 | 5 | 34 |
| `name_only` | 27.04 | 33.60 | 29.16 | 36.39 | 94 | 91 | 5 | 34 |
| `full` | 37.83 | 44.03 | 43.36 | 51.37 | 94 | 91 | 5 | 34 |

Self-reported reference: 31.68 Recall@5 (unverified).
