from chalicelib.cw_log import CWLog

def test_log(client):
    # CWLog.set_groups()
    # CWLog.list_log_groups()
    # CWLog.create_log_stream()
    CWLog.send_cw_log('pizda 2')