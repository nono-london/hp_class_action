from hp_class_action.app_config import get_external_ip_address


def test_ip_address():
    assert isinstance(get_external_ip_address(), str) and len(get_external_ip_address()) > 0


if __name__ == '__main__':
    test_ip_address()
