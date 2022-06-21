import json

from nameko.web.handlers import http
from werkzeug.wrappers import Response
from nameko.rpc import RpcProxy

from session import SessionProvider

class GatewayService:

    name = "gateway_service"

    news_access_rpc = RpcProxy('news_service')

    session_provider = SessionProvider()

    @http('POST', '/register')
    def add_user(self, request):
        data = request.json
        result = self.news_access_rpc.add_user(data['username'], data['password'])
        return result
    
    @http('POST', '/login')
    def get_user(self, request):
        data = request.json
        result = self.news_access_rpc.get_user(data['username'], data['password'])
        response = ""
        if result:
            session_id = self.session_provider.set_session(result)
            response = Response(str("Logged in as " + result[0]['username']))
            response.set_cookie('sessionID', session_id)
            return response
        else:
            response = Response(str("Account not found, please register!"))
            return response
    
    @http('POST', '/logout')
    def logout(self, request):
        cookies = request.cookies
        if cookies:
            session_data = self.session_provider.delete_session(cookies['sessionID'])
            response = Response('User Logged Out')
            return response
        else:
            response = Response('Currently Unable to Log Out')
            return response
        
    @http('POST', '/add')
    def add_news(self, request):
        cookies = request.cookies
        if cookies:
            data = request.json
            result = self.news_access_rpc.add_news(data['title'], data['content'], data['image'])
            return result
        else:
            response = Response("Log in required to add news! Please log in.")
            return response
    
    @http('POST', '/edit')
    def edit_news(self, request):
        cookies = request.cookies
        if cookies:
            data = request.json
            result = self.news_access_rpc.edit_news(data['title'], data['content'], data['image'])
            return result
        else:
            response = Response("Log in required to edit news! Please log in.")
            return response
        
    @http('POST', '/getall')
    def get_all_news(self, request):
        data = request.json
        result = self.news_access_rpc.get_all_news()
        return json.dumps(result)
    
    @http('POST', '/getbyid')
    def get_news_by_id(self, request):
        data = request.json
        result = self.news_access_rpc.get_news_by_id(data['id'])
        return json.dumps(result)
    
    @http('POST', '/delete')
    def delete_news(self, request):
        cookies = request.cookies
        if cookies:
            data = request.json
            result = self.news_access_rpc.delete_news(data['id'])
            return json.dumps(result)
        else:
            response = Response("Log in required to delete news! Please log in.")
            return response
        
    @http('POST', '/download')
    def download_file_by_id(self, request):
        data = request.json
        result = self.news_access_rpc.download_file_by_id(data['id'])
        return json.dumps(result)