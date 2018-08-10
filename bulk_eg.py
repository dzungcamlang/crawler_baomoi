from __future__ import print_function

from os.path import dirname, basename, abspath
from datetime import datetime
import logging
import sys
import argparse

import git

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import TransportError
from elasticsearch.helpers import bulk, streaming_bulk

def create_git_index(client, index):
    # we will use user on several places
    user_mapping = {
      'properties': {
        'name': {
          'type': 'text',
          'fields': {
            'keyword': {'type': 'keyword'},
          }
        }
      }
    }

    create_index_body = {
      'settings': {
        # just one shard, no replicas for testing
        'number_of_shards': 1,
        'number_of_replicas': 0,

        # custom analyzer for analyzing file paths
        'analysis': {
          'analyzer': {
            'file_path': {
              'type': 'custom',
              'tokenizer': 'path_hierarchy',
              'filter': ['lowercase']
            }
          }
        }
      },
      'mappings': {
        'doc': {
          'properties': {
            'repository': {'type': 'keyword'},
            'author': user_mapping,
            'authored_date': {'type': 'date'},
            'committer': user_mapping,
            'committed_date': {'type': 'date'},
            'parent_shas': {'type': 'keyword'},
            'description': {'type': 'text', 'analyzer': 'snowball'},
            'files': {'type': 'text', 'analyzer': 'file_path', "fielddata": True}
          }
        }
      }
    }

    # create empty index
    try:
        client.indices.create(
            index=index,
            body=create_index_body,
        )
    except TransportError as e:
        # ignore already existing index
        if e.error == 'index_already_exists_exception':
            pass
        else:
            raise

def parse_commits(head, name):
    """
    Go through the git repository log and generate a document per commit
    containing all the metadata.
    """
    for commit in head.traverse():
        yield {
            '_id': commit.hexsha,
            'repository': name,
            'committed_date': datetime.fromtimestamp(commit.committed_date),
            'committer': {
                'name': commit.committer.name,
                'email': commit.committer.email,
            },
            'authored_date': datetime.fromtimestamp(commit.authored_date),
            'author': {
                'name': commit.author.name,
                'email': commit.author.email,
            },
            'description': commit.message,
            'parent_shas': [p.hexsha for p in commit.parents],
            # we only care about the filenames, not the per-file stats
            'files': list(commit.stats.files),
            'stats': commit.stats.total,
        }

def load_repo(client, path=None, index='git'):
    """
    Parse a git repository with all it's commits and load it into elasticsearch
    using `client`. If the index doesn't exist it will be created.
    """
    path = dirname(dirname(abspath(__file__))) if path is None else path
    repo_name = basename(path)
    repo = git.Repo(path)

    create_git_index(client, index)

    # we let the streaming bulk continuously process the commits as they come
    # in - since the `parse_commits` function is a generator this will avoid
    # loading all the commits into memory
    for ok, result in streaming_bulk(
            client,
            parse_commits(repo.refs.master.commit, repo_name),
            index=index,
            doc_type='doc',
            chunk_size=50 # keep the batch sizes small for appearances only
        ):
        action, result = result.popitem()
        doc_id = '/%s/doc/%s' % (index, result['_id'])
        # process the information from ES whether the document has been
        # successfully indexed
        if not ok:
            print('Failed to %s document %s: %r' % (action, doc_id, result))
        else:
print(doc_id)