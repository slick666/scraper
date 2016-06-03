from unittest import TestCase

from videodata.videodata import text_tools


class TextToolsTestCase(TestCase):
    def test_extract_speakers_empty(self):
        text = '''Intro'''

        speakers = text_tools.extract_speakers(text)

        self.assertEqual([], speakers)

    def test_extract_speakers_single(self):
        text = '''
        Intro
        Speaker: First Speaker
        Outro
        '''

        speakers = text_tools.extract_speakers(text)

        self.assertEqual(['First Speaker'], speakers)

    def test_extract_speakers_multiple(self):
        text = '''
        Intro
        Speaker: First Speaker, 高 國棟, Łąki Łan
        Outro
        '''

        speakers = text_tools.extract_speakers(text)

        self.assertIn('First Speaker', speakers)
        self.assertIn('高 國棟', speakers)
        self.assertIn('Łąki Łan', speakers)
