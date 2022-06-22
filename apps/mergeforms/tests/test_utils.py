def test_save_string_to_tempfile():
    body="This is the body of the text"
    fn = save_string_to_tempfile(body)
    assert os.path.exists(fn)
