import endb


def test_connect():
    host = "192.168.2.124:3306"
    db = endb.Connection(host, "item_name", "root", "root12345678")
    print("echo =>", db)


test_connect()
