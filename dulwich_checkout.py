from dulwich.repo import Repo
from dulwich.file import ensure_dir_exists, GitFile
import os
import sys


def checkout(repo_path='.', co_ref='HEAD'):
    """
        Checkout a reference from a Git repository
        :param repo_path: <str> path of repository
        :param co_ref: <str> name of checkout reference
        :return: None
    """
    repo = Repo(repo_path)
    obj_sto = repo.object_store
    tree_id = repo['HEAD'].tree

    for entry in obj_sto.iter_tree_contents(tree_id):
        entry_in_path = entry.in_path(repo.path)
        path = os.path.split(entry_in_path.path)
        ensure_dir_exists(path[0])
        print 'creating %s in %s' % path
        path = os.path.join(*path)
        git_file = GitFile(path, 'wb')
        git_file.write(repo.get_blob(entry.sha).data)
        git_file.close()
        os.chmod(path, entry_in_path.mode)
