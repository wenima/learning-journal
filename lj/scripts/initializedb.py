import os
import sys
import transaction
import datetime

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models.meta import Base
from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
    )
from ..models import Post


text_id0 = """I've operated on 2h of sleep today and it was very noticeable. Nick was sharp as always and pointed out that getting the last 4 chars of a string when you expect \r\n is actually not going to work because these are 2 chars. Off to a good start. While my fellow classmates were comparing against something that doesn't exist, I was wrestling with various tries of timeouts to determine if a client is still sending. Should I really care if the client is still sending? I used an immensely useful tactic some old timer gave me when I was fretting over not finding an email: > "If it's important, they'll send it again and then send you another mail asking if you read the previous two". But what sounded good on paper did not work so I decided today to full concentrate on the data structures and clean testing using fixtures.

But before that we rushed through the HTTP Protocol which needs to be absorbed fully as I expect this will be very central when doing Pyramid and Django. I was also looking for some modules/libraries as the wrapper around the socket object is low-level and close to C and so doesn't come with alot of things to help manage the connections.

The code review this morning was very helpful and it's all so clear if Nik is typing it up. Very much enjoyed the official appearance of fixtures. I used the capsys fixtures on the mailroom assignment to capture and ets sdtout. They are immensely useful.

Before I could get to testing we talked about Inheritance vs Composition and while abstract at first, it really makes sense to stay away from Inheritance, even if they are fine for smaller projects but it's just the style of programming and a way of thinking and one day, if that style prevails, large systems will be build with Inheritance and it will become immensely difficult to manage.

While it makes sense on paper to inherit from an Animal class when building a cat class and that cat class shares attributes of the Mammal class, the complex systems programmers are thrown into are not like that. Unless you are building a geneology website for your cat or whatever, a real programmer is more likely to find himself thrown into a codebase that is way more abstract: class FactoryManager extends Factory?? Exactly..

The concepts we fly through in the first part of the day can't really be learned, at least not on 2h of sleep until they are put into action. The issue I have right now is that my understanding of the concepts are lacking behind the course by about 2 days and I need to keep it at that so I can catchup on the weekend.

My partner was off to the races and I was happily sinking my teeth into testing today, first building out the tests for the to-be-programmed Stack and then refactoring the tests for the previous day's assignment. What I love about the stages of grasping a concept is that you can go back and see everthing clearer all of a sudden. Where you see a lengthy for loop you now see a list comprehension. Where you see anything that you think can be counted, you are eager to check if it's an iterable. And if not, make it into one!

Once the tests were written I went back to complete all the tests across Stack and Linked List and my goal was 100% .

On my way to that number I found few issues in the code and one pretty big issue that was missed and I was hoping I could beat any of the TAs before they reviewed it. No such luck unfortunately.

Having a solid test suite is so immensiley helpful in refactoring code. At one point I was close my goal but one of the TAs agreed with me, pytest was acting up and showing code as not tested allthough it clearly was entered and ran successfully. So reverted to a small trick so I could achieve my goal for the day.
"""

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

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    settings["sqlalchemy.url"] = os.environ["DATABASE_URL"]

    engine = get_engine(settings)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)

        model = Post(id=0,
            title="Goal: 100% Result: Win... (well, almost)",
            body=text_id0,
            creation_date=d.replace(day=14)
            )
        dbsession.add(model)
