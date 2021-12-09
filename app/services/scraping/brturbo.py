import scrapy
from scrapy import crawler
from scrapy.crawler import CrawlerProcess
from scrapy.utils.misc import warn_on_generator_with_return_value


def url_scraper(plataforma, user):
    return f"https://cod.tracker.gg/warzone/profile/atvi/h-eid_elnems%237782159/details"


class Warzone(scrapy.Item):
    username = scrapy.Field()
    platform = scrapy.Field()
    views = scrapy.Field()
    img_level = scrapy.Field()
    level = scrapy.Field()
    status_level = scrapy.Field()
    avatar = scrapy.Field()
    playtime = scrapy.Field()
    wins = scrapy.Field()
    top5 = scrapy.Field()
    kd_ratio = scrapy.Field()
    damage_game = scrapy.Field()
    top10 = scrapy.Field()
    top25 = scrapy.Field()
    kills = scrapy.Field()
    deaths = scrapy.Field()
    downs = scrapy.Field()
    avg_life = scrapy.Field()
    score = scrapy.Field()
    score_min = scrapy.Field()
    score_game = scrapy.Field()
    cash = scrapy.Field()
    contracts = scrapy.Field()
    win_percentage = scrapy.Field()
    damage_done_7_days = scrapy.Field()
    damage_game_7_days = scrapy.Field()
    damage_min_7_days = scrapy.Field()
    kills_7_days = scrapy.Field()
    kills_game_7_day = scrapy.Field()
    kd_ratio_7_days = scrapy.Field()
    headshot_percentage = scrapy.Field()
    score_game_7_days = scrapy.Field()
    score_min_7_days = scrapy.Field()


class Brturbo(scrapy.Spider):
    name = "brturbo"
    start_urls = []

    # save json
    # custom_settings = {
    #     "FEED_URI": "warzone.json",
    #     "CLOSESPIDER_TIMEOUT": 15,
    # }

    def __init__(self, category="", **kwargs):
        super().__init__(**kwargs)
        self.start_urls.append(category)

    def parse(self, response):
        dados = Warzone()
        warzone = response.xpath('//span[@class="value"]/text()').getall()

        dados["username"] = response.css("span.trn-ign__username::text").get()
        dados["img_level"] = response.css(".level-progression img").xpath("@src").get()
        dados["level"] = response.css(".level-progression__suptext::text").get()
        dados["status_level"] = response.css(".level-progression__text::text").get()
        dados["views"] = response.css(".ph-details__subtitle span span::text").get()
        dados["platform"] = response.css("svg.platform-icon").xpath("@class").get()[19:]
        dados["avatar"] = response.css(".ph-avatar__image::attr(src)").get()
        dados["playtime"] = response.css("span.playtime::text").get().strip()[:-10]
        dados["wins"] = warzone[0]
        dados["top5"] = warzone[1]
        dados["kd_ratio"] = warzone[2]
        dados["damage_game"] = warzone[3]
        dados["top10"] = warzone[4]
        dados["top25"] = warzone[5]
        dados["kills"] = warzone[6]
        dados["deaths"] = warzone[7]
        dados["downs"] = warzone[8]
        dados["avg_life"] = warzone[9]
        dados["score"] = warzone[10]
        dados["score_min"] = warzone[11]
        dados["score_game"] = warzone[12]
        dados["cash"] = warzone[13]
        dados["contracts"] = warzone[14]
        dados["win_percentage"] = warzone[15]
        dados["damage_done_7_days"] = warzone[16]
        dados["damage_game_7_days"] = warzone[17]
        dados["damage_min_7_days"] = warzone[18]
        dados["kills_7_days"] = warzone[19]
        dados["kills_game_7_day"] = warzone[20]
        dados["kd_ratio_7_days"] = warzone[21]
        dados["headshot_percentage"] = warzone[22]
        dados["score_game_7_days"] = warzone[23]
        dados["score_min_7_days"] = warzone[24]

        yield dados


# if __name__=='__main__':
#     process = CrawlerProcess()
#     process.crawl(Brturbo)
#     process.start()
