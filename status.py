def cmd_status(path):
    r = Repo(path)
    obj_sto = r.object_store
    tree_id = r['HEAD'].tree
    treeIter = obj_sto.iter_tree_contents(tree_id)
    names = []
    for root, dirs, files in os.walk(r.path):
        if '.git' in dirs:
            dirs.remove('.git')  # don't visit .git directories
        if root == '.':
            names += [wc for wc in files]
        else:
            path = root.rsplit(os.path.sep)[1:]
            path = os.path.join(*path)
            names += [os.path.join(path, wc) for wc in files]
    def lookup_entry(name):
        if name not in names:
            raise(KeyError)
        else:
            name = os.path.join(r.path, name)
            with open(name,'rb') as GitFile:
                data = GitFile.read()
                s = sha1()
                s.update("blob %u\0" % len(data))
                s.update(data)
            return (s.hexdigest() , os.stat(name).st_mode)
    result = changes_from_tree(names, lookup_entry, obj_sto, tree_id,
                               want_unchanged=False)
    was_removed = ([(name[0], mode[0], sha[0]) for (name, mode, sha) in result
                   if name[0] is not None and name[1] is None])
    added_files = ([(name[1], mode[1], sha[1]) for (name, mode, sha) in result
                   if name[0] is None and name[1] is not None])
    was_changed = ([(name, mode, sha) for (name, mode, sha) in result if
                   name[0] is not None and name[1] is not None])
    # Was removed
    print '# On branch <TODO>'
    if was_removed:
        print '# Changes to be committed:'
        print '#   (use "git reset HEAD <file>..." to unstage)'
        print '#'
        for (name, mode, sha) in was_removed:
            print '#       deleted:    %s' % name
        print '#'
    if added_files:
        print '# Untracked files:'
        print '#   (use "git add <file>..." to include in what will be committed)'
        print '#'
        for (name, mode, sha) in added_files:
            print '#       new file:   %s' % name
        print '#'
    if was_changed:
        print '# Untracked files:'
        print '#   (use "git add <file>..." to include in what will be committed)'
        print '#'
        for (name, mode, sha) in was_changed:
            print '#       modified:   %s' % name[0]
        print '#'