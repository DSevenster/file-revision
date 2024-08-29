import unittest
import revision

"""
Ideally, I would have like to mock out the file_ingest and rewrite in the tests.
But alas, time constraints got the better of me
"""


class TestRevision(unittest.TestCase):
    # the example given in the test document doesn't correspond to the syntax of the files
    # i.e. revision_id == filename for the attached files
    # unlike the example where they are different identifiers
    def test_determine_revision_sequence(self):
        input_dict = {
            "A": {"revision_id": "A", "revises_id": "B"},
            "B": {"revision_id": "B", "revises_id": None},
            "C": {"revision_id": "C", "revises_id": "A"},
        }
        expected_result = ["B", "A", "C"]

        result = revision.determine_revision_sequence(input_dict)
        self.assertListEqual(expected_result, result)

    def test_content_extraction_revision_id(self):
        input_string = "revision_id = '0a99bbeb77cb0de27593fea346ad362d'"
        expected_result = "0a99bbeb77cb0de27593fea346ad362d"

        result = revision.content_extraction(input_string)
        assert result == expected_result

    def test_content_extraction_revises_id(self):
        input_string = "revises_id = '7cd8edbd067e751a33ce7b5868605f0d'"
        expected_result = "7cd8edbd067e751a33ce7b5868605f0d"

        result = revision.content_extraction(input_string)
        assert result == expected_result

    def test_content_extraction_failure(self):
        input_string = "7cd8edbd067e751a33ce7b5868605f0d"

        result = revision.content_extraction(input_string)
        assert result is None


if __name__ == "__main__":
    unittest.main()
