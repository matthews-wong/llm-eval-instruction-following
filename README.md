# llm-eval-instruction-following

Check whether a model response obeys the instructions in its prompt, using
only rules a program can verify: word limits, required and banned terms,
bullet counts, JSON-only output, casing and endings. No judge model, no
network.

Each case carries a prompt, a recorded response and a list of constraints.
The report gives two numbers, in the style of IFEval:

- **instruction accuracy**: share of individual constraints satisfied
- **prompt accuracy**: share of cases where every constraint is satisfied

Prompt accuracy is the stricter of the two and is the one to gate on.

## Usage

```
python3 -m ifeval data/cases.jsonl
```

## Constraints

| kind | argument | passes when |
| --- | --- | --- |
| `max_words` / `min_words` | int | whitespace-separated word count is within the bound |
| `max_sentences` | int | sentence-ending marks do not exceed the bound |
| `include` / `exclude` | list of strings | all / none of the terms appear, ignoring case |
| `bullets` | int | exactly this many `-` or `*` bullet lines |
| `lowercase` / `no_commas` | bool | no uppercase letters / no commas |
| `ends_with` | string | response ends with the string, ignoring trailing whitespace |
| `json_object` | bool | the whole response parses as a JSON object |

An unknown kind is rejected when the file is loaded, so a typo cannot
silently count as a pass.

## Fixture result

`data/cases.jsonl` holds 12 hand-written cases, half of them written to
fail. `make eval` on it gives 50.0% prompt accuracy and 58.8% instruction
accuracy (17 constraints). That is a fixture, not a model benchmark.

Use `--min-prompt-accuracy 0.9` to exit 1 when a run falls below a threshold.

## Validate

```
make validate
```

Zero dependencies; Python 3.12 and `unittest` only.
