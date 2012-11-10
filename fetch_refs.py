    import sys, os, csv
    from dulwich.repo import Repo
    from dulwich.client import get_transport_and_path
    from dulwich.file import ensure_dir_exists, GitFile
    
    DULWICH_REFS = 'dulwich_refs'
    
    # Help on method fetch in module dulwich.client:
    # fetch(self, path, target, determine_wants=None, progress=None) unbound
    # dulwich.client.TCPGitClient method
    #   Fetch into a target repository.
    #   :param path: Path to fetch from
    #   :param target: Target repository to fetch into
    #   :param determine_wants: Optional function to determine what refs to fetch
    #   :param progress: Optional progress function
    #   :return: remote refs as dictionary
    
def fetch_refs(remote, local='.', branch='master'):
    """
    """
    client, host_path = get_transport_and_path(remote)
    # TODO: check that repo exists, if not use Repo.init(local,mkdir=True)
    r = Repo(local)
    gitdir = r.controldir()
    objsto = r.object_store
    headtree = r['HEAD'].tree
    #treeiter = objsto.iter_tree_contents(headtree)
    determine_wants = objsto.determine_wants_all
    remote_refs = client.fetch(host_path, r, determine_wants,
                              sys.stdout.write)

    dulwich_refs = os.path.join(local, gitdir, DULWICH_REFS)
    with open(dulwich_refs, 'wb') as file:
        writer = csv.writer(file, delimiter=' ')
        for key, value in remote_refs.items():
            writer.writerow([key, value])

    myref = refs[branch]
    tree_id = repo[myref].tree
    #iterate over tree content, giving path and blob sha.
    for entry in repo.object_store.iter_tree_contents(tree_id):
        entry_in_path = entry.in_path(repo.path)
        ensure_dir_exists(os.path.split(entry_in_path.path)[0])
        file = GitFile(entry_in_path.path, 'wb')
        file.write(repo[entry.sha].data)
        file.close