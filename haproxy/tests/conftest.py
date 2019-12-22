# -*- coding: utf-8 -*-
from copy import deepcopy
from haproxy.line import Line

import pytest


DEFAULT_DATA = {
    'syslog_date': 'Dec  9 13:01:26',
    'process_name_and_pid': 'localhost haproxy[28029]:',
    'client_ip': '127.0.0.1',
    'client_port': 2345,
    'accept_date': '09/Dec/2013:12:59:46.633',
    'frontend_name': 'loadbalancer',
    'backend_name': 'default',
    'server_name': 'instance8',
    'tq': 0,
    'tw': 51536,
    'tc': 1,
    'tr': 48082,
    'tt': '99627',
    'status': '200',
    'bytes': '83285',
    'act': '87',
    'fe': '89',
    'be': '98',
    'srv': '1',
    'retries': '20',
    'queue_server': 2,
    'queue_backend': 67,
    'headers': ' {77.24.148.74}',
    'http_request': 'GET /path/to/image HTTP/1.1',
}


@pytest.fixture
def default_line_data():
    return DEFAULT_DATA


@pytest.fixture
def line_factory():
    def _build_test_string(**kwargs):
        data = deepcopy(DEFAULT_DATA)
        data.update(**kwargs)
        data['client_ip_and_port'] = '{client_ip}:{client_port}'.format(**data)
        data['server_names'] = '{frontend_name} {backend_name}/{server_name}'.format(
            **data
        )
        data['timers'] = '{tq}/{tw}/{tc}/{tr}/{tt}'.format(**data)
        data['status_and_bytes'] = '{status} {bytes}'.format(**data)
        data['connections_and_retries'] = '{act}/{fe}/{be}/{srv}/{retries}'.format(
            **data
        )
        data['queues'] = '{queue_server}/{queue_backend}'.format(**data)

        # queues and headers parameters are together because if no headers are
        # saved the field is completely empty and thus there is no double space
        # between queue backend and http request.
        raw_line = (
            '{syslog_date} {process_name_and_pid} {client_ip_and_port} '
            '[{accept_date}] {server_names} {timers} {status_and_bytes} '
            '- - ---- {connections_and_retries} {queues}{headers} '
            '"{http_request}"'
        )
        log_line = raw_line.format(**data)
        return Line(log_line)

    return _build_test_string
