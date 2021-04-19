import os
import tempfile

import pytest

from belvo_transactions import create_app, connection


@pytest.fixture
def app():
    db_fd, database = tempfile.mkstemp()
    app = create_app({'DATABASE': database})
    with app.app_context():
        connection.init_db()
    yield app

    os.close(db_fd)
    os.unlink(database)
