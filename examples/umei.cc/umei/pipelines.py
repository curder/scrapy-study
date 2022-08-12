import scrapy
import hashlib
from scrapy.utils.python import to_bytes
from scrapy.pipelines.images import ImagesPipeline


class UmeiPipeline(ImagesPipeline):
    """自定义图片下载器, 添加资源ID作为文件夹保存图片"""

    def get_media_requests(self, item, info):
        """发生图片下载请求"""
        yield scrapy.Request(item["image_url"], meta={"id": item['id']})  # 继续传递页面ID

    def file_path(self, request, response=None, info=None, *, item=None):
        """自定义图片保存路径, 以页面ID作为文件夹保存"""
        id = request.meta['id']
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()

        return f'origin/{id}/{image_guid}.jpg'
