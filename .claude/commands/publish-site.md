---
description: Build the static site of approved events and publish it to Cloudflare as static assets
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

The site name is `$CLOUDFLARE_SITE_NAME`, or `event-planner-guides` if it
is not set. Ask with `AskUserQuestion` whether to publish, naming the
site and listing the events by title and date. Say that the pages will be
publicly reachable. Continue only on a clear yes.

## 4. Publish

Deploy the generated folder as static assets (Cloudflare Workers static
assets, the current way to host static sites there; the first deploy
creates the site):

```
npx wrangler deploy --assets site --name <site> --compatibility-date <today>
```

Do not use `wrangler pages project create` or `--force`: current wrangler
delegates Pages commands to Workers and the project creation step fails
for a site without a Worker script.

Report the address wrangler printed and the list of published events. If
the deploy fails, report the error and stop, do not retry with other
flags.

Do not edit anything inside `site/` by hand: it is generated and
replaced on every build.
