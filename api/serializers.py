import json
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from webapp.models import Recipe, Step, Picture, Time, Savour, Comment


class FullImageField(serializers.ImageField):
    def to_native(self, value):
        request = self.context.get('request', None)
        if request and value:
            return request.build_absolute_uri(value.url)


class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class EmbeddedUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    display_name = serializers.CharField(source="profile.get.display_name")
    avatar = FullImageField(source="profile.get.avatar")


class StepSerializer(serializers.ModelSerializer):
    image = FullImageField()

    class Meta:
        model = Step
        fields = ('text', 'image')


class PictureSerializer(serializers.ModelSerializer):
    image = FullImageField()

    class Meta:
        model = Picture
        fields = ["image"]


class TimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Time
        fields = ('prep_time', 'cook_time')


class SavoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = Savour
        fields = ('salty', 'sour', 'bitter', 'sweet', 'spicy')


class CommentSerializer(serializers.ModelSerializer):
    user_own = EmbeddedUserSerializer()

    class Meta:
        model = Comment
        fields = ('text', 'create_date', 'user_own')


class EmbeddedRecipeSerializer(serializers.ModelSerializer):
    author = EmbeddedUserSerializer()

    class Meta:
        model = Recipe
        fields = ('id', 'title', 'author')


class RecipeSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    creation_date = serializers.DateTimeField()
    main_image = FullImageField()
    modification_date = serializers.DateTimeField()
    ingredients = serializers.SerializerMethodField("ingredients_list")
    serves = serializers.CharField()
    language = serializers.CharField()
    temporality = serializers.SerializerMethodField("temporality_list")
    nationality = serializers.CharField()
    special_conditions = serializers.SerializerMethodField("special_conditions_list")
    notes = serializers.CharField()
    difficult = serializers.IntegerField(max_value=3, min_value=1)
    food_type = serializers.CharField()
    tags = serializers.SerializerMethodField("tags_list")
    savours = SavoursSerializer()

    parent = EmbeddedRecipeSerializer()
    steps = StepSerializer()
    author = EmbeddedUserSerializer()
    pictures = PictureSerializer(many=True)
    time = TimeSerializer()
    comments = CommentSerializer(many=True)

    positives = serializers.SerializerMethodField('positive_votes')
    negatives = serializers.SerializerMethodField('negative_votes')

    child_recipes = EmbeddedRecipeSerializer(source='get_child_recipes', many=True)

    #TODO: http://www.snip2code.com/Snippet/12518/Django-REST-framework-list-serializer
    def ingredients_list(self, obj):
        return obj.ingredients

    def temporality_list(self, obj):
        return obj.temporality

    def special_conditions_list(self, obj):
        return obj.special_conditions

    def tags_list(self, obj):
        return obj.tags

    def positive_votes(self, obj):
        return len(obj.positives)

    def negative_votes(self, obj):
        return len(obj.negatives)

