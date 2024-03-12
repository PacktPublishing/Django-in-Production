# Django in Production

<a href="https://www.packtpub.com/product/django-in-production/9781804610480"><img src="https://content.packt.com/B18867/cover_image_small.jpg" alt="" height="256px" align="right"></a>

This is the code repository for [Django in Production](https://www.packtpub.com/product/django-in-production/9781804610480), published by Packt.

**Expert tips, strategies, and essential frameworks for writing scalable and maintainable code in Django**

## What is this book about?
You may have got your first Django developer job after a six-week bootcamp or online course, and that’s great, but what’s next? In small companies, mentorship can be hard to come by and gaining the traits of a senior developer without that can take a long time. This is precisely where Django in Production comes into play.
	
This book covers the following exciting features:
* Write scalable and maintainable code like a Django expert
* Become proficient in Docker for Django and experience platform-agnostic development
* Explore intelligent practices for continuous integration
* Leverage the power of AWS to seamlessly deploy your application in a production environment
* Optimize unstable systems through effective performance monitoring
* Effortlessly handle authentication and authorization issues
* Automate repetitive tasks by creating custom middleware
* Thoroughly test your code using factory_boy and craft comprehensive API tests

If you feel this book is for you, get your [copy](https://www.amazon.com/dp/1804610488) today!

<a href="https://www.packtpub.com/?utm_source=github&utm_medium=banner&utm_campaign=GitHubBanner"><img src="https://raw.githubusercontent.com/PacktPublishing/GitHub/master/GitHub.png" 
alt="https://www.packtpub.com/" border="5" /></a>


## Instructions and Navigations
All of the code is organized into folders. For example, Chapter02.

The code will look like the following:
```
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    bio = models.TextField()
    
	class Meta:
        indexes = [
            models.Index(fields=['first_name']),
        ]
```

**Following is what you need for this book:**

This book is for Python and Django developers who aspire to elevate their Django skills to an advanced level. It assumes an intermediate level of proficiency in Python and Django programming and aims to impart comprehensive knowledge on optimizing the production environment and utilizing associated toolsets. By implementing these best practices, you will enhance the efficiency, robustness, and scalability of your production systems, thereby accelerating your career growth and professional development.

With the following software and hardware list you can run all code files present in the book (Chapter 1-14).

## Software and Hardware List

| Chapter  | Software required                                      | OS required                   |
| -------- | -------------------------------------------------------| ------------------------------|
| 1-14     | Python 3.10 and above                                  | Windows, macOS, or Linux      |
| 1-14     | Django 4.x, Django 5.0 and above                       | Windows, macOS, or Linux      |
| 1-14     | Docker, Amazon Web Services (AWS), ElephantSQL, Neon   | Windows, macOS, or Linux      |


## Related products <Other books you may enjoy>
* Django 5 By Example [[Packt]](https://www.packtpub.com/product/django-5-by-example-fifth-edition/9781805125457) [[Amazon]](https://www.amazon.in/dp/1805125451)

* Mastering Flask Web Development [[Packt]](https://www.packtpub.com/product/mastering-flask-web-development/9781837633227) [[Amazon]](https://www.amazon.in/dp/1837633223)

## Get to Know the Author
**Arghya(argo) Saha**
is a software developer with 8+ years of experience and has been working with Django since 2015. Apart from Django, he is proficient in JavaScript, ReactJS, Node.js, Postgres, AWS, and several other technologies. He has worked with multiple start-ups, such as Postman and HealthifyMe, among others, to build applications at scale. He currently works at Abnormal Security as a senior Site Reliability Engineer to explore his passion in the infrastructure domain.
In his spare time, he writes tech blogs. He is also an adventurous person who has done multiple Himalayan treks and is an endurance athlete with multiple marathons and triathlons under his belt.

## For doubts and feedback
> [!NOTE]
> 
> Join the Discord server "[Django in Production](https://discord.gg/FCrGUfmDyP)" for direct support from the author as you follow the instructions in the book. Feel free to reach out for any help or clarifications needed. https://discord.gg/FCrGUfmDyP.
