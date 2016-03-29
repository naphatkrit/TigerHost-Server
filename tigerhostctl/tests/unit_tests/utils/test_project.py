from tigerhostctl.project import get_project_path, save_project_path


def test_project_path(ensure_private_dir):
    assert get_project_path() is None
    save_project_path('/test/../')
    assert get_project_path() == '/'
