import pytest
from main import article_parser


def test_article_parser():
    article = """
    TITLWEREWREW 
    SDFDSFDSFSD

    SDFDSF
    """
    assert article_parser(article) == "Could not find the article"
    answer = article_parser("https://original.com")
    print(answer)
    assert answer["title"] == "Some original news article"


if __name__ == "__main__":
    pytest.main()
