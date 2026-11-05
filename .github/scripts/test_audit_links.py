from email.message import Message
from io import BytesIO
from pathlib import Path
import runpy
from tempfile import TemporaryDirectory
import unittest


ROOT = Path(__file__).resolve().parents[2]
AUDIT = runpy.run_path(str(ROOT / '.agents/skills/brainx-doc-sync/scripts/audit_links.py'))


class AuditLinksTest(unittest.TestCase):
    def test_table_links_and_skipped_query_locations(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            page = root / 'table.md'
            page.write_text(
                '|[A](https://example.com/a)|[B](https://example.com/b_(c)#section)|\n'
                '[Query](https://example.com/search?q=test)\n',
                encoding='utf-8',
            )
            refs, skipped = AUDIT['inventory'](root, [page])
            self.assertEqual(list(refs), ['https://example.com/a', 'https://example.com/b_(c)'])
            self.assertEqual(refs['https://example.com/b_(c)'][0]['fragment'], 'section')
            self.assertEqual(skipped, [{'file': 'table.md', 'line': 2}])

    def test_missing_relative_targets_ignore_examples(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            page = root / 'README.md'
            (root / 'present (1).md').touch()
            page.write_text(
                '[Present](<present (1).md#heading>)\n'
                '[Missing](missing(1).md)\n'
                '`[Inline example](example.md)`\n'
                '```markdown\n[Fenced example](example.md)\n```\n',
                encoding='utf-8',
            )
            self.assertEqual(AUDIT['missing_local_targets'](root, [page]), [
                {'file': 'README.md', 'line': 2, 'target': 'missing(1).md'},
            ])

    def test_static_fragment_lookup(self):
        response = BytesIO('<h2 id="café">Title</h2><a name="old"></a>'.encode())
        response.headers = Message()
        response.headers['Content-Type'] = 'text/html; charset=utf-8'
        self.assertEqual(AUDIT['check_anchors'](response, ['caf%C3%A9', 'old', 'absent']), {
            'caf%C3%A9': 'found',
            'old': 'found',
            'absent': 'missing_candidate',
        })


if __name__ == '__main__':
    unittest.main()
