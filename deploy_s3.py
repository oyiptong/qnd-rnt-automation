#!/usr/bin/env python
from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool
import sys
import json
import os
import hashlib
import boto
import copy
from boto.s3.key import Key
from furl import furl

INPUT_DIR = './build'
all_files = []
bucket = None
gpool = Pool(20)

headers = {
    'Cache-Control': 'public, max-age=86400',
}


def upload_maybe(fname):

    keyname = fname[len(INPUT_DIR)+1:]
    key = bucket.get_key(keyname)
    uploaded = False

    fname_md5 = hashlib.md5()
    with open(fname, 'r') as f:
        fname_md5.update(f.read())

    hsh = fname_md5.hexdigest()

    if key is None or key.md5 != hsh:
        h = headers
        if keyname.endswith('sw.js'):
            h = copy.deepcopy(headers)
            h['Service-Worker-Allowed'] = '/'
        key = Key(bucket)
        key.name = keyname
        key.set_contents_from_filename(fname, headers=h)
        key.set_acl("public-read")
        uploaded = True

    url = key.generate_url(expires_in=0, query_auth=False)

    uri = furl(url)
    try:
        uri.args.pop('x-amz-security-token')
    except:
        pass
    url = uri.url
    return (url, uploaded)


if __name__ == "__main__":
    for dirpath, dirnames, files in os.walk(os.path.join(INPUT_DIR, "v0")):
        if len(files):
            for f in files:
                filepath = os.path.join(dirpath, f)
                print "adding: {}".format(filepath)
                all_files.append(filepath)

    upload_count = len(all_files)

    print "found {} files".format(upload_count)

    s3 = boto.connect_s3()
    global bucket
    bucket = s3.get_bucket('mozilla-cs-newtab')

    urls = []

    process_count = 0
    tasks = gpool.imap_unordered(upload_maybe, all_files)

    for url, uploaded in tasks:
        urls.append((url, uploaded))
        process_count += 1
        sys.stdout.write('\rprocessed file {} / {}'.format(
            process_count, upload_count))
        sys.stdout.flush()

    sys.stdout.write('\n')

    with open('distro_out.json', 'w') as f:
        json.dump(urls, f)
    print 'dumped output at ./distro_out.json'
