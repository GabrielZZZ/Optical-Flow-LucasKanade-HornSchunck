from . import Path

def getimgfiles(stem):
    stem = Path(stem).expanduser()
    path = stem.parent
    name = stem.name
    exts = ['.ppm','.bmp','.png','.jpg']
    for ext in exts:
        flist = sorted(path.glob(name+'.*'+ext))
        if flist:
            break

    if not flist:
        raise FileNotFoundError('no files found with {}.*{}'.format(stem,ext))

    print('analyzing {} files {}.*{}'.format(len(flist),stem,ext))

    return flist,ext