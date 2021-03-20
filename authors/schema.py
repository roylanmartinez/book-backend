import graphene
import datetime
from graphene_django import DjangoObjectType
from graphql_auth import mutations
from .models import Author, Book
from graphql_auth.schema import UserQuery, MeQuery
from graphql_jwt.decorators import login_required, superuser_required


class AuthMutation(graphene.ObjectType):

    create_user = mutations.Register.Field()
    login_user = mutations.ObtainJSONWebToken.Field()
    logout_user = mutations.RevokeToken.Field()
    update_password = mutations.PasswordReset.Field()
    verify = mutations.VerifyToken.Field()


class AuthorType(DjangoObjectType):
    class Meta:
        model = Author
        fields = ('id', 'username', 'email', 'description')


class BookType(DjangoObjectType):
    class Meta:
        model = Book
        fields = ('id', 'name', 'description', 'made', 'author')


class Query(MeQuery, UserQuery, graphene.ObjectType):
    all_authors = graphene.List(AuthorType)
    all_books = graphene.List(BookType)

    @login_required
    def resolve_all_authors(root, info):
        return Author.objects.all()

    @login_required
    def resolve_all_books(root, info):
        return Book.objects.all()


class BookMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        category = graphene.String(required=True)
        description = graphene.String(required=True)

    book = graphene.Field(BookType)

    @classmethod
    def mutate(cls, root, info, name="Don Quijote", category="Comedia", description="Comedias comunes"):
        owner = Author.objects.get(id=info.context.user.id)
        book = Book.objects.create(author=owner)
        book.name = name
        book.category = category
        book.description = description
        book.save()

        return BookMutation(book=book)


class Mutation(AuthMutation, graphene.ObjectType):
    newBook = BookMutation.Field()
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
