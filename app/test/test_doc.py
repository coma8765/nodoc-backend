from . import *
from .fixtures import doc_type_ref, doc_ref, doc_obj


class TestDoc(BaseTest):
    async def test_create_doc_type(self):
        ref = doc_type_ref()
        r = await dc.add_doc_types(ref)
        assert_dict(ref.dict(), r)

    async def test_list_doc_types(self):
        objs = [(await dc.add_doc_types(doc_type_ref())).dict() for _ in range(5)]
        r = await dc.list_doc_types()
        assert_dict_in_list(objs, r)

    async def test_upload(self):
        refs = [await doc_ref() for _ in range(5)]
        r = await dc.upload_docs(refs)
        # noinspection PyTypeChecker
        assert_dict_in_list(map(dict, refs), r)

    async def test_list(self):
        refs = [await doc_obj() for _ in range(5)]
        refs.append(refs[0])
        r = await dc.list_doc_types()
        # noinspection PyTypeChecker
        assert_dict_in_list(map(dict, refs), r)
