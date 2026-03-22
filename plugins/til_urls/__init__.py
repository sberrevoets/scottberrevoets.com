from pelican import signals


def set_til_urls(generator):
    for article in generator.articles:
        if article.category.name == "til":
            article.override_url = f"til/{article.slug}/"
            article.override_save_as = f"til/{article.slug}/index.html"
            article.template = "til_article"


def register():
    signals.article_generator_finalized.connect(set_til_urls)
