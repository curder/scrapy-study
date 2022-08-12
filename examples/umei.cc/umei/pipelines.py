import scrapy
from scrapy.pipelines.images import ImagesPipeline


class UmeiPipeline(ImagesPipeline):
    """自定义图片下载器, 添加资源ID作为文件夹保存图片"""

    def get_media_requests(self, item, info):
        """发生图片下载请求"""
        yield scrapy.Request(item["image_url"], meta={"path": item['path']})  # 继续传递图片存储路径

    def file_path(self, request, response=None, info=None, *, item=None):
        """自定义图片保存路径"""
        return request.meta['path']
