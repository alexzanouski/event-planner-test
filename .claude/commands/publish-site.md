---
description: Build the static site of approved events and publish it to Cloudflare Pages
argument-hint: (no arguments)
---

You publish the approved event guides as a static site. Publishing makes
the pages public, so it only happens after the user confirms.

## 1. Build

Run `python3 scripts/build_site.py`. It includes only runs whose plan is
approved and unchanged since approval. Read its output. If it built no
events, tell the user there is nothing to publish and stop.

## 2. Check access

Run `npx wrangler whoami`. If it reports that nobody is logged in, tell
the user to run `npx wrangler login`, or to export `CLOUDFLARE_API_TOKEN`
and `CLOUDFLARE_ACCOUNT_ID`, then stop. Do not print tokens or account
details.

## 3. Confirm

The project name is `$CLOUDFLARE_PAGES_PROJECT`, or `event-planner-guides`
if it is not set. Ask with `AskUserQuestion` whether to publish, naming
the project and listing the events by title and date. Say that the pages
will be publicly reachable. Continue only on a clear yes.

## 4. Publish

1. If the project does not exist (`npx wrangler pages project list`),
   create it: `npx wrangler pages project create <project> --production-branch main`.
2. Deploy: `npx wrangler pages deploy site --project-name <project> --branch main`.
3. Report the address wrangler printed and the list of published events.

Do not edit anything inside `site/` by hand: it is generated and
replaced on every build.
