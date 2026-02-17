---
name: start-draft
description: This skill should be used when the user asks to "start a draft", "create a new post", "write a new blog post", "begin a new article", "draft a blog entry", or generally wants to scaffold a new blog post for the site.
version: 1.0.0
---

# Start Draft

Create a new blog post draft for the Pelican-based site at scottberrevoets.com.

## File Naming Convention

Blog post files live in `content/` and follow this naming pattern:

```
YYYY-MM-DD-slug.md
```

- Use today's date for the date prefix
- Derive the slug from the post title (lowercase, hyphens, no special characters)

## Post Metadata

Every post begins with Pelican metadata (no YAML frontmatter — just key-value lines):

```
Title: The post title
Date: YYYY-MM-DD
Description: A one-sentence summary of the post
```

- `Title` should be sentence case (not title case)
- `Description` should be concise and suitable for social sharing / SEO
- Leave a blank line after the metadata before the body content

## Workflow

1. Ask the user for a working title and topic (if not already provided)
2. Create the file at `content/YYYY-MM-DD-slug.md` with the metadata header
3. Add a brief placeholder paragraph or outline based on the topic
4. Open the file for further editing

## Example

For a post titled "Why types matter" on 2026-02-16:

**File:** `content/2026-02-16-why-types-matter.md`

```
Title: Why types matter
Date: 2026-02-16
Description: An exploration of how strong typing improves code quality

Start writing here...
```
