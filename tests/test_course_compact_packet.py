"""Execute the literal packed source cell; no dependency downloads or inference."""

import hashlib
import json
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch
import zipfile

from scripts.build_course_kaggle import notebook


class CompactPacketTests(unittest.TestCase):
    def fixture(self, base):
        package=base/"input/multi-agents"; package.mkdir(parents=True)
        commit="a"*40
        members={"SOURCE_COMMIT.txt":(commit+"\n").encode(),"recovery/fixture.py":b"# CPU fixture\n"}
        payload=package/"course-kaggle-source.payload"
        with zipfile.ZipFile(payload,"w",zipfile.ZIP_DEFLATED) as archive:
            for name,raw in members.items(): archive.writestr(name,raw)
        manifest=dict(payload_filename=payload.name,archive_bytes=payload.stat().st_size,
            archive_sha256=hashlib.sha256(payload.read_bytes()).hexdigest(),
            members={name:dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()) for name,raw in members.items()})
        encoded=json.dumps(manifest).encode(); (package/"source-manifest.json").write_bytes(encoded)
        document=notebook(hashlib.sha256(encoded).hexdigest(),commit)
        return package,payload,document,members

    def execute(self,base,document):
        display=types.SimpleNamespace(display=lambda *args:None,FileLink=str,HTML=str)
        values={}
        with patch.dict("os.environ",COURSE_WORKSPACE=str(base/"workspace"),COURSE_INPUT=str(base/"input")), \
                patch.dict(sys.modules,{"IPython":types.ModuleType("IPython"),"IPython.display":display}):
            for name in ("action","source"):
                cell=next(c for c in document["cells"] if c["id"]==name)
                exec("".join(cell["source"]),values)
        return values

    def test_two_input_files_extract_only_verified_research_members(self):
        with tempfile.TemporaryDirectory() as directory:
            base=Path(directory); package,payload,document,members=self.fixture(base)
            self.assertEqual(len(list(package.iterdir())),2)
            self.assertFalse((package/"recovery").exists())
            values=self.execute(base,document)
            for name,raw in members.items(): self.assertEqual((values["source"]/name).read_bytes(),raw)
            self.assertEqual((values["source"]/"source-manifest.json").read_bytes(),(package/"source-manifest.json").read_bytes())
            # Running the same source cell again verifies the saved source,
            # without re-extracting or replacing the original working copy.
            self.execute(base,document)

    def test_modified_packed_archive_refuses_before_source_extraction(self):
        with tempfile.TemporaryDirectory() as directory:
            base=Path(directory); package,payload,document,members=self.fixture(base)
            payload.write_bytes(payload.read_bytes()+b"unexpected bytes")
            with self.assertRaisesRegex(ValueError,"research archive differs"):
                self.execute(base,document)
            self.assertFalse((base/"workspace/bundle/source").exists())


if __name__=="__main__":
    unittest.main()
