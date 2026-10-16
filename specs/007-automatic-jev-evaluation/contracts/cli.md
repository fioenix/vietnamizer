# Public CLI Contract

From the installed skill root:

```bash
python3 -B -m jev status
python3 -B -m jev evaluate --input input.json
python3 -B -m jev evaluate --input input.json --pattern V20
```

status emits only key_available/key_absent and makes no network call. evaluate with no injected key returns key_absent before reading an input. With a key, stdin is used if --input is omitted. The individual-pattern diagnostic declares single_pattern coverage.

Example authorized synthetic input:

```json
{"transmission_allowed":true,"sections":[{"id":"p1","profile":"blog","kind":"prose","text":"Tao hiểu. Mày cứ nói tiếp.","context":[]}]}
```

Only TYPESAFE_API_KEY from the execution environment is read. No key discovery, endpoint override or redirect is supported. The only outbound endpoint is POST https://api.typesafe.ai/v1/systemone; model jev-1.14.0.

Exit 0: evaluated or key_absent. Exit 2: noncompleted/denied/invalid evaluation. Host core editing still continues on exit 2 while preserving actual evaluator state. Results never contain an automatic edit decision.

Runtime bounds: 1 MiB input/response, 48,000-byte request, 48 questions/request, 32 requests, 120 seconds overall, 15 seconds/request. No automatic retry or cross-invocation cache shortcut. Context is never silently truncated to fit.
