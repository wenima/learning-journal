import pytest
import transaction

from pyramid import testing

from .models import Post, get_tm_session
from .models.meta import Base
import random
import datetime


ENTRIES = [
    {"title" : "Today I learned...", "id": 1, "creation_date": "15",
    "body": """more about fixtures which I find super helpful. I started using the capsys fixture for the mailroom program and really got interested in using it more. Glad to know about scope now, it makes immediate sense.

    Also it was useful to learn about class methods, they don't go through the instance for lookup but go directly to the class. I don't have a good use case yet that I can think of but I'm sure it will present itself soon.

    The most useful thing I learned as that super classes work differently in Python where the child determines the order of the tree and a class might get called that is not a parent of the immediate parent of the child using the method resolution order.

    Today we impleted the doubly linked list which I got to a bit late as I was refactoring the tests for the linked list first while my partner did a great job in mapping out the testing. He wrote the first 10 tests, I wrote the classes/function and when I was 100% complete on tests, I fetched the next round of tests. We need to do a better job at actually reading the assignment though as the README was not in place and it actually required a paragraph about when to use doubly linked list vs linked list. It's a time consuming job to get that readme right.

    After coding up the initial server by myself 2 days ago until late night, server didn't get much love today as I went to PuPPy meetup where one of the co founders from Kitt.AI gave a presentation. After watching "Her" I was already mind blown and it was fascinating to really see the vision of interacting with bots come to realization. Very fascinating field that I would like to get into as I'm very passionate about effective workflows and bots offer a solution.
"""},
    {"title" : "Night and Day", "id": 2, "creation_date": "16",
    "body": """Today in class I didn't learn much, we literally just read through 2 paragraphs of concurrency and I know as much about it as I knew before the class. That it exists and there are different ways to go about solving it and none is perfect. Ok.

    Whenever some topic makes an appearance that is distinctively different to Java I get interested so was trying to absorb the concept of properties that can be used in a declarative style. The problem is that there is so much to do in the assignments that all of the concepts I would like to think about and work into my code go right out the door so other than hearing about them, I again, didn't really learn anything.

    I did learn somthing by watching the video: "Stop writing classes" which was entertaining and informative and it had great takeaways. Don't use classnames for taxonomy, don't build something because you thinkg you might need it in the future, if a class has 2 methods, one of them being init, it shouldn't be a class. The Q&A at the end of the video showed though that it's not all black&white. I have to explore more on the concepts of storing globals in a class.

    Assignments were night and day. Everthing clicked on the data structure assignment wen we blazed right through it allthough we started with a great example of why not to mutate things. I agreed to take an easy approach in how to pass in the iterable and my partner found a method to reverse a list but it also mutates it in place which now broke the tests. Cost us a good 30m to figure it out. So mutate things if you have lots of time is the takeaway. Python gives you the ability to alwasy return something and work with that return for a reason.

    Server assignment was polar opposite experience. Progress came to a screeching halt and I feel like I'm not even speaking the same language. Sitting next to each other but not saying even telling the other person which file is being changed/pushed/etc just frustrates me. There probably is a good portion of my inability to explain but there are clearly other factors as well.

    Missing sleep def got to me today. I couldn't figure out why my gist wasn't working and all I did was that I forgot to unpack the tuple by missing a * and I also got frustrated towards the end of the server coding which I consider to be a fail
"""},
    {"title" : "Today I learned..", "id": 3, "creation_date": "17",
    "body": """today I learned that I still struggle to write good, workin code in a speedy manner but it went better than the other Gist coding challenges.

    the whiteboard challenge was really fun, I enjoy drawing out solutions but didn't have time to finish the actual code but will return to that.

    My partner and I got on the same page and we made good progress on the server assignment but it's still uphill."""}
]



@pytest.fixture(scope="session")
def configuration(request):
    """Set up a Configurator instance.

    This Configurator instance sets up a pointer to the location of the
        database.
    It also includes the models from your app's model package.
    Finally it tears everything down, including the in-memory SQLite database.

    This configuration will persist for the entire duration of your PyTest run.
    """
    config = testing.setUp(settings={
        'sqlalchemy.url': 'sqlite:///:memory:'
    })
    config.include(".models")

    def teardown():
        testing.tearDown()

    request.addfinalizer(teardown)
    return config


@pytest.fixture(scope="function")
def db_session(configuration, request):
    """Create a session for interacting with the test database.

    This uses the dbsession_factory on the configurator instance to create a
    new database session. It binds that session to the available engine
    and returns a new session for every call of the dummy_request object.
    """
    SessionFactory = configuration.registry["dbsession_factory"]
    session = SessionFactory()
    engine = session.bind
    Base.metadata.create_all(engine)

    def teardown():
        session.transaction.rollback()

    request.addfinalizer(teardown)
    return session

# def test_model_gets_added(new_session):
#     assert len(new_session.query(MyModel).all()) == 0
#     model = MyModel(name="Bob", value=42)
#     new_session.add(model)
#     new_session.flush()
#     assert len(new_session.query(MyModel).all()) == 1
#
# def dummy_http_request(new_session):
#     return testing.DummyRequest()
#
#
# def test_my_view(new_session):
#     from .views.default import my_view
#
#     new_session.add(MyModel(name="one", value=1))
#     new_session.flush() # stages changes to be committed to the DB
#
#     http_request = dummy_request(new_session)
#     result = my_view(http_request) # views commit changes to the DB
#     assert result["one"].name == "one"


#------
# def new_entry_is_added(new_session):
#     """Test existing entries in a dict are saved into a database"""
#     new_session.add_all(ENTRIES)
#     query = new_session.query(ENTRIES).all()
#     assert len(query) == len(ENTRIES)

def test_model_gets_added(db_session):
    assert len(db_session.query(Post).all()) == 0
    model = Post(id=1, title='Test entry', body='some random text', creation_date=datetime.date.today())
    db_session.add(model)
    assert len(db_session.query(Post).all()) == 1
