#! /usr/bin/env/ python

import sys, os, csv
from dulwich.repo import Repo
from dulwich.client import get_transport_and_path
from dulwich.errors import NotGitRepository
from dulwich.file import ensure_dir_exists, GitFile
from dulwich.config import ConfigFile

DULWICH_REFS = 'dulwich_refs' # folder to save refs fetched by dulwich


def fetch_refs(remote_name = 'origin', local='.'):
    """
    Fetch references from a Git remote repository
    :param remote_name: <str> git name of remote repository, _default='origin'_
    :param local: <str> full path to local repository, _default='.'_
    :return entries: <TreeEntry> named tuples
    """
    #import rpdb; rpdb.set_trace()
    # **Fetch refs from remote**
    # create a dulwich Repo object from path to local repo
    r = Repo(local)  # local repository
    objsto = r.object_store  # create a ObjectStore object from the local repo
    determine_wants = objsto.determine_wants_all  # built in dulwich function
    gitdir = os.path.join(local, r.controldir())  # the git folder
    cnf_file = os.path.join(gitdir, 'config')  # path to config
    cnf = ConfigFile.from_path(cnf_file)  # config
    remote = cnf.get(('remote', remote_name), 'url')  # url of remote
    # correctly parse host path and create dulwich Client object from it
    client, host_path = get_transport_and_path(remote)
    remote_refs = client.fetch(host_path, r, determine_wants, sys.stdout.write)

    # **Store refs fetched by dulwich**
    dulwich_refs = os.path.join(gitdir, DULWICH_REFS)
    with open(dulwich_refs, 'wb') as file:
        writer = csv.writer(file, delimiter=' ')
        for key, value in remote_refs.items():
            writer.writerow([key, value])

    # **save remote refs shas for future checkout**
    remote_dir = os.path.join(gitdir, 'refs', 'remotes', remote_name)  # .git/refs/remotes
    ensure_dir_exists(remote_dir)  # built in dulwich function
    headref = 0
    # head branch ref
    if remote_refs.has_key('HEAD'):
        headref = remote_refs.pop('HEAD')  # sha of HEAD
        i_head = remote_refs.values().index(headref)  # index of head ref
        head_branch = remote_refs.keys()[i_head]  # name of head branch
        branch_key = head_branch.rsplit('/',1)[-1]  # branch
        head_file = os.path.join(remote_dir, 'HEAD')  # path to branch shas file
        with open(head_file, 'wb') as GitFile:
            GitFile.write('/'.join(['refs','remotes',remote_name,branch_key]) + '\n')
    # remote branch refs
    for key, value in remote_refs.items():
        key = key.rsplit('/',1)[-1]  # get just the remote's branch
        reffile = os.path.join(remote_dir, key)  # path to branch shas file
        with open(reffile, 'wb') as GitFile:
            GitFile.write(value + '\n')
    if headref:
        remote_refs['HEAD'] = headref  # restore HEAD sha

    return remote_refs

if __name__ == "__main__":
    fetch_refs(*sys.argv[1:])
    print "fetch %s for %s" % sys.argv[1:2]