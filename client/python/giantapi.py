import os
import requests
import json as pyjson

from collections import OrderedDict
from StringIO import StringIO
# from pandas import DataFrame

class NetwasJob(object):

    url = "http://giant-api.princeton.edu/netwas/1.0/jobs"

    @classmethod
    def from_server(cls, id):
        sync_url = cls.url + "/" + id
        r = requests.get(sync_url)
        if r.status_code != requests.codes.ok:
            r.raise_for_status()
        json = r.json()
        nj = cls(json['gwas_file'],
                 json['gwas_format'],
                 json['tissue'],
                 json['p_value'],
                 json['title'],
                 json['email'],
                 True)
        nj.id = json['id']
        nj.created = json['created']
        nj.sync()
        nj.is_init = True
        return nj

    def __init__(self, gwas_file, gwas_format, tissue, p_value, title=None, email=None, from_server=False):
        # For lazy initialization
        self.is_init = False

        # Fields assigned by the user at the front end
        self.title = title
        self.email = email
        self.gwas_file = gwas_file
        self.gwas_format = gwas_format
        self.tissue = tissue
        self.p_value = p_value

        # Fields assigned by the server at the back end
        self.id = None
        self.created = None
        self.log_file = None
        self.results_file = None
        self.status = None
        if from_server:
            pass
        else:
            if not os.path.isfile(self.gwas_file):
                raise IOError("GWAS file '" + self.gwas_file + "' can't be opened.")

    def json(self):
        d = self.__dict__
        keys = ['id', 'created', 'title', 'email', 'gwas_file', 'gwas_file', 'tissue', 'p_value', 'log_file', 'results_file', 'status']
        od = OrderedDict((key, d[key]) for key in keys)
        json = pyjson.dumps(od, indent=4, separators=(',', ': '))
        return json

    def __str__(self):
        self.sync()
        return str(self.json())

    def __repr__(self):
        self.sync()
        return str(self.json())

    def init(self):
        if self.is_init:
            return
        data = {'gwas_format': self.gwas_format, 'tissue': self.tissue, 'p_value': str(self.p_value)}
        if self.title is not None:
            data['title'] = self.title
        if self.email is not None:
            data['email'] = self.email
        files = {'gwas_file': (self.gwas_file, open(self.gwas_file, 'rb'))}

        r = requests.post(self.url, data=data, files=files)
        if r.status_code != requests.codes.ok:
            r.raise_for_status()
        json = r.json()
        self.id = json['id']
        self.created = json['created']
        # Rewrite file path to remote location.
        self.gwas_file = json['gwas_file']
        self.status = json['status']

        self.is_init = True

    def start(self):
        # Lazy initialization
        if not self.is_init:
            self.init()
        # Disallow restarting running or completed jobs. This is now rejected by
        # the API anyway but we can still save a network request.
        if self.status != 'not_started':
            return
        start_url = self.url + "/" + self.id + "/start"
        r = requests.post(start_url)
        json = r.json()
        self.status = json['status']

    def sync(self):
        if self.id is None:
            return
        sync_url = self.url + "/" + self.id
        r = requests.get(sync_url)
        json = r.json()
        self.status = json['status']
        self.log_file = json['log_file']
        self.results_file = json['results_file']

    def log(self):
        self.sync()
        if self.log_file is None:
            return
        log_url = self.log_file
        r = requests.get(log_url)
        return str(r.text)

    def result(self):
        self.sync()
        if self.results_file is None:
            return
        results_url = self.results_file
        r = requests.get(results_url)
        rs = ["gene\tclass\tz_score"]
        # Results files have \r\n terminators, which we replace.
        for line in r.text.splitlines():
            # Remove comments and spaces
            li = line.split('#')[0].strip()
            if li:
                rs.append(li)
        rs2 = "\n".join(rs)
        return rs2
        # ss = StringIO(rs2)
        # df = DataFrame.from_csv(ss, sep='\t')
        # return df

    def results(self):
        return self.result()
