import dependencies

from nameko.rpc import rpc

class NewsService:

    name = 'news_service'

    database = dependencies.Database()

    @rpc
    def add_user(self, username, password):
        user = self.database.add_user(username, password)
        return user

    @rpc
    def get_user(self, username, password):
        user = self.database.get_user(username, password)
        return user
    
    @rpc
    def add_news(self, title, content, image):
        user = self.database.add_news(title, content, image)
        return user
    
    @rpc
    def edit_news(self, title, content, image):
        user = self.database.edit_news(title, content, image)
        return user
    
    @rpc
    def get_all_news(self):
        user = self.database.get_all_news()
        return user
    
    @rpc
    def get_news_by_id(self, uuid):
        user = self.database.get_news_by_id(uuid)
        return user
    
    @rpc
    def delete_news(self, uuid):
        user = self.database.delete_news(uuid)
        return user
    
    @rpc
    def download_file_by_id(self, uuid):
        user = self.database.download_file_by_id(uuid)
        return user