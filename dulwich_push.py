from dulwich.repo import Repo
from dulwich.client import get_transport_and_path
from getopt import getopt
import sys


def push(args):
    opts, args = getopt(args, "", [])
    opts = dict(opts)
    client, path = get_transport_and_path(args.pop(0))
    r = Repo(".")
    objsto = r.object_store
    refs = r.get_refs()
    def determine_wants_new(old):
        same = list(set(refs).intersection(old))
        new = dict([(k,refs[k]) for k in same if refs[k] != old[k]])
        dfky = list(set(refs) - set(new))
        dfrnt = dict([(k,refs[k]) for k in dfky if k != 'HEAD'])
        return dict(new.items() + dfrnt.items())
    refs = client.send_pack(path,
                            determine_wants_new,
                            objsto.generate_pack_contents,
                            sys.stdout.write)
