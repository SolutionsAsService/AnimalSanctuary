# Mesa Animal Rescue

A concept website for a small animal rescue in Mesa, Arizona: cats, dogs and rabbits waiting for homes, plus fostering, volunteering and giving. The animals, people and address are illustrative, and the site takes no adoptions or donations; it says so in the footer and on the Give page.

The original version is kept on the `legacy-2026-10-30` branch.

## Pages

| Page | What |
|---|---|
| `index.html` | Home: the mission, three animals to meet, four ways to help |
| `adopt.html` | All six animals with a Dogs / Cats / Rabbits filter, how adoption works, fees |
| `foster.html` | What fostering involves and who's needed |
| `volunteer.html` | Volunteer roles and shifts |
| `give.html` | What gifts pay for, the wish list, where money goes |
| `about.html` | Promises and team |
| `contact.html` | Contact form (prefills the animal from `?about=`) and visiting hours |

## Layout

- `site/`: the deployable static site (HTML, `css/`, `js/`, `favicon.svg`).
- `_src/`: the generator. `layout.html`, `pages/*.html` and `build.py`, which also draws each animal's portrait (`{{pet:dog:#B9824F}}`), so there are no stock photos.

## Build

```bash
python _src/build.py
```

Edit `_src/`, not the generated HTML in `site/`. The build fails if a page links to a local file that doesn't exist.

## Form

With no endpoint, the contact form opens the visitor's mail app with the message filled in. To receive messages directly, set `FORM_ENDPOINT` in `site/js/site.js` to a form service URL.

## Deploy

Ready for Vercel with no build step: the root `vercel.json` serves `site/`, and `site/vercel.json` does the same if the Vercel Root Directory is set to `site`. The root `index.html` redirects to the site.
