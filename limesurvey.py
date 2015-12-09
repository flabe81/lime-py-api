#!/usr/bin/python
# -*- coding: utf-8 -*-


import json
import sys

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
from csv import DictReader
from time import sleep


class Api:
    def __init__(self, url, user, pw):
        self.url = url
        self._user = user
        self._password = pw

        data = """{   "id": 1,
                    "method": "get_session_key",
                    "params": { "username": "%s",
                                "password": "%s" } } """ % (user, pw)

        self.session_key = self._get_json(data)['result']

    def _get_json(self, data):
        req = urllib2.Request(url=self.url, data=data)
        req.add_header('content-type', 'application/json')
        req.add_header('connection', 'Keep-Alive')

        try:
            f = urllib2.urlopen(req)
            response = f.read()
            return json.loads(response)

        except:
            e = sys.exc_info()[0]
            print ("<p>Error: %s</p>" % e)

    def delete_survey(self, sid):
        data = """{ "id": 1,
                    "method": "delete_survey",
                    "params": { "sSessionKey": "%s",
                                "iSurveyID": %s } }""" % (self.session_key,
                                                          sid)
        return self._get_json(data)['result']

    def set_survey_property(self, sid, prop, value):
        data = """{ "id": 1,
                    "method": "set_survey_properties",
                    "params": { "sSessionKey": "%s",
                                "iSurveyID": %s,
                                "aSurveySettings": { "%s": "%s" }
            } }""" % (self.session_key, sid, prop, value)
        return self._get_json(data)['result']

    def get_survey_properties(self, sid, settings=None):

        if settings is None:
            settings = """ [
            "sid","savetimings","allowprev","tokenanswerspersistence",
            "showgroupinfo","showwelcome","owner_id","template","printanswers",
            "assessments","shownoanswer","showprogress","admin","language",
            "ipaddr","usecaptcha","showqnumcode","allowjumps","active",
            "additional_languages","refurl","usetokens","bouncetime",
            "navigationdelay","expires","datestamp","datecreated",
            "bounce_email","bounceprocessing","nokeyboard","startdate",
            "usecookie","publicstatistics","attributedescriptions",
            "bounceaccounttype","alloweditaftercompletion","adminemail",
            "allowregister","publicgraphs","emailresponseto",
            "bounceaccounthost","googleanalyticsstyle","anonymized",
            "allowsave","listpublic","emailnotificationto","bounceaccountpass",
            "googleanalyticsapikey","faxto","autonumber_start","htmlemail",
            "tokenlength","bounceaccountencryption","format","autoredirect",
            "sendconfirmation","showxquestions","bounceaccountuser" ] """

        data = """{ "id": 1,
                    "method": "get_survey_properties",
                    "params": { "sSessionKey": "%s",
                                "iSurveyID": %s,
                                "aSurveySettings": %s
            } }""" % (self.session_key, sid, settings)
        return self._get_json(data)['result']

    def get_summary(self, sid):
        data = """{ "id": 1,
                    "method": "get_summary",
                    "params": { "sSessionKey": "%s",
                                "iSurveyID": %s,
                                "sStatname": "all" } }""" % (self.session_key,
                                                             sid)
        return self._get_json(data)['result']

    def list_surveys(self):
        json_list_surveys = self._list_surveys()

        surveys = []
        for e in json_list_surveys:
            survey = e['sid'], e['surveyls_title']
            surveys.append(survey)
        return surveys

    def _list_surveys(self):
        """Devuelve el JSON ENTERO"""
        data = """{ "id": 1,
                    "method": "list_surveys",
                    "params": { "sSessionKey": "%s" } }""" % (self.session_key)

        return self._get_json(data)['result']

    def activate_survey(self, sid):
        data = """{ "id": 1,
                    "method": "activate_survey",
                    "params": { "sSessionKey": "%s",
                                "SurveyID": %s } }""" % (self.session_key, sid)
        return self._get_json(data)['result']

    def import_survey(self, datos, titulo, sid, tipo='lss'):
        data = """{ "id": 1,
                    "method": "import_survey",
                    "params": { "sSessionKey": "%s",
                                "sImportData": "%s",
                                "sImportDataType": "%s",
                                "sNewSurveyName": "%s",
                                "DestSurveyID": %d } }""" \
               % (self.session_key, datos, tipo, titulo, sid)
        return self._get_json(data)['result']

    def release_session_key(self):
        data = """ { "method": "release_session_key",
                     "params": { "sSessionKey" : "%s"},
                     "id":1}' }""" % (self.session_key)
        return self._get_json(data)['result']

    def export_responses(self, sid):
        data = """ {    "id" : 1,
                        "method":"export_responses",
                        "params": { "sSessionKey": "%s",
                                    "iSurveyID":  %s,
                                    "sDocumentType": "json",
                                    "sLanguageCode": "ca",
                                    "sCompletionStatus":"all",
                                    "sHeadingType": "code",
                                    "sResponseType": "long"
                        } } """ % (self.session_key, sid)
        return self._get_json(data)['result']

    def export_responses_by_token(self, sid, token, language_code):
        data = """ {    "id" : 1,
                        "method":"export_responses_by_token",
                        "params": { "sSessionKey": "%s",
                                    "iSurveyID":  %s,
                                    "sDocumentType": "json",
                                    "sToken":  "%s",
                                    "$sLanguageCode": "%s",
                                    "sCompletationStatus": "all",
                                    "sHeadingType": "code",
                                    "sResponseType": "long"
                        } } """ % (self.session_key, sid, token, language_code)
        return self._get_json(data)['result']

    def _add_response(self, sid, response_data):
        data = """ {          "id": 1,
                              "method":"add_response",
                              "params": { "sSessionKey": "%s",
                                          "iSurveyID": %s,
                                          "aResponseData": %s }
                    } """ % (self.session_key, sid, response_data)
        return self._get_json(data)['result']


    '''Update Response '''
    def update_response(self, sid, response_data):
        data = """ {          "id": 1,
                              "method":"update_response",
                              "params": { "sSessionKey": "%s",
                                          "iSurveyID": %s,
                                          "aResponseData": %s }
                    } """ % (self.session_key, sid, response_data)
        return self._get_json(data)['result']

    def impor_from_file(self, sid, file):
        """Esto no funciona!"""

        with open(file) as csv:
            datos = []
            for line in csv.readlines():
                datos.append(line.rstrip().split('\t'))

        columns = datos[1]
        for d in datos[2:]:
            r = dict(zip(columns, d))
            r['id'] = ""
            self._add_response(sid, json.dumps(r))
            sleep(1)

    def _list_groups(self, sid):
        data = """ {          "method":"list_groups",
                              "params": { "sSessionKey": "%s",
                                          "iSurveyID": %s },
                            "id": 1 } """ % (self.session_key, sid)
        return self._get_json(data)['result']

    def list_groups(self, sid):
        json_list_groups = self._list_groups(sid)

        groups = []
        for g in json_list_groups:
            group = g['id']['gid'], g['group_name']
            groups.append(group)

        return groups

    def _list_questions(self, sid, gid):
        data = """ {          "method":"list_questions",
                              "params": { "sSessionKey": "%s",
                                          "iSurveyID": %s,
                                          "iGroupID": %s },
                            "id": 1 } """ % (self.session_key, sid, gid)
        return self._get_json(data)['result']

    def list_questions(self, sid, gid):
        json_list_questions = self._list_questions(sid, gid)

        questions = []
        for q in json_list_questions:
            question = q['id']['qid'], q['question']
            questions.append(question)

        return questions
