# BeFree by BeLive

Generic property-partner website based on the approved BeLive design. The original condo-specific repository remains untouched.

## Review the website

[Open the BeFree website preview](https://raw.githack.com/keithkuang-BeLive/BeFree/main/index.html)

This is a review preview, not a claimed Vercel production deployment.

## Deploy on Vercel

Import `keithkuang-BeLive/BeFree`, branch `main`. Framework: **Other**. Root: repository root. Build: `npm run build`. Output: `dist`. Configuration is included in `vercel.json`.

`public/` is the normal website. Root `index.html` is the same application as a single-file review preview (images, CSS and JS embedded; original public typefaces referenced). No secrets or private records are included.

## Data scope

The uploaded portfolio report covers eight properties, 896 lettable rooms and 195 active units. It reports 95.5% September occupancy (856/896 rooms), 57.3% renewals on 1,019 expiring contracts, and 2,278 tenants housed to date. September is incomplete. Occupancy means at least one tenancy-covered day in the month, not daily occupancy. Highest recorded unit rent is RM5,750 gross before costs, not a typical or guaranteed return. These are not company-wide totals.

Google review figures and selected collaboration logos are retained from the original approved template and are separately qualified on the page. No review numbers are represented as live. Services and the 0% fee model remain subject to package terms and other charges.

## Reproduce this version

`scripts/create-portfolio.py` applies the documented content changes to the pinned original compiled template. It does not claim to recover the original editable React/TypeScript source. Use the accompanying workflow to rebuild from that pinned reference. The supplied raw portfolio report is not published.

This is a draft and carries `noindex,nofollow` until approved for launch.


## Visual-first revision

The introduction now shows **4,500 rooms under management**, a company-wide figure explicitly supplied by Keith on 22 September 2026. It is not derived from the eight-property report. The 2,278-tenants and 896-rooms promotional cards were removed. Case-study performance remains separately labelled. A real team photo, six interactive team functions and an unmodified Google wordmark replace text-heavy introductory blocks. Review figures remain an explicitly labelled non-live company-profile snapshot. Run `python scripts/refine-introduction.py` after `scripts/create-portfolio.py` to reproduce this revision.
