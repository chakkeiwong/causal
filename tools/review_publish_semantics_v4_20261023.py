#!/usr/bin/env python3
"""Bind the common preserving review to the v4 reader and evidence directory."""
import argparse
import review_publish_semantics_20261023 as review
import build_semantics_reader_v4_20261023 as build

review.build = build
review.ROOT, review.BASE, review.OUT = build.ROOT, build.BASE, build.OUT

if __name__ == '__main__':
    commands = dict(review=review.review, publish=review.publish, renew=review.renew)
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=commands)
    commands[parser.parse_args().command]()
