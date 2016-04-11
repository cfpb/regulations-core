import json

from django.views.decorators.csrf import csrf_exempt

from regcore import db
from regcore.responses import success, user_error


@csrf_exempt
def add(request, part_or_docnum, docnum):
    """ Add the notice to the db """
    part = part_or_docnum

    try:
        notice = json.loads(request.body)
    except ValueError:
        return user_error('invalid format')

    db.Notices().put(docnum, part, notice)
    return success()

@csrf_exempt
def add_all(request, part_or_docnum):
    """ Add the notice for all applicable CFR parts, as specified in the
        notice body. """
    # NOTE: Be absolutely certain if you're PUTing /notice/1234-12345
    # that it actually does contain content for all the parts in cfr_parts.
    docnum = part_or_docnum

    try:
        notice = json.loads(request.body)
    except ValueError:
        return user_error('invalid format')

    # This supports old-style notices that apply to multiple CFR parts.
    cfr_parts = notice.get('cfr_parts', [])
    if 'cfr_part' in notice:
        cfr_parts.append(notice['cfr_part'])
    notice['cfr_parts'] = cfr_parts

    for cfr_part in cfr_parts:
        db.Notices().put(docnum, cfr_part, notice)

    return success()



