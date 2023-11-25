# Chapter 3: Serializing Data with DRF

## Table of Contents
* [Understanding the basics of DRF Serializers](#understanding-the-basics-of-drf-serializers)
* [Using Model Serializers](#using-model-serializers)
  * [Creating a new model object](#creating-a-new-model-object) 
  * [Updating existing model objects](#updating-existing-model-objects)
  * [Retrieving data from the Model object instance](#retrieving-data-from-the-model-object-instance)
  * [Exploring Meta class](#exploring-meta-class)
* [Implementing Serializer Relations](#implementing-serializer-relations)
  * [Working with Nested Serializers](#working-with-nested-serializers)
  * [Exploring source](#exploring-source)
  * [Exploring SerializerMethodField](#exploring-serializermethodfield)
* [Validating Data with Serializers](#validating-data-with-serializers)
  * [Customizing field level Validation](#customizing-field-level-validation)
  * [Performing Object level Validation](#performing-object-level-validation)
  * [Defining Custom object validators](#defining-custom-object-validators)
  * [Order of evaluation of Validators](#order-of-evaluation-of-validators)
  * [Remove default validators from the DRF Serializer class](#remove-default-validators-from-the-drf-serializer-class)
* [Mastering DRF Serializers](#mastering-drf-serializers)
* [Using Serializers with DRF Views](#using-serializers-with-drf-views)
  * [Working with Generic Views](#working-with-generic-views)
  * [Filtering with SearchFilter and OrderingFilter](#filtering-with-searchfilter-and-orderingfilter)

## Understanding the basics of DRF Serializers

## Using Model Serializers

Taking the same blog example as in the previous chapter. Create a new model serializer for Blog model.

create a new file `blog/serializers.py` with the following code

```python
from rest_framework import serializers

from blog import models


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Blog
        fields = '__all__'
```

Now we can use this serializer to create a new blog object. 

Let us first test what default definition values did the `ModelSerializer` take.

Open python shell and run the following commands

```bash
python manage.py shell
```
> Once the python shell opens, run the following commands in the python shell.

```python
from blog import serializers
print(serializers.BlogSerializer())
```

### Creating a new model object

> Run the following commands in the python shell

```python
from blog import serializers
input_data = {
    'title': 'My First Blog',
    'content': 'This is my first blog. I am so excited to write my first blog.',
    'author': '1',
} 

new_blog = serializers.BlogSerializer(data=input_data)
new_blog.is_valid()
new_blog.save()
```

Let us check how we can override the default behavior of ModelSerializer. 

Create a new serializer class `BlogCustomSerializer` in `blog/serializers.py` with the following code

> Run the following commands in the python shell

```python
from blog import serializers
class BlogCustomSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        print('*** Custom Create method ****')
        return super(BlogCustomSerializer, self).create(validated_data)

    class Meta:
        model = Blog
        fields = '__all__'
```

### Updating existing model objects

> Run the following commands in the python shell

```python
from blog import models, serializers

update_input_data = {
  'title': 'Updated title',
}
existing_blog = models.Blog.objects.get(id=1)
update_blog = serializers.BlogSerializer(instance=existing_blog, data=update_input_data, partial=True)
update_blog.is_valid()
update_blog.save()
```
Custom `update` method `BlogCustom2Serializer` in `blog/serializers.py` with the following code

```python
class BlogCustom2Serializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        print('*** Custom Update method ****')
        return super(BlogCustom2Serializer, self).update(instance, validated_data)

    class Meta:
        model = Blog
        fields = '__all__'

```

> Run the following commands in the python shell

```python
from blog import models, serializers

update_input_data = {
  'title': 'Updated title',
}
existing_blog = models.Blog.objects.get(id=1)
update_blog = serializers.BlogCustom2Serializer(instance=existing_blog, data=update_input_data, partial=True)
update_blog.is_valid()
update_blog.save()
```

### Retrieving data from the Model object instance

> Run the following commands in the python shell

```python
from blog import models, serializers
from pprint import pprint

first_blog = models.Blog.objects.get(id=1)
blog_obj_data = serializers.BlogSerializer(instance=first_blog)
pprint(blog_obj_data.data)
``` 

Retrieve multiple model objects

> Run the following commands in the python shell

```python
from blog import models, serializers
from pprint import pprint

all_blogs = models.Blog.objects.all()
blog_obj_data = serializers.BlogSerializer(instance=all_blogs, many=True)
pprint(blog_obj_data.data)
```

### Exploring Meta class

## Implementing Serializer Relations

Create serializer relations for `Blog` model related to `Tags`, `CoverImage` and `Author` models.

```python
from rest_framework import serializers
from rest_framework import validators

from blog import models
from author import models as author_models


class BlogCustom3Serializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=author_models.Author.objects.all())
    tags = serializers.PrimaryKeyRelatedField(
        queryset=models.Tags.objects.all(), many=True, allow_empty=True
    )
    cover_image = serializers.PrimaryKeyRelatedField(
        queryset=models.CoverImage.objects.all(),
        validators=[validators.UniqueValidator(models.CoverImage.objects.all())]
    )

    class Meta:
        model = models.Blog
        fields = '__all__'
```

### Working with Nested Serializers

```python
class BASerializer(serializers.ModelSerializer):
    class Meta:
        model = author_models.Author
        fields = ['name', 'bio']


class BlogCustom4Serializer(serializers.ModelSerializer):
    author_details = BASerializer(source='author')

    class Meta:
        model = models.Blog
        fields = '__all__'
```

### Exploring source

```python
# author/models.py
class Author(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    bio = models.TextField()
    
    def fetch_short_bio(self):
         return self.bio[:100]

# author/serializer.py
class AuthorSerializer(serializers.ModelSerializer):
    long_bio = serializers.CharField(source='bio')
    short_bio = serializers.CharField(source='fetch_short_bio')

    class Meta:
        model = Author
        fields = '__all__'
        exclude = ['bio', 'email']
```

### Exploring SerializerMethodField

```python
class BlogCustom5Serializer(serializers.ModelSerializer):
    word_count = serializers.SerializerMethodField()
    
    def get_word_count(self, obj):
        return len(obj.content.split())
    
    class Meta:
        model = models.Blog
        fields = '__all__'
```

```python
class BlogCustom6CustomSerializer(serializers.ModelSerializer):
    word_count = serializers.SerializerMethodField(
        method_name='use_custom_word_count'
    )
    
    def use_custom_word_count(self, obj):
        return len(obj.content.split())
    
    class Meta:
        model = models.Blog
        fields = '__all__'
```

## Validating Data with Serializers

### Customizing field level Validation

```python
class BlogCustom7Serializer(serializers.ModelSerializer):
    def validate_title(self, value):
        print('validate_title method')
        if '_' in value:
            raise serializers.ValidationError('illegal char')
        return value

    class Meta:
        model = Blog
        fields = '__all__'

```

### Defining Custom field level validator

```python
def demo_func_validator(attr):
    print('func val')
    if '_' in attr:
        raise serializers.ValidationError('invalid char')
    return attr


class BlogCustom8Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Blog
        fields = '__all__'
        extra_kwargs = {
            'title': {
                'validators': [demo_func_validator]
            },
            'content': {
                'validators': [demo_func_validator]
            }
        }

```

### Performing Object level Validation

```python
class BlogCustom9Serializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if attrs['title'] == attrs['content']:
            raise serializers.ValidationError('Title and content cannot have value')   
        return attrs

    class Meta:
        model = models.Blog
        fields = '__all__'
```

### Defining Custom object validators

```python
def custom_obj_validator(attrs):
    print('custom object validator')
    if attrs['title'] == attrs['content']:
        raise serializers.ValidationError('Title and content cannot have the same')
    return attrs

class BlogCustom10Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Blog
        fields = '__all__'
        validators = [custom_obj_validator]

```

### Order of evaluation of Validators

```python
def func_validator(attr): # 1- Evaluates first
    print('func val')
    if '*' in attr:
        raise serializers.ValidationError('Illegal char')
    return attr

class BlogCustom11Serializer(serializers.ModelSerializer):
    def validate_title(self, value): # 2-If func_validator succeeds
        print('validate_title method')
        if '_' in value:
            raise serializers.ValidationError('Illegal char')
        return value

    def validate(self, attrs): # 3- If all field validator succeeds
        print('main validate method')
        return attrs
    
    class Meta:
        model = models.Blog
        fields = '__all__'
        extra_kwargs = {
            'title': {
                'validators': [func_validator]
            }
        }

```


### Remove default validators from the DRF Serializer class

```python
class BlogCustom12Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Blog
        fields = '__all__'
        validators = []
```


## Mastering DRF Serializers

### Using to_internal_value

```python
class BlogCustom13Serializer(serializers.ModelSerializer):
    def to_internal_value(self, data):
        print('before validation', data)
        return super().to_internal_value(data)

    class Meta:
        model = models.Blog
        fields = '__all__'
```

### Using to_representation

```python
class BlogCustom14Serializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        resp = super().to_representation(instance)
        resp['title'] = resp['title'].upper()
        return resp

    class Meta:
        model = models.Blog
        fields = '__all__'

```

### Use context argument to pass information

```python
class BlogCustom15Serializer(serializers.ModelSerializer):
    def to_internal_value(self, data):
        print('Printing context –', self.context)
        return super().to_internal_value(data)

    class Meta:
        model = models.Blog
        fields = '__all__'
        
```
Now let us pass some data to the context argument

```python
input_data = BlogCustom15Serializer(
    data={'title':'abc'}, context={'request': 'some value'}
)
input_data.is_valid()
# Printing context – {'request': 'some value'}
```

### Customizing fields

### Passing custom queryset to PrimaryKeyField

```python
class CustomPKRelatedField(serializers.PrimaryKeyRelatedField): 
    def get_queryset(self):
        req = self.context.get('request', None) #context value
        queryset = super().get_queryset() #retrieve default filter
        if not req:
            return None
        return queryset.filter(user=req.user) #additional filter

class BlogCustom16Serialzier(serializers.ModelSerializer):
    tags = CustomPKRelatedField(queryset=Tags.objects.all())

    class Meta:
        model = models.Blog
        fields = '__all__'
```


### Building DynamicFieldsSerializer 

### Avoiding the N+1 query problem

## Using Serializers with DRF Views

Add the following code to `blog/views.py`
```python
from rest_framework import views
from rest_framework import response
from rest_framework import status

class BlogGetCreateView(views.APIView):
    def get(self, request):
        blogs_obj_list = models.Blog.objects.all()
        blogs = serializer.BlogSerializer(blogs_obj_list, many=True)
        return response.Response(blogs.data)

    def post(self, request):
        input_data = request.data
        b_obj = serializer.BlogSerializer(data=input_data)
        if b_obj.is_valid():
            b_obj.save()
            return response.Response(b_obj.data, status=status.HTTP_201_CREATED)
        return response.Response(b_obj.errors, status=status.HTTP_400_BAD_REQUEST)
```

### Working with Generic Views

Add the following code to `blog/views.py`
```python
from rest_framework import generics

class BlogGetUpdateView(generics.ListCreateAPIView):
    serializer_class = serializer.BlogSerializer

    def get_queryset(self):
        blogs_queryset = models.Blog.objects.filter(id__gt=1)
        return blogs_queryset
```


### Filtering with SearchFilter and OrderingFilter

Add the following code to `blog/views.py`
```python
from rest_framework import filters

class BlogGetUpdateFilterView(generics.ListAPIView):
    serializer_class = serializer.BlogSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['title']
```

