import scrapy
from scrapy.spiders import CrawlSpider
from ..items import NewContext
class PositionSpider(scrapy.Spider):
    name = 'Position'
    start_urls = [
        #'http://www.people.com.cn/',
        #'http://finance.people.com.cn/',
        #'http://military.people.com.cn/',
        'http://house.people.com.cn/',
        'http://auto.people.com.cn/',
        #'http://finance.people.com.cn/n1/2019/1119/c1004-31461488.html',
        #'http://finance.people.com.cn/n1/2019/1118/c1004-31459976.html',
    ]
    
    url_list=[]
    def parse(self, response):
        marqueue=response.css('marquee a::attr(href)').getall()
        focus_list=response.css('div.focus_list ul li a::attr(href)').getall()
        news_box=response.css('div.news_box ul li a::attr(href)').getall()
        col_href=response.css('div.img_box.bgc_gray a::attr(href)').getall()
        hd_href=response.css('div.hdNews.clearfix div h5 a::attr(href)').getall()
        pages_href=response.css('div.page_n.clearfix a::attr(href)').getall()
        ph_list=response.css('ul.ph_list li a::attr(href)').getall()
        sum_href=marqueue + focus_list + news_box + col_href + hd_href + pages_href + ph_list
        self.url_list+=sum_href
        for u in self.url_list:
            yield response.follow(u,callback=self.next_parse)
            

        

    def next_parse(self, response):
        
        try:
                
            t=response.css('span#rwb_navpath a::text').getall()
            
            author=response.css('div.box01 div.fl a::text').get()
                           
            title=response.css('div.clearfix.w1000_320.text_title h1::text').get()
            
            text=response.css('div.box_con#rwb_zw p::text').getall()
            
            content=''.join(text)
            img=response.xpath('//img/@src').extract()[1:4]
            
            item=NewContext()
            item['image_urls']=img
            item['type']=type
            item['author']=author
            item['title']=title
            item['text']=content
            yield item
        except Exception:
            print('或许这页不是文章')
            return
        
    
       



''' #href=response.xpath('//body/div/a/@href').getall()
        marqueue=response.css('marquee a::attr(href)').getall()
        focus_list=response.css('div.focus_list ul li a::attr(href)').getall()
        news_box=response.css('div.news_box ul li a::attr(href)').getall()
        col_href=response.css('div.img_box.bgc_gray a::attr(href)').getall()
        hd_href=response.css('div.hdNews.clearfix div h5 a::attr(href)').getall()
        pages_href=response.css('div.page_n.clearfix a::attr(href)').getall()
        ph_list=response.css('ul.ph_list li a::attr(href)').getall()
        sum_href=marqueue + focus_list + news_box + col_href + hd_href + pages_href + ph_list
        self.url_list+=sum_href
        print(self.url_list)
        if self.url_list[self.i]!='':
            print("已执行一次")
            yield response.follow(self.url_list[self.i], callback=self.parse_detail)
            self.i+=1
            print(self.i)
    
    def parse_detail(self, response):  
            print('crawl detail_pages')
            t=response.css('span#rwb_navpath a::text').getall()
            print(t[-1])
            author=response.css('div.box01 div.fl a::text').get()
            print(author)               
            title=response.css('div.clearfix.w1000_320.text_title h1::text').get()
            print(title)
            text=response.css('div.box_con#rwb_zw p::text').getall()
            print(text)
            content=''.join(text)
            print(content)
            item=CrawlNewsItem()
            item['type']=type
            item['author']=author
            item['title']=title
            item['text']=content
            yield  item
                '''
                
            
               
       
'''rmw_nav=response.xpath('//body/div/div/div/nav/div/span/a/@href').getall()
           
            em_herf=response.xpath('//body/div/div/div/nav/div/div/em/a/@href').getall()
            
            section_herf=response.xpath('//body/div/div/div/section/div/a/@href').getall()
            print(section_herf)
            sum_href=rmw_nav+em_herf+section_herf
            url_list+=sum_href
        
            if url_list[i]!='':
                
                i+=1
                
                yield response.follow(url_list[i], callback=self.parse)
        except Exception:
            try:
                href=response.xpath('//body/div/a/@href').getall()
                marqueue=response.css('marquee a::attr(href)').getall()
                print(marqueue)
                focus_list=response.css('div.focus_list ul li a ').getall()
                news_box=response.css('div.news_box ul li a').getall()
                col_href=response.css('div.img_box.bgc_gray a').getall()
                hd_href=response.css('div.hdNews.clearfix div h5 a').getall()
                pages_href=response.css('div.page_n.clearfix a').getall()
                ph_list=response.css('ul.ph_list li a').getall()
                list_14=response.css('ul.list_14.mt15 li a').getall()
                sum_href=href + marqueue + focus_list + news_box + col_href + hd_href + pages_href + ph_list + list_14
                if url_list[i]!='':
                    i+=1
                    yield response.follow(url_list[i], callback=self.parse)
            
            except Exception:
                print()
                try:
                    
                    t=response.css('rwb_navpath a::text').getall()
                    type=t[-1]
                    author=response.css('div.f1 a::text').get()               
                    title=response.css('div.clearfix.w1000_320.text_title h1::text').get()
                    text=response.css('div.box_con#rwb_zw p:: text').getall()
                    content=''.join(text)
                    item=CrawlNewsItem()
                    item['type']=type
                    item['author']=author
                    item['title']=title
                    item['text']=content
                    if url_list[i]!='':
                        i+=1
                        print(item)
                        yield{
                            item,
                            response.follow(url_list[i], callback=self.parse)
                       
                        }
                except Exception:
                    yield response.follow(url_list[i], callback=self.parse)'''
       
                  
  
            