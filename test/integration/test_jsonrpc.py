import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from advanced import AdvanceDaemon
from advance_config import AdvanceConfig


def test_advanced():
    config_text = AdvanceConfig.slurp_config_file(config.advance_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'0000048c2773ffa14cfbde0c0834cd0bcde6f3e067bf2a05c7612490264321f9'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'0000063f66dca0ac5e709cfb3af53c2c4c04d65427be619f69eb2c678b54476d'

    creds = AdvanceConfig.get_rpc_creds(config_text, network)
    advanced = AdvanceDaemon(**creds)
    assert advanced.rpc_command is not None

    assert hasattr(advanced, 'rpc_connection')

    # Advance testnet block 0 hash == 00000bafbc94add76cb75e2ec92894837288a481e5c005f6563d91623bf8bc2c
    # test commands without arguments
    info = advanced.rpc_command('getinfo')
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
    assert advanced.rpc_command('getblockhash', 0) == genesis_hash
