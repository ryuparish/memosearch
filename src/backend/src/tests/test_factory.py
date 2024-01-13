from memosearch import create_app

# Test for correct configuration
def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing
