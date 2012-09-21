    import sys, os, csv
    from dulwich.repo import Repo
    from dulwich.client import get_transport_and_path
    from dulwich.file import ensure_dir_exists, GitFile
    
    LOCALPATH = 'c:\\path\\to\\repo'
    REMOTE = 'git@github.com:user/path'
    GITDIR = '.git'
    DULWICH_REFS = 'dulwich_refs'
    MYBRANCH = 'mybranch'
    
    repo = Repo.init(LOCALPATH, mkdir=True)
    client, host_path = get_transport_and_path(REMOTE)
    
    # Help on method fetch in module dulwich.client:
    # fetch(self, path, target, determine_wants=None, progress=None) unbound
    # dulwich.client.TCPGitClient method
    #   Fetch into a target repository.
    #   :param path: Path to fetch from
    #   :param target: Target repository to fetch into
    #   :param determine_wants: Optional function to determine what refs to fetch
    #   :param progress: Optional progress function
    #   :return: remote refs as dictionary
    
    refs = client.fetch(host_path, r, objsto.determine_wants_all, sys.stdout.write)
    
    # lets write these to a file, but we can fetch them again any time
    with open(os.path.join(repo.path, GITDIR, DULWICH_REFS), 'wb') as file:
        writer = csv.writer(file, delimiter=' ')
        for key, value in refs.items():
            writer.writerow([key, value])

    myref = refs[MYBRANCH]
    tree_id = repo[myref].tree
    #iterate over tree content, giving path and blob sha.
    for entry in repo.object_store.iter_tree_contents(tree_id):
        entry_in_path = entry.in_path(repo.path)
        ensure_dir_exists(os.path.split(entry_in_path.path)[0])
        file = GitFile(entry_in_path.path, 'wb')
        file.write(repo[entry.sha].data)
        file.close