import os

from pelican import signals


def write_markdown_files(generator):
    for article in generator.articles:
        with open(article.source_path, "r") as f:
            raw = f.read()

        # Strip Pelican metadata (everything before the first blank line)
        parts = raw.split("\n\n", 1)
        body = parts[1] if len(parts) > 1 else raw

        # Build description line
        description = getattr(article, "description", None) or article.metadata.get(
            "summary", ""
        )

        # Format the date
        date_str = article.date.strftime("%Y-%m-%d")

        # Assemble the clean markdown
        header = f"# {article.title}\n\n{date_str}"
        if description:
            header += f"\n\n{description}"
        header += "\n\n---"

        output = f"{header}\n\n{body}"

        # Derive output path from save_as (e.g. 2025/09/19/slug/index.html -> 2025/09/19/slug.md)
        md_path = article.save_as.replace("/index.html", ".md")
        full_path = os.path.join(generator.output_path, md_path)

        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w") as f:
            f.write(output)


def register():
    signals.article_generator_finalized.connect(write_markdown_files)
