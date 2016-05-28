import unittest

from run import parse_articles


class TestXMLParsing(unittest.TestCase):
    def test_parsing(self):
        with open('test_response.xml') as f:
            xml = f.read()
        articles = parse_articles(xml)
        self.assertEqual(len(articles), 26)
        self.assertEqual(
            articles[0].title[:30],
            'Real-Time Human Motion Capture'
        )


if __name__ == '__main__':
    unittest.main()
