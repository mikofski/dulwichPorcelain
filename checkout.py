from dulwich.repo import Repo
from dulwich.index import build_index_from_tree


def checkout(repo_path='.', co_ref='HEAD'):
    """
    Checkout a reference from a Git repository
    :param repo_path: <str> path of repository
    :param co_ref: <str> name of checkout reference
    :return entries: <TreeEntry> list of named tuples
    """
    # TODO: add all checkout options
    repo = Repo(repo_path)
    indexfile = repo.index_path()
    obj_sto = repo.object_store
    # TODO: catch if not a reference
    tree_id = repo[co_ref].tree
    # TODO: error out if unstaged or uncommited files
    build_index_from_tree(repo_path,indexfile,obj_sto,tree_id)
    return [obj_sto.iter_tree_contents(tree_id)]
