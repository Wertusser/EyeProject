# -*- coding: utf-8 -*-

import re #work with regual
import requests #work with URLs
import vk
from adapters.transliter import translit

class infoVk:
    def __init__(self,person_id):
        self.person_id = person_id
        if self.person_id[0].isdigit():
            pass
        else:
            self.person_id = infoVk.getAbout(person_id)[0]['uid']
            

    def getInfo(self):
        person_id = self.person_id
        about = infoVk.getAbout(person_id)
        try:
            wall = infoVk.getWall(person_id)
        except Exception:
            return {'person_id':person_id,'access':'denied'}
        geo = infoVk.getLocFromWall(wall)
        loc =[] + infoVk.getLocFromPhotos(person_id)
        for i in range(0,len(geo)):
            loc.append(float(geo[i][0]))
            loc.append(float(geo[i][1]))
        SomeUseful = infoVk.getTextFromWall(wall)
        urls = []
        for i in range(len(SomeUseful)):
            urls += re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',SomeUseful[i])
        if 'instagram' in about[0]:
            nicknames = about[0]['instagram']
        elif about[0]['screen_name'].startswith('id'):
            nicknames = infoVk.getNicknames(urls,person_id)
        else:
            nicknames = about[0]['screen_name']
        allData = infoVk.createDict(person_id,about,loc,urls,nicknames,access="accept")
        try:
            return allData
        except:
            pass

    @staticmethod
    def getAbout(person_id):
        session = vk.Session()
        api = vk.API(session)
        about = api.users.get(user_ids = person_id, fields = 'photo_200_orig, screen_name, status, domain, site, contacts, bdate, connections')
        return about

    def getWall(person_id):
        '''Get wall using person id.
    Return list of wall'''
        #create vk session
        session = vk.Session()
        api = vk.API(session)
        wall = api.wall.get(owner_id = person_id, filter ='owner')[1:]
        return wall

    def getLocFromWall(wall):
        '''Get geo location from vk wall.
        Return list of geo'''
        geo = []
        for i in range(len(wall)):
            try:
                geo.append(wall[i]['geo']['coordinates'].split())
            except:
                continue
        return geo

    def getLocFromPhotos(person_id):
        #create vk session
        session = vk.Session()
        api = vk.API(session)
        geo_photo =[]

        photo = api.photos.get(owner_id = person_id, album_id='profile')
        for i in range(len(photo)):
            try:
                a = photo[i]['lat'],photo[i]['long']
                geo_photo += a
                
            except Exception:
                continue
        return geo_photo

    def getNicknames(data,person_id):
        #create vk session
        session = vk.Session()
        api = vk.API(session)
        

        nicknames = []
        for i in data:
            regex_name = re.sub(r'.+(.com||.org||.tv||.ru||.fm)/','',i)
            if '<' in regex_name:
                nicknames.append(regex_name[:len(regex_name)-4])
            if regex_name.startswith('watch?'):
                continue
            else:
                nicknames.append(regex_name)
        name_nick = translit(api.users.get(user_ids = person_id)[0]['last_name'])
        nicknames.append(name_nick)
        return nicknames

    def getFriends(owner_id):
        #create vk session
        session = vk.Session()
        api = vk.API(session)

        friends = api.friends.get(user_id = owner_id)
        return friends

    def getMembers(group_id):
        #create vk session
        session = vk.Session()
        api = vk.API(session)
        members = []
        members_count = api.groups.getMembers(group_id = group_id)['count']
        for i in range(0,members_count // 1000):
            members += api.groups.getMembers(group_id = group_id, offset = i*1000)['users']
        return members

    def createDict(person_id,about,geo,urls,nicknames,access):
        d = {}
        d['Person_id'] = person_id
        d['About'] = about
        d['Location'] = geo
        d['Url'] = urls
        d['Nicknames'] = nicknames
        d['access'] = access
        return d

    def getTextFromWall(wall):
        '''Get useful text from vk wall.
        Return list of urls'''
        urls = []
        for i in range(len(wall)):
            try: 
            #trying to find some useful text using this filter(finding urls or words)
                if re. findall(r'вопрос',wall[i]['text']) or re.findall(r'instagram',wall[i]['text']) or re.findall(r'\wsk.fm',wall[i]['text']) or re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',wall[i]['text']):
                    urls.append(wall[i]['text'])
                    urls.append(wall[i]['attachments'][0]['link']['url'])
            except:
                continue
        return urls
