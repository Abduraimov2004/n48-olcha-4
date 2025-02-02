from rest_framework import serializers
from .models import Category, Group, Product, Image, Comment

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)
    full_image_url = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField(method_name='groups_count')

    def groups_count(self, obj):
        count = obj.groups.count()
        return count

    def get_full_image_url(self, instance):

        if instance.image:
            image_url = instance.image.url
            request = self.context.get('request')
            return request.build_absolute_uri(image_url)
        else:
            return None

    class Meta:
        model = Category
        fields = ['id', 'title', 'full_image_url', 'slug', 'count', 'groups']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    all_images = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()  # To get all comments
    comments_count = serializers.SerializerMethodField()  # To get comment count
    users_like = serializers.SerializerMethodField()  # To check if user liked the product
    average_rating = serializers.SerializerMethodField()  # To get average rating

    def get_all_images(self, instance):
        request = self.context.get('request')
        images = [request.build_absolute_uri(image.image.url) for image in instance.images.all()]
        return images

    def get_comments(self, instance):
        return CommentSerializer(instance.comments.all(), many=True).data

    def get_comments_count(self, instance):
        return instance.comments.count()

    def get_users_like(self, instance):
        request = self.context.get('request')
        user = request.user
        return instance.users_like.filter(id=user.id).exists() if user.is_authenticated else False

    def get_average_rating(self, instance):
        comments = instance.comments.all()
        total_ratings = sum([comment.rating for comment in comments])
        return total_ratings / comments.count() if comments.count() > 0 else 0

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'quantity', 'all_images',
            'comments', 'comments_count', 'users_like', 'average_rating'
        ]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'message', 'rating', 'created_at']

