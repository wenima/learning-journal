def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('detail', '/detail/{id:\d+}')
    config.add_route('edit', '/edit/{id:\d+}')
    config.add_route('create', '/publish')
    config.add_route('login', '/login')
