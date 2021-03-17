import graphene

from graphql_server.models import User, Client

from promise import Promise

class CommentType(graphene.ObjectType):
    comment_id = graphene.Int(name='comment_id')
    post_id = graphene.Int(name='post_id')
    user_id = graphene.Int(name='user_id')
    description = graphene.String()
    created_at = graphene.String(name='created_at')
    updated_at = graphene.String(name='updated_at')
    

class PostType(graphene.ObjectType):
    post_id = graphene.Int(name='post_id')
    user_id = graphene.Int(name='user_id')
    title = graphene.String()
    description = graphene.String()
    created_at = graphene.String(name='created_at')
    updated_at = graphene.String(name='updated_at')

    comments = graphene.List(CommentType)

    def resolve_comments(parent, info):
      return (info.context['loaders']).comments_by_post_loader.load(parent.post_id)

class UserType(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    last_name = graphene.String(name='last_name')
    email = graphene.String()
    birthday = graphene.String()
    address = graphene.String()
    email_verified_at = graphene.String(name='email_verified_at')
    password = graphene.String()
    remember_token = graphene.String(name='remember_token')
    created_at = graphene.String(name='created_at')
    updated_at = graphene.String(name='updated_at')

    posts = graphene.List(PostType)

    def resolve_posts(parent, info):
      return (info.context['loaders']).posts_by_user_loader.load(parent.id)

class ClientInput(graphene.InputObjectType):
    name = graphene.String()
    last_name = graphene.String(name='last_name')
    email = graphene.String()
    birthday = graphene.String()
    address = graphene.String()
    created_at = graphene.String(name='created_at')
    updated_at = graphene.String(name='updated_at')

class ClientType(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    last_name = graphene.String(name='last_name')
    email = graphene.String()
    birthday = graphene.String()
    address = graphene.String()
    created_at = graphene.String(name='created_at')
    updated_at = graphene.String(name='updated_at')

class CreateClient(graphene.Mutation):
    class Arguments:
      client = graphene.Argument(lambda: ClientInput)

    Output = ClientType

    def mutate(root, info, client):
      newClient = Client.objects.create(
        name = client.name,
        last_name = client.last_name,
        email = client.email,
        birthday = client.birthday,
        address = client.address,
        created_at = client.created_at)

      return ClientType(
        id=newClient.id,
        name=client.name,
        last_name = client.last_name,
        email = client.email,
        birthday = client.birthday,
        address = client.address,
        created_at = client.created_at
      )

class Query(graphene.ObjectType):   
    users = graphene.List(UserType, first=graphene.Int(required=False))
    
    def resolve_users(root, info, first):
      return User.objects.order_by('id').all()[:first or 10]

class Mutation(graphene.ObjectType):
    createClient = CreateClient.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
