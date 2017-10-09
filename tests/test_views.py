def test_ping(client):
    """Test simple ping endpoint"""
    res = client.get('/ping')
    assert b'pong' in res.data


def test_simple(client, db, packages, admin_headers):
    """Test simple view index"""
    res = client.get('/simple/', headers=admin_headers)
    assert b'test-package' in res.data
    assert b'other-package' in res.data


def test_simple_package(client, packages_dirs, releases_dirs, admin_headers):
    """Test simple index for specific package"""
    res = client.get('/simple/test-package/', headers=admin_headers)
    assert b'test-package-0.1' in res.data


def test_simple_package_download(client, packages_dirs,
                                 releases_dirs, admin_headers):
    """Test download of a package version"""
    res = client.get(
        '/simple/test-package/test-package-0.1.tar.gz/',
        headers=admin_headers
    )
    assert res.status_code == 200
    assert res.data == b'insidepackage'


def test_list_packages(client):
    """Test list packages view"""


def test_package_details(client):
    """Test view for package details"""


def test_delete_package(client):
    """Test delete of package"""


def test_package_upload(client, tmpdir, admin_headers):
    """Test upload of a package"""
    f = tmpdir.join("test")
    f.write("a simple test")
    data = {
        ':action': 'file_upload',
        'name': 'uploaded',
        'summary': 'from unittests',
        'description': 'simple upload test',
        'download_url': '',
        'home_page': '',
        'version': '0.1',
        'keywords': ['test', 'other'],
        'md5_digest': 'badhash',
        'file': (f.open('rb'), 'test-0.1.tar.gz')
    }
    resp = client.post('/simple/', headers=admin_headers, data=data)
    print(resp.data)
    assert resp.status_code == 200


def test_list_users(client):
    """Test list users view"""


def test_create_users(client):
    """Test creation of a new user"""


def test_update_user(client):
    """Test update of a user"""


def test_delete_user(client):
    """Test deletion of a user"""
