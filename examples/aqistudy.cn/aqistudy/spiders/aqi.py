import scrapy
from lxml import etree
from xml.etree.ElementTree import tostring
from ..items import AqiItem


class AqiSpider(scrapy.Spider):
    name = 'aqi'
    allowed_domains = ['aqistudy.cn']
    start_urls = ['https://www.aqistudy.cn/historydata/']

    def parse(self, response):
        city_node_list = response.xpath('//div[@class="all"]/div[@class="bottom"]/ul//li/a')  # 获取城市月份节点

        for city_node in city_node_list[16:17]:  # 获取一个城市
            url = response.urljoin(city_node.xpath('./@href').get())
            city_name = city_node.xpath('./text()').get()
            # print(url, city_name)
            yield scrapy.Request(url=url, callback=self.parse_month_data, meta={"city_name": city_name})

    # 获取空气质量指数月统计历史数据，分析出日统计历史数据页面地址
    def parse_month_data(self, response):
        month_node_list = response.xpath('//ul[@class="unstyled1"]/li/a/@href').getall()  # 获取城市日节点
        for month_url in month_node_list:  # 获取12个月
            url = response.urljoin(month_url)
            yield scrapy.Request(url=url, callback=self.parse_day_data, meta={"city_name": response.meta['city_name']})

    def parse_day_data(self, response):
        # 分析数据
        first_table_tr = response.xpath("//table/tbody/tr[position() = 1]"
                                        "/*[local-name()='td' or local-name()='th']/text()")  # 获取随机数据表头，确定其索引
        table_tr_list = response.xpath('//table/tbody/tr[position() > 1]')  # 获取所有数据

        need_fields = {
            'day': "日期",
            'aqi': "AQI",
            'quality_level': "质量等级",
            'pm_2_5': 'PM2.5',
            'pm_10': 'PM10',
            'co': 'CO',
            'so2': 'SO2',
            'no2': 'NO2',
            'o3_8h': 'O3_8h'
        }

        reverse_need_fields = {v: k for k, v in need_fields.items()}  # 反转字典，将key -> value 互换

        # print(first_table_tr.getall())

        need_field_dict = {reverse_need_fields[table_th.get()]: index + 1 for index, table_th in
                           enumerate(first_table_tr)
                           if table_th.get() in need_fields.values()}  #

        # print(need_field_dict)

        for table_tr in table_tr_list:
            # tr = table_tr.get()

            yield AqiItem(
                city_name=response.meta['city_name'],
                day=table_tr.xpath('./td[%d]/text()' % need_field_dict['day']).get(),
                aqi=table_tr.xpath('./td[%d]/text()' % need_field_dict['aqi']).get(),
                quality_level=table_tr.xpath('./td[%d]//text()' % need_field_dict['quality_level']).get(),
                pm_2_5=table_tr.xpath('./td[%d]/text()' % need_field_dict['pm_2_5']).get(),
                pm_10=table_tr.xpath('./td[%d]/text()' % need_field_dict['pm_10']).get(),
                co=table_tr.xpath('./td[%d]/text()' % need_field_dict['co']).get(),
                so2=table_tr.xpath('./td[%d]/text()' % need_field_dict['so2']).get(),
                no2=table_tr.xpath('./td[%d]/text()' % need_field_dict['no2']).get(),
                o3_8h=table_tr.xpath('./td[%d]/text()' % need_field_dict['o3_8h']).get(),
            )
