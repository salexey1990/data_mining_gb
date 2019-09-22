# -*- coding: utf-8 -*-
import re
import json
import scrapy
from scrapy.http import HtmlResponse
from urllib.parse import urlencode, urljoin
from copy import deepcopy

from jobparser.items import InstagramItem


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    graphql_url = 'https://www.instagram.com/graphql/query/?'
    allowed_domains = ['instagram.com']
    start_urls = ['http://instagram.com/']
    variables_base = {'fetch_mutual': 'false', "include_reel": 'true', "first": 100}
    item = {}

    def __init__(self, user_links, login, pswrd, *args, **kwargs):
        self.user_links = user_links
        self.login = login
        self.pswrd = pswrd
        self.query_feed_hash = '58b6785bea111c67129decbe6a448951'
        self.query_like_hash = 'd5d763b1e2acf209d62d22d184488e57'
        self.query_comment_hash = '97b41c52301f77ce508f55e66d17620e'
        super().__init__(*args, *kwargs)

    def parse(self, response: HtmlResponse):
        csrf_token = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            'https://www.instagram.com/accounts/login/ajax/',
            method='POST',
            callback=self.parse_users,
            formdata={'username': self.login, 'password': self.pswrd},
            headers={'X-CSRFToken': csrf_token}
        )

    def parse_users(self, response: HtmlResponse):
        j_body = json.loads(response.body)
        if j_body.get('authenticated'):
            for user in self.user_links:
                yield response.follow(urljoin(self.start_urls[0], user),
                                      callback=self.parse_user,
                                      cb_kwargs={'user': user})

    def parse_user(self, response: HtmlResponse, user):
        user_id = self.fetch_user_id(response.text, user)
        user_vars = deepcopy(self.variables_base)
        user_vars.update({'id': user_id})
        yield response.follow(self.make_graphql_url(user_vars, query_hash=self.query_feed_hash),
                              callback=self.parse_posts,
                              cb_kwargs={'user': user})

    def parse_posts(self, response: HtmlResponse, user):
        data = json.loads(response.body)
        likes_vars = {"shortcode":"B2oY9vPnmxV", "include_reel":"true"}
        comment_vars = {"shortcode":"B2oY9vPnmxV"}
        codes = [item.get('node').get('shortcode') for item in data.get('data').get('user').get('edge_owner_to_timeline_media').get('edges')]

        for code in codes:
            comment_vars.update({'shortcode': code})
            likes_vars.update({'shortcode': code})
            yield response.follow(self.make_graphql_url({'variables':json.dumps(likes_vars)}, query_hash=self.query_like_hash), callback=self.parse_likes,
                                  cb_kwargs={'vars': likes_vars, 'code': code, 'user': user})

            yield response.follow(self.make_graphql_url({'variables':json.dumps(comment_vars)}, query_hash=self.query_comment_hash), callback=self.parse_comments,
                                  cb_kwargs={'vars': comment_vars, 'code': code, 'user': user})

    # def parse_post(self, response: HtmlResponse, vars, user):
    #     data = json.loads(response.body)
    #     commented_users = [item.get('node').get('owner') for item in data.get('data').get('shortcode_media').get('edge_media_to_parent_comment').get('edges')]
    #
    #     yield InstagramItem(commented_users=commented_users, post_shortcode=vars.get('shortcode'))

    def parse_likes(self, response: HtmlResponse, vars, code, user):
        data = json.loads(response.body)
        pass

    def parse_comments(self, response: HtmlResponse, vars, code, user):
        data = json.loads(response.body)
        pass



    def fetch_csrf_token(self, text):
        """Используя регулярные выражения парсит переданную строку на наличие
        `csrf_token` и возвращет его."""
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        """Используя регулярные выражения парсит переданную строку на наличие
        `id` нужного пользователя и возвращет его."""
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')

    def make_graphql_url(self, variables, query_hash):
        """Возвращает `url` для `graphql` запроса"""
        result = '{url}query_hash={hash}&{variables}'.format(
            url=self.graphql_url, hash=query_hash,
            variables=urlencode(variables)
        )
        return result