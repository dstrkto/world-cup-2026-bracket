# 2026 World Cup — radial knockout bracket

A single static page (`index.html`) that renders a radial bracket of the 2026 FIFA World Cup
knockout stage. It reads `bracket.json` at load time, so updating results only means editing that
JSON file and pushing — no code changes.

Hosted via GitHub Pages and embedded in the Notion dashboard.

## Updating results (`bracket.json`)

```jsonc
{
  "updated": "2026-06-28",            // shown in the header
  "note": "Round of 32 under way",    // optional sub-note (set to "" once knockouts start)
  "champion": null,                    // team name once the final is won, else null
  "m": {
    "73": { "t1": "Mexico", "t2": "Croatia", "s": "2-1", "w": 1 }
    // t1/t2: team names EXACTLY as in the Notion select (e.g. "USA", "Türkiye", "DR Congo")
    // s: score string "x-y" (regulation), or null if not played
    // w: 1 if t1 advances, 2 if t2 advances, null if undecided
  }
}
```

- Match numbers 73–88 = Round of 32, 89–96 = Round of 16, 97–100 = quarter-finals,
  101–102 = semi-finals, 103 = third place, 104 = final.
- Fill `t1`/`t2` as soon as a matchup is known (even before it's played) so the slot labels
  ("RU A", "W90") become real teams.
- Flags are looked up from the team name automatically.

## Deploy

```sh
git add bracket.json && git commit -m "Update results" && git push
```

GitHub Pages serves the latest within ~1 minute.
