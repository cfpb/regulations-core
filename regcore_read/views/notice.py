from regcore import db
from regcore.responses import four_oh_four, success


def get(request, part, docnum):
    """ Find and return the notice with this docnum and part """
    notice = db.Notices().get(document_number=docnum, cfr_part=part)
    if notice:
        return success(notice)
    else:
        return four_oh_four()


def listing(request, part=None):
    """Find and return all notices"""
    return success({
        'results': db.Notices().listing(part=part)
    })
