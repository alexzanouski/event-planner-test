---
name: artifact-validator
description: Structural and citation check for a workflow artifact. Use on every new or changed artifact in runs/<run-id>/artifacts/ before dependent agents start.
---

# artifact-validator

Checks one artifact against the conventions in `docs/artifacts.md`.
It does not judge the quality of the plan, that is the `validator` agent's
job. It only decides whether the artifact is well-formed and its sources
are real.

## Input

Path to one artifact, for example `runs/<run-id>/artifacts/venue.md`.

## Structural check

1. The file starts with a title and the `Owner`, `Run`, `Status` lines.
2. `Owner` matches the agent that owns this artifact (see `CLAUDE.md`).
3. All sections required for this artifact type are present, in the order
   given in the "Required sections" table of `docs/artifacts.md`.
4. No section is empty.
5. No placeholders (`TBD`, `TODO`, `lorem ipsum`, `<...>`) when
   `Status: final`.
6. Costs, if any, use the currency from `requirements.md`.

## Citation check

Applies to artifacts that have a `Sources` section.

1. Every source line has a title and an `http(s)` URL.
2. Open each URL with WebFetch. The page must load and be about the
   thing it is cited for. A 404, a redirect to a home page, or an
   unrelated page fails.
3. Every venue, vendor, price or opening hour mentioned in `Details` is
   covered by at least one source.

## Output

Reply in exactly this format and do not edit the artifact:

```
ARTIFACT: <file name>
RESULT: PASS | FAIL
FINDINGS:
- <check number or name>: <what is wrong>, <where>
```

Use `FINDINGS: none` on PASS. Keep findings specific enough that the
owning agent can fix them without re-reading the whole file.
