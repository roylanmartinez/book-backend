import graphene
import datetime
from graphene_django import DjangoObjectType
from graphql_auth import mutations
from .models import Author
from graphql_auth.schema import UserQuery, MeQuery
from graphql_jwt.decorators import login_required, superuser_required


class AuthMutation(graphene.ObjectType):
    # Authentication with django-graphql-auth
    # docs here: https://django-graphql-auth.readthedocs.io/en/latest/api/
    create_user_credentials = mutations.Register.Field()
    verify_user_account = mutations.VerifyAccount.Field()
    login_token = mutations.ObtainJSONWebToken.Field()
    logout_token = mutations.RevokeToken.Field()
    # update_user_credentials = mutations.UpdateAccount.Field()
    # resend_activation_email = mutations.ResendActivationEmail.Field()
    # send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    update_password = mutations.PasswordReset.Field()


class AuthorType(DjangoObjectType):
    class Meta:
        model = Author
        fields = ('id', 'username', 'email', 'description')


class Query(MeQuery, UserQuery, graphene.ObjectType):
    # UserQuery was deleted of the arguments because otherwise it shows all user details
    # If I add more arguments it can then be used as a function in graphql
    all_authors = graphene.List(AuthorType)
    # all_reviews = graphene.List(ReviewType)
    # all_reviewliketypes = graphene.List(ReviewLikeType)

    def resolve_all_authors(root, info):
        return Author.objects.all()


class Mutation(AuthMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
