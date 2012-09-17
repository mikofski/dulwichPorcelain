from dulwich.repo import Repo
from dulwich.file import ensure_dir_exists, GitFile
import os


def checkout(args):
    """
        Checkout a reference from a Git repository.
        usage: dulwich checkout [--verbose] [REF]
    """
    opts, args = getopt(args, "", ["verbose"])
    opts = dict(opts)
    if len(args) > 0:
        ref = args.pop(0)
    else:
        ref = 'HEAD'
    # TODO: error out if unstaged or uncommited files
    repo = Repo('.')
    obj_sto = repo.object_store
    tree_id = repo[ref].tree
    for entry in obj_sto.iter_tree_contents(tree_id):
        entry_in_path = entry.in_path(repo.path)
        path = os.path.split(entry_in_path.path)
        ensure_dir_exists(path[0])
        if opts["verbose"]
            print 'creating %s in %s' % path
        path = os.path.join(*path)
        git_file = GitFile(path, 'wb')
        git_file.write(repo[entry_in_path.sha].data)
        git_file.close()
        os.chmod(path, entry_in_path.mode)
