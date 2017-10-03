def test_ping(client):
    """Test simple ping endpoint"""
    res = client.get('/ping')
    assert b'pong' in res.data


def test_simple(client, db, test_packages):
    """Test simple view index"""
    res = client.get('/simple/')
    assert b'test-package' in res.data
    assert b'other-package' in res.data


def test_simple_package(client):
    """Test simple index for specific package"""
    # res = client.get('/simple/test-package')
    # assert b'test-package-0.1.tar.gz' in res.data


def test_simple_package_download(client):
    """Test download of a package version"""
    # res = client.get('/simple/test-package/')


def test_list_packages(client):
    """Test list packages view"""


def test_package_details(client):
    """Test view for package details"""


def test_delete_package(client):
    """Test delete of package"""


def test_package_upload(client):
    """Test upload of a package"""


def test_list_users(client):
    """Test list users view"""


def test_create_users(client):
    """Test creation of a new user"""


def test_update_user(client):
    """Test update of a user"""


def test_delete_user(client):
    """Test deletion of a user"""
