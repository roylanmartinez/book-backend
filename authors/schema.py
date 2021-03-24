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
    # password_change = mutations.PasswordChange.Field()
    verify = mutations.VerifyToken.Field()


class AuthorType(DjangoObjectType):
    class Meta:
        model = Author
        fields = ('id', 'username', 'email', 'description', 'love')


class BookType(DjangoObjectType):
    class Meta:
        model = Book
        fields = ('id', 'name', 'description', 'made', 'created_at', 'author', 'love', 'category')


class Query(MeQuery, UserQuery, graphene.ObjectType):
    all_authors = graphene.List(AuthorType)
    all_books = graphene.List(BookType)

    # @login_required
    def resolve_all_authors(root, info):
        return Author.objects.all()

    # @login_required
    def resolve_all_books(root, info):
        return Book.objects.all()


class BookMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        category = graphene.String()
        description = graphene.String()
        delete = graphene.Boolean()

    book = graphene.Field(BookType)

    @classmethod
    def mutate(cls, root, info, name="", category="", description=""):
        # owner
        owner = Author.objects.get(id=info.context.user.id)

        book = Book.objects.create(author=owner)
        if name == "":
            book.name = "Without name"
        else:
            book.name = name
        if category == "":
            book.category = "this book has not a category"
        else:
            book.category = category
        if description == "":
            book.description = "this book has not a description"
        else:
            book.description = description
        book.save()
        # owner.love.add(book)

        # book.book_set.add(
        return BookMutation(book=book)


class LikeMutation(graphene.Mutation):
    class Arguments:
        bookid = graphene.ID()
        like = graphene.Boolean(required=True)


    book = graphene.Field(BookType)

    @classmethod
    def mutate(cls, root, info, bookid, like=False):
        book = Book.objects.get(id=bookid)
        owner = Author.objects.get(id=info.context.user.id)
        if like:
            book.love.add(owner)
            book.save()
        else:
            book.love.remove(owner)
            book.save()

        return LikeMutation(book=book)


class AuthorMutation(graphene.Mutation):
    class Arguments:
        authorid = graphene.ID()
        username = graphene.String()
        email = graphene.String()
        delete = graphene.Boolean()


    author = graphene.Field(AuthorType)

    @classmethod
    def mutate(cls, root, info, authorid, username, email, delete):
        author = Author.objects.get(id=authorid)

        if delete:
            # print("deleteeeeeeeeeeeeeeeeeeeeeeeeeeeee")
            author.delete()
        else:
            author.username = username
            author.email = email
            author.save()

        return AuthorMutation(author=author)


class EditBookMutation(graphene.Mutation):
    class Arguments:
        bookid = graphene.ID()
        name = graphene.String()
        description = graphene.String()
        category = graphene.String()
        delete = graphene.Boolean()
        pass

    book = graphene.Field(BookType)

    @classmethod
    def mutate(cls, root, info, bookid, name, description, category, delete):
        # print(bookid)
        book = Book.objects.get(id=bookid)

        if delete:
            # print("deleteeeeeeeeeeeeeeeeeeeeeeeeeeeee")
            book.delete()
        else:
            book.name = name
            book.description = description
            book.category = category
            book.save()

        return EditBookMutation(book=book)


class Mutation(AuthMutation, graphene.ObjectType):
    editTheAuthor = AuthorMutation.Field()
    newBook = BookMutation.Field()
    editPostLike = LikeMutation.Field()
    editTheBook = EditBookMutation.Field()
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
