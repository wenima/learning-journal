import pytest
import transaction

from pyramid import testing

from ..models import (
    MyModel,
    get_engine,
    get_session_factory,
    get_tm_session,
)
from ..models.meta import Base


@pytest.fixture(scope="session") #set up a SQL DB for the entire testing session.
def sqlengine(request):
    config = testing.setUp(settings={
        'sqlalchemy.url': 'sqlite:///:memory:'
    })
    config.include("..models")
    settings = config.get_settings()
    engine = get_engine(settings)
    Base.metadata.create_all(engine)

    def teardown():
        testing.tearDown()
        transaction.abort()
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return engine


@pytest.fixture(scope="function")
def new_session(sqlengine, request):
    session_factory = get_session_factory(sqlengine)
    session = get_tm_session(session_factory, transaction.manager)

    def teardown():
        transaction.abort()

    request.addfinalizer(teardown)
    return session


def test_model_gets_added(new_session):
    assert len(new_session.query(MyModel).all()) == 0
    model = MyModel(name="Bob", value=42)
    new_session.add(model)
    new_session.flush()
    assert len(new_session.query(MyModel).all()) == 1

def dummy_http_request(new_session):
    return testing.DummyRequest()


def test_my_view(new_session):
    from ..views.default import my_view

    new_session.add(MyModel(name="one", value=1))
    new_session.flush() # stages changes to be committed to the DB

    http_request = dummy_request(new_session)
    result = my_view(http_request) # views commit changes to the DB
    assert result["one"].name == "one"
