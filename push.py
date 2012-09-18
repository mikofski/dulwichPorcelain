from dulwich.repo import Repo
from dulwich.client import get_transport_and_path
import sys


def push(remote_url, repo_path='.'):
    """
    Push to a remote repository
    :param remote_url: <str> url of remote repository
    :param repo_path: <str> path of local repository
    :return refs: <dict> dictionary of ref-sha pairs
    """
    client, path = get_transport_and_path(remote_url)
    r = Repo(repo_path)
    objsto = r.object_store
    refs = r.get_refs()
    def update_refs(old):
        # TODO: Too complicated,  not necessary to find the refs that
        # differ - it's fine to update a ref even if it already exists.
        # TODO: Also error out if there are non-fast forward updates
        same = list(set(refs).intersection(old))
        new = dict([(k,refs[k]) for k in same if refs[k] != old[k]])
        dfky = list(set(refs) - set(new))
        dfrnt = dict([(k,refs[k]) for k in dfky if k != 'HEAD'])
        return dict(new.items() + dfrnt.items())
    return client.send_pack(path,
                            update_refs,
                            objsto.generate_pack_contents,
                            sys.stdout.write)
