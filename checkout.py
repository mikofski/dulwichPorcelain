from dulwich.repo import Repo
from dulwich.file import ensure_dir_exists, GitFile
import os


def checkout(repo_path='.', co_ref='HEAD'):
    """
    Checkout a reference from a Git repository
    :param repo_path: <str> path of repository
    :param co_ref: <str> name of checkout reference
    :return entries: <TreeEntry> named tuples
    """
    # TODO: try using index.build_index_from_tree
    repo = Repo(repo_path)
    obj_sto = repo.object_store
    # TODO: catch not a reference
    tree_id = repo[co_ref].tree
    # TODO: error out if unstaged or uncommited files
    tree_id = repo[ref].tree
    entries = []
    for entry in obj_sto.iter_tree_contents(tree_id):
        entry_in_path = entry.in_path(repo.path)
        path = os.path.split(entry_in_path.path)
        ensure_dir_exists(path[0])
        path = os.path.join(*path)
        with open(path, 'wb') as GitFile:
            write(repo[entry_in_path.sha].data)
        os.chmod(path, entry_in_path.mode)
        entries.append(entry)
    return entries
