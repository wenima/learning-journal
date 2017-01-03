from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy.exc import DBAPIError
from pyramid.httpexceptions import HTTPFound
from ..models import Post
from ..security import check_credentials

@view_config(route_name='home', renderer='../templates/home.jinja2')
def home(request):
    try:
        query = request.dbsession.query(Post).all()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'entries': query}

@view_config(route_name="detail", renderer="../templates/detail.jinja2")
def detail_view(request):
    post_id = int(request.matchdict["id"])
    print(post_id)
    post = request.dbsession.query(Post).get(post_id)
    return {"post": post}

@view_config(route_name="edit", renderer="../templates/edit-post.jinja2")
def edit_view(request):
    post_id = int(request.matchdict["id"])
    post = request.dbsession.query(Post).get(post_id)
    return {"post": post}


@view_config(route_name='create', renderer="../templates/publish.jinja2")
def create_post(request):
    if request.method == "POST":
        title = request.POST["title"]
        body = request.POST["body"]
        creation_date = request.POST["creation_date"]
        new_post = Post(title=title, body=body, creation_date=creation_date)
        request.dbsession.add(new_post)
        return HTTPFound(request.route_url('home'))
    return {}

@view_config(route_name="login", renderer="../templates/login.jinja2")
def login_view(request):
    if request.POST:
        username = request.POST["username"]
        password = request.POST["password"]
        if check_credentials(username, password):
            return HTTPFound(request.route_url('home'))
    return {}


db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_lj_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
