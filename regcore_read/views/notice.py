from regcore import db
from regcore.responses import four_oh_four, success


def get(request, part_or_docnum, docnum):
    """ Find and return the notice with this docnum and part """
    part = part_or_docnum
    notice = db.Notices().get(doc_number=docnum, part=part)
    if notice:
        return success(notice)
    else:
        return four_oh_four()


def listing(request, part_or_docnum=None):
    """Find and return all notices"""
    part = part_or_docnum
    return success({
        'results': db.Notices().listing(part=part)
    })
