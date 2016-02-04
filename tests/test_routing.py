"""tests/test_output_format.py

Tests that the hug routing functionality works as expected

Copyright (C) 2015 Timothy Edmund Crosley

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and
to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

"""
import hug
from hug.routing import (APIRouter, CLIRouter, ExceptionRouter, HTTPRouter,
                         NotFoundRouter, Router, SinkRouter, StaticRouter, URLRouter)

api = hug.API(__name__)


class TestRouter(object):
    '''A collection of tests to ensure the base Router object works as expected'''
    route = Router(transform='transform', output='output')

    def test_init(self):
        '''Test to ensure the route instanciates as expected'''
        assert self.route.route['transform'] == 'transform'
        assert self.route.route['output'] == 'output'
        assert not 'api' in self.route.route

    def test_output(self):
        '''Test to ensure modifying the output argument has the desired effect'''
        new_route = self.route.output('test data', transform='transformed')
        assert new_route != self.route
        assert new_route.route['output'] == 'test data'
        assert new_route.route['transform'] == 'transformed'

    def test_transform(self):
        '''Test to ensure changing the transformation on the fly works as expected'''
        new_route = self.route.transform('transformed')
        assert new_route != self.route
        assert new_route.route['transform'] == 'transformed'

    def test_api(self):
        '''Test to ensure changing the API associated with the route works as expected'''
        new_route = self.route.api('new')
        assert new_route != self.route
        assert new_route.route['api'] == 'new'

    def test_where(self):
        '''Test to ensure `where` can be used to replace all arguments on the fly'''
        new_route = self.route.where(transform='transformer', output='outputter')
        assert new_route != self.route
        assert new_route.route['output'] == 'outputter'
        assert new_route.route['transform'] == 'transformer'


class TestCLIRouter(TestRouter):
    '''A collection of tests to ensure the CLIRouter object works as expected'''
    route = CLIRouter(name='cli', version=1, doc='Hi there!', transform='transform', output='output')

    def test_name(self):
        '''Test to ensure the name can be replaced on the fly'''
        new_route = self.route.name('new name')
        assert new_route != self.route
        assert new_route.route['name'] == 'new name'
        assert new_route.route['transform'] == 'transform'
        assert new_route.route['output'] == 'output'

    def test_version(self):
        '''Test to ensure the version can be replaced on the fly'''
        new_route = self.route.version(2)
        assert new_route != self.route
        assert new_route.route['version'] == 2
        assert new_route.route['transform'] == 'transform'
        assert new_route.route['output'] == 'output'

    def test_doc(self):
        '''Test to ensure the documentation can be replaced on the fly'''
        new_route = self.route.doc('FAQ')
        assert new_route != self.route
        assert new_route.route['doc'] == 'FAQ'
        assert new_route.route['transform'] == 'transform'
        assert new_route.route['output'] == 'output'


class TestHTTPRouter(TestRouter):
    '''Collection of tests to ensure the base HTTPRouter object works as expected'''
    route = HTTPRouter(output='output', versions=(1, ), parse_body=False, transform='transform', requires=('love', ),
                       parameters=('one', ), defaults={'one': 'value'}, status=200)

    def test_versions(self):
        '''Test to ensure the supported versions can be replaced on the fly'''
        assert self.route.versions(4).route['versions'] == (4, )

    def test_parse_body(self):
        '''Test to ensure the parsing body flag be flipped on the fly'''
        assert self.route.parse_body().route['parse_body'] == True
        assert not 'parse_body' in self.route.parse_body(False).route

    def test_requires(self):
        '''Test to ensure requirements can be added on the fly'''
        assert self.route.requires(('values', )).route['requires'] == ('love', 'values')

    def test_parameters(self):
        '''Test to ensure the parameters can be replaced on the fly'''
        assert self.route.parameters(('one', 'two')).route['parameters'] == ('one', 'two')

    def test_defaults(self):
        '''Test to ensure the defaults can be replaced on the fly'''
        assert self.route.defaults({'one': 'three'}).route['defaults'] == {'one': 'three'}

    def test_status(self):
        '''Test to ensure the default status can be changed on the fly'''
        assert self.route.set_status(500).route['status'] == 500

    def test_on_invalid(self):
        '''Test to ensure on_invalid handler can be changed on the fly'''
        assert self.route.on_invalid(str).route['on_invalid'] == str

    def test_output_invalid(self):
        '''Test to ensure output_invalid handler can be changed on the fly'''
        assert self.route.output_invalid(hug.output_format.json).route['output_invalid'] == hug.output_format.json

    def test_validate(self):
        '''Test to ensure overriding the secondary validation method works as expected'''
        assert self.route.validate(str).route['validate'] == str


class TestStaticRouter(object):
    '''Test to ensure that the static router sets up routes correctly'''
    route = StaticRouter("/here")
    route2 = StaticRouter(("/here", "/there"), 'api')

    def test_init(self):
        '''Test to ensure the route instanciates as expected'''
        assert self.route.route['urls'] == ("/here", )
        assert self.route2.route['urls'] == ("/here", "/there")
        assert self.route2.route['api'] == 'api'


class TestSinkRouter(TestHTTPRouter):
    '''Collection of tests to ensure that the SinkRouter works as expected'''
    route = SinkRouter(output='output', versions=(1, ), parse_body=False, transform='transform',
                       requires=('love', ), parameters=('one', ), defaults={'one': 'value'})


class TestNotFoundRouter(TestHTTPRouter):
    '''Collection of tests to ensure the NotFoundRouter object works as expected'''
    route = NotFoundRouter(output='output', versions=(1, ), parse_body=False, transform='transform',
                           requires=('love', ), parameters=('one', ), defaults={'one': 'value'})


class TestExceptionRouter(TestHTTPRouter):
    '''Collection of tests to ensure the ExceptionRouter object works as expected'''
    route = ExceptionRouter(Exception, output='output', versions=(1, ), parse_body=False, transform='transform',
                            requires=('love', ), parameters=('one', ), defaults={'one': 'value'})


class TestURLRouter(TestHTTPRouter):
    '''Collection of tests to ensure the URLRouter object works as expected'''
    route = URLRouter('/here', transform='transform', output='output', requires=('love', ))

    def test_urls(self):
        '''Test to ensure the url routes can be replaced on the fly'''
        assert self.route.urls('/there').route['urls'] == ('/there', )

    def test_accept(self):
        '''Test to ensure the accept HTTP METHODs can be replaced on the fly'''
        assert self.route.accept('GET').route['accept'] == ('GET', )

    def test_get(self):
        '''Test to ensure the HTTP METHOD can be set to just GET on the fly'''
        assert self.route.get().route['accept'] == ('GET', )

    def test_delete(self):
        '''Test to ensure the HTTP METHOD can be set to just DELETE on the fly'''
        assert self.route.delete().route['accept'] == ('DELETE', )

    def test_post(self):
        '''Test to ensure the HTTP METHOD can be set to just POST on the fly'''
        assert self.route.post().route['accept'] == ('POST', )

    def test_put(self):
        '''Test to ensure the HTTP METHOD can be set to just PUT on the fly'''
        assert self.route.put().route['accept'] == ('PUT', )

    def test_trace(self):
        '''Test to ensure the HTTP METHOD can be set to just TRACE on the fly'''
        assert self.route.trace().route['accept'] == ('TRACE', )

    def test_patch(self):
        '''Test to ensure the HTTP METHOD can be set to just PATCH on the fly'''
        assert self.route.patch().route['accept'] == ('PATCH', )

    def test_options(self):
        '''Test to ensure the HTTP METHOD can be set to just OPTIONS on the fly'''
        assert self.route.options().route['accept'] == ('OPTIONS', )

    def test_head(self):
        '''Test to ensure the HTTP METHOD can be set to just HEAD on the fly'''
        assert self.route.head().route['accept'] == ('HEAD', )

    def test_connect(self):
        '''Test to ensure the HTTP METHOD can be set to just CONNECT on the fly'''
        assert self.route.connect().route['accept'] == ('CONNECT', )

    def test_call(self):
        '''Test to ensure the HTTP METHOD can be set to accept all on the fly'''
        assert self.route.call().route['accept'] == hug.HTTP_METHODS

    def test_examples(self):
        '''Test to ensure examples can be modified on the fly'''
        assert self.route.examples('none').route['examples'] == ('none', )

    def test_prefixes(self):
        '''Test to ensure adding prefixes works as expected'''
        assert self.route.prefixes('/js/').route['prefixes'] == ('/js/', )

    def test_suffixes(self):
        '''Test to ensure setting suffixes works as expected'''
        assert self.route.suffixes('.js', '.xml').route['suffixes'] == ('.js', '.xml')

    def test_response_headers(self):
        '''Test to ensure it's possible to switch out response headers for URL routes on the fly'''
        assert self.route.response_headers({'one': 'two'}).route['response_headers'] == {'one': 'two'}

    def test_add_response_headers(self):
        '''Test to ensure it's possible to add headers on the fly'''
        route = self.route.response_headers({'one': 'two'})
        assert route.route['response_headers'] == {'one': 'two'}
        assert route.add_response_headers({'two': 'three'}).route['response_headers'] == {'one': 'two', 'two': 'three'}

    def test_cache(self):
        '''Test to ensure it's easy to add a cache header on the fly'''
        assert self.route.cache().route['response_headers']['cache-control'] == 'public, max-age=31536000'

    def test_allow_origins(self):
        '''Test to ensure it's easy to expose route to other resources'''
        assert self.route.allow_origins().route['response_headers']['Access-Control-Allow-Origin'] == '*'
        test_headers = self.route.allow_origins('google.com', methods=('GET', 'POST')).route['response_headers']
        assert test_headers['Access-Control-Allow-Origin'] == 'google.com'
        assert test_headers['Access-Control-Allow-Methods'] == 'GET, POST'


class TestAPIRouter(object):
    '''Test to ensure the API router enables easily reusing all other routing types while routing to an API'''
    router = APIRouter(__name__)

    def test_route_url(self):
        '''Test to ensure you can dynamically create a URL route attached to a hug API'''
        assert self.router.urls('/hi/').route == URLRouter('/hi/', api=api).route

    def test_not_found(self):
        '''Test to ensure you can dynamically create a Not Found route attached to a hug API'''
        assert self.router.not_found().route == NotFoundRouter(api=api).route

    def test_static(self):
        '''Test to ensure you can dynamically create a static route attached to a hug API'''
        assert self.router.static().route == StaticRouter(api=api).route

    def test_sink(self):
        '''Test to ensure you can dynamically create a sink route attached to a hug API'''
        assert self.router.sink().route == SinkRouter(api=api).route

    def test_exceptions(self):
        '''Test to ensure you can dynamically create an Exception route attached to a hug API'''
        assert self.router.exceptions().route == ExceptionRouter(api=api).route

    def test_cli(self):
        '''Test to ensure you can dynamically create a CLI route attached to a hug API'''
        assert self.router.cli().route == CLIRouter(api=api).route