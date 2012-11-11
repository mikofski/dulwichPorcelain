import sys, os, csv
from dulwich.repo import Repo
from dulwich.client import get_transport_and_path
from dulwich.file import ensure_dir_exists, GitFile
from dulwichPorcelain import checkout

DULWICH_REFS = 'dulwich_refs' # folder to save refs fetched by dulwich
REFS = 'refs' # git folder where ref shas are saved
REMOTES = 'remotes' # git folder in refs/ with remote ref shas


def fetch_refs(remote, remote_name = 'origin', local='.'):
    """
    Fetch references from a Git remote repository
    :param remote: <str> url of remote repository, _required_
    :param remote_name: <str> git name of remote repository, _default='origin'_
    :param local: <str> full path to local repository, _default='.'_
    :return entries: <TreeEntry> named tuples
    """
    # TODO: get remote's name from config file
    # from dulwich.config import ConfigFile
    # cnf = ConfigFile.from_path('./.git/config')
    # rmtname = cnf.get(('branch','master'),'remote')
    # **Fetch refs from remote**
    # correctly parse host path and create dulwich Client object from it
    client, host_path = get_transport_and_path(remote)
    # create a dulwich Repo object from path to local repo
    # TODO: check that repo exists, if not use Repo.init(local,mkdir=True)
    r = Repo(local)  # local repository
    gitdir = r.controldir()  # the .git/ folder
    objsto = r.object_store  # create a ObjectStore object from the local repo
    determine_wants = objsto.determine_wants_all  # built in dulwich function
    remote_refs = client.fetch(host_path, r, determine_wants, sys.stdout.write)

    # **Store refs fetched by dulwich**
    dulwich_refs = os.path.join(local, gitdir, DULWICH_REFS)
    with open(dulwich_refs, 'wb') as file:
        writer = csv.writer(file, delimiter=' ')
        for key, value in remote_refs.items():
            writer.writerow([key, value])

    # **save remote refs shas for future checkout**
    refsdir = os.path.join(local, gitdir, REFS)  # full path to ./git/refs
    remotesdir = os.path.join(refsdir, REMOTES)  # .git/refs/remotes
    thisremote = os.path.join(remotesdir, remote_name)  # path to remote folder
    ensure_dir_exists(thisremote)  # built in dulwich function
    # head branch ref
    if remote_refs.has_key('HEAD'):
        headref = remote_refs.pop('HEAD')  # sha of HEAD
        i_head = remote_refs.values().index(headref)  # index of head ref
        head_branch = remote_refs.keys()[i_head]  # name of head branch
        branch_key = head_branch.rsplit('/',1)[-1]  # branch
        head_file = os.path.join(thisremote, _branch_key)  # path to branch shas file
        with open(head_file, 'wb') as GitFile:
            write(branch_key)
    # remote branch refs
    for key, value in remote_refs.items():
        key = key.rsplit('/',1)[-1]  # get just the remote's branch
        reffile = os.path.join(thisremote, key)  # path to branch shas file
        with open(reffile, 'wb') as GitFile:
            write(value)

    return remote_refs
