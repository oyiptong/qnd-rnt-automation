#!/usr/bin/env python
import os
import shutil

LANGS = (
    'ach', 'af', 'ak', 'an', 'ar', 'as', 'ast', 'az', 'be', 'bg',
    'bn-BD', 'bn-IN', 'br', 'bs', 'ca', 'cs', 'csb', 'cy', 'da',
    'de', 'dsb', 'el', 'en-GB', 'en-US', 'en-ZA', 'eo', 'es-AR', 'es-CL',
    'es-ES', 'es-MX', 'et', 'eu', 'fa', 'ff', 'fi', 'fr', 'fy-NL',
    'ga-IE', 'gd', 'gl', 'gu-IN', 'he', 'hi-IN', 'hr', 'hu', 'hy-AM',
    'hsb', 'id', 'is', 'it', 'ja', 'ja-JP-mac', 'ka', 'kk', 'km', 'kn',
    'ko', 'ku', 'lg', 'lij', 'lt', 'lv', 'mai', 'mk', 'ml', 'mn',
    'mr', 'ms', 'my', 'nb-NO', 'nl', 'nn-NO', 'nso', 'oc', 'or', 'pa-IN',
    'pl', 'pt-BR', 'pt-PT', 'rm', 'ro', 'ru', 'sah', 'si', 'sk', 'sl',
    'son', 'sq', 'sr', 'sv-SE', 'sw', 'ta', 'ta-LK', 'te', 'th', 'tr',
    'uk', 'ur', 'vi', 'wo', 'xh', 'zh-CN', 'zh-TW', 'zu',
)

CHANNELS = (
    'nightly', 'aurora', 'beta', 'release'
)

INPUT_DIR = '/Users/oyiptong/Projects/up-projects/remote-newtab/src'
OUTPUT_BASEDIR = './build/'

VERSION = 'v2'

for channel in CHANNELS:
    for lang in LANGS:
        path = os.path.join(OUTPUT_BASEDIR, VERSION, channel, lang)
        print path

        shutil.copytree(INPUT_DIR, path)
