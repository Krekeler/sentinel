import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from dmsd import DMSDaemon
from dms_config import DMSConfig


def test_dms():
    config_text = DMSConfig.slurp_config_file(config.dms_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'00000af4a21d6e8daa4026a5eafc7132089a7dbb9d3921b12c4fa39b78c9a010'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'00004399a114a034b2f8d742b8e7f018d3cfdec0b25150d0b7e271b63c9cd4ce'

    creds = DMSConfig.get_rpc_creds(config_text, network)
    dmsd = DMSDaemon(**creds)
    assert dmsd.rpc_command is not None

    assert hasattr(dmsd, 'rpc_connection')

    # Documentchain testnet block 0 hash == 00004399a114a034b2f8d742b8e7f018d3cfdec0b25150d0b7e271b63c9cd4ce
    # test commands without arguments
    info = dmsd.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert dmsd.rpc_command('getblockhash', 0) == genesis_hash
