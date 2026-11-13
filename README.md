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

## Validate

```
make validate
```

Zero dependencies; Python 3.12 and `unittest` only.
