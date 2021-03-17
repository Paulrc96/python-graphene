from promise import Promise
from promise.dataloader import DataLoader

from graphql_server.models import Post, Comment

from promise import Promise
from promise.dataloader import DataLoader

import functools

from datetime import datetime


def queryPostsByUserIds(ids):
  return Post.objects.raw(f'SELECT * from posts WHERE user_id IN ({ids})')

def keysDataReducer (prev, current):
  prev[current] = []
  return prev

def transformPostData (postData, data, keys):
  for rows in data:
    for row in rows:
      postData[row.user_id].append(row)
  
  print('Posts promises resolved!', datetime.now())
  return Promise.resolve(list(map(lambda key: postData[key], keys)))

class PostsByUserLoader(DataLoader):
  def batch_load_fn(self, keys):
    print('Loading posts by users...')
    postsData = functools.reduce(keysDataReducer, keys, {})
    promises = []
    length = len(keys)
    i = 0
    size = 50000
    while i < length:
      tempUserIds = keys[i:i + size]
      print(f'Getting posts from {i} to {i + size}')
      i = i + size
      ids = ','.join(f'{id}' for id in tempUserIds)
      promises.append(
        Promise(
          lambda resolve, reject:
            resolve(queryPostsByUserIds(ids))
        )
      )
    print('Waiting for posts promises to resolve...', datetime.now())
    return Promise.all(promises).then(lambda data: transformPostData(postsData, data, keys))


def queryCommentsByPostIds(ids):
  return Comment.objects.raw(f'SELECT * from comments WHERE post_id IN ({ids})')

def transformCommentsData (postData, data, keys):
  for rows in data:
    for row in rows:
      postData[row.post_id].append(row)
  
  print('Posts comments resolved!', datetime.now())
  return Promise.resolve(list(map(lambda key: postData[key], keys)))

class CommentsByPostsLoader(DataLoader):
  def batch_load_fn(self, keys):
    commentsData = functools.reduce(keysDataReducer, keys, {})
    promises = []
    length = len(keys)
    i = 0
    size = 50000
    while i < length:
      tempPostIds = keys[i:i + size]
      print(f'Getting comments from {i} to {i + size}')
      i = i + size
      ids = ','.join(f'{id}' for id in tempPostIds)
      promises.append(
        Promise(
          lambda resolve, reject:
            resolve(queryCommentsByPostIds(ids))
        )
      )
    print('Waiting for comments promises to resolve...', datetime.now())
    return Promise.all(promises).then(lambda data: transformCommentsData(commentsData, data, keys))

class Loaders:
    def __init__(self):
        self.posts_by_user_loader = PostsByUserLoader()
        self.comments_by_post_loader = CommentsByPostsLoader()


class LoaderMiddleware:
    def resolve(self, next, root, info, **args):
      if not hasattr(info.context, 'loaders'):  
          info.context.loaders = Loaders()

      return next(root, info, **args)