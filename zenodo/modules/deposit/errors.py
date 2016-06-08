# -*- coding: utf-8 -*-
#
# This file is part of Zenodo.
# Copyright (C) 2016 CERN.
#
# Zenodo is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Zenodo is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Zenodo; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Deposit errors."""

from __future__ import absolute_import, print_function

import json

from flask_babelex import gettext as _
from invenio_rest.errors import FieldError, RESTValidationError


class MissingFilesError(RESTValidationError):
    """Error for when no files have been provided."""

    errors = [
        FieldError(None, _('Minimum one file must be provided.'), code=10)
    ]


class MarshmallowErrors(RESTValidationError):
    """Marshmallow validation errors."""

    def __init__(self, errors):
        """Store marshmallow errors."""
        self.errors = errors
        super(MarshmallowErrors, self).__init__()

    @staticmethod
    def iter_errors(errors):
        """Iterator over marshmallow errors."""
        for field, error in errors.items():
            if isinstance(error, list):
                yield dict(field=field, message=' '.join(error))
            elif isinstance(error, dict):
                if '_schema' in error:
                    yield dict(field=field, message=error['_schema'][0])

    def get_body(self, environ=None):
        """Get the request body."""
        body = dict(
            status=self.code,
            message=self.get_description(environ),
        )

        if self.errors:
            body['errors'] = list(self.iter_errors(self.errors))

        return json.dumps(body)
