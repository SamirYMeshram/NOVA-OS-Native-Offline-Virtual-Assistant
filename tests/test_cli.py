from nova.cli.main import build_parser

def test_cli_parser():
    args = build_parser().parse_args(['chat', 'hello'])
    assert args.cmd == 'chat'
