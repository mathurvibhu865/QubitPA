from django.shortcuts import render,redirect,get_object_or_404
from .models import Brand,Category
from django.views import View
from .models import Product,ProductImages
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
#from .views import brand_list


def recommend_products(product_id, num_recommendations=5):
    # Get all products
    products = Product.objects.all().values('id', 'name', 'description', 'features')
    df = pd.DataFrame(list(products))

    # Use TF-IDF to vectorize text features
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(df['description'] + ' ' + df['features'].astype(str))

    # Find similarity for the given product
    
    product_index = df[df['id'] == product_id].index[0]
    cosine_sim = cosine_similarity(tfidf_matrix[product_index], tfidf_matrix).flatten()

    # Get top N recommendations
    similar_indices = cosine_sim.argsort()[-num_recommendations - 1:-1][::-1]
    # recommended_products = df.iloc[similar_indices]
    recommended_ids = df.iloc[similar_indices]['id'].tolist()

    # Fetch recommended products as a queryset
    recommended_products = Product.objects.filter(id__in=recommended_ids)
    return recommended_products

def brand_list(request):
    data= Brand.objects.all()
    context ={
        'brands' : data
    }
    return render(request,'product/brand_list.html',context)


class AddProduct(View):
    def get(self,request):
        brands = Brand.objects.all()
        context = {
            'brands':brands
        }
        return render(request,'product/create_product.html',context)
    def post(self,request):
        print(request.POST)
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        brand = request.POST.get('brand')
        Product.objects.create(
            name=name,
            price_inclusive = price,
            description = description,
            brand= Brand.objects.get(name= brand),
            features = ''
            )
        return redirect('/')

# def brand_list(request):
#      data= Brand.objects.all()
#      context ={


#          'brands' : data
#      }
#      return render(request,'product/brand_list.html',context)



def fetch_image_in_dictionary(image_obj,product_obj):
    result = dict()
    for image in image_obj:
        if (len(result)==2):
                break
        if image.product.id == product_obj.id:
                result[chr(65+len(result))]=image
    return result


from typing import List, Dict

def get_product_with_images(products_objects: List[Product], images: List[ProductImages]) -> List[Dict]:
    """
    This function takes a list of product objects and image objects, and returns a combined list of products with images.
    """
    products = []  # Empty list to hold combined results
    for product_obj in products_objects:
        image = fetch_image_in_dictionary(images, product_obj)  # Assuming fetch_image_in_dictionary is already defined
        products.append({
            'details': product_obj,
            'images': image
        })
    return products



def product_list(request):
    products_objects= Product.objects.all()#fetching all records from product model/table
    images = ProductImages.objects.all()#fetching all records from productImage model/table
    # products=[]                          #emptu list for result
    # for product_obj in products_objects:
    #     image = fetch_image_in_dictionary(images,product_obj)#fetchin 2 image for each product
    #     products.append( {
    #         'details':product_obj,
    #         'images': image
    #     })
    products = get_product_with_images(products_objects, images)
    categories = Category.objects.all()#fetching all records from category model/table
    context ={
        'products' : products,
        'categories':categories,
    }
    return render(request,'product/shop.html',context)
from .models import UserInteraction
from django.utils.timezone import now, timedelta
def product_details(request,id):
    product  = get_object_or_404(Product,id = id)
    images = ProductImages.objects.filter(product = product)
    if request.user.is_authenticated:
        # Define the time threshold (e.g., 24 hours)
        time_threshold = now() - timedelta(hours=24)

        # Check for an existing interaction within the time threshold
        interaction = UserInteraction.objects.filter(
            user=request.user,
            product=product,
            interaction_type='view',
            timestamp__gte=time_threshold
        ).first()

        if interaction:
            # If interaction exists within the time period, increment the count
            interaction.count += 1
            interaction.timestamp = now()  # Update the timestamp
            interaction.save()
        else:
            # Create a new interaction record if none exist within the time period
            UserInteraction.objects.create(
                user=request.user,
                product=product,
                interaction_type='view',
                count=1,
                timestamp=now()
            )

    # recommended_products = recommend_products(product.id)
    # recommended_images = ProductImages.objects.filter(product = recommended_products)
    recommended_products = recommend_products(product.id)  # Get recommended products for the given product
    
    recommended_images = ProductImages.objects.filter(product__in=recommended_products)  # Filter images for recommended products
    
    # Get recommended products with images using the utility function
    recommended_products_with_images = get_product_with_images(recommended_products, recommended_images)
    
    print(recommended_products)
    context = {
        'product':product,
        'images':images,
        'recommended_products': recommended_products_with_images,
    }
    return render(request,'product/product_details.html',context)


def update_product(request,id):
    product  = get_object_or_404(Product,id = id)
    brands = Brand.objects.all()
    if request.method == 'GET':
        context = {
            'product':product,
            'brands':brands
        }
        return render(request,'product/update_product.html',context)
    elif request.method =="POST":
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        brand = request.POST.get('brand')
        product.name= name
        product.price_inclusive = price
        product.description = description
        product.brand = Brand.objects.get(name= brand)
        product.save()
        return redirect( 'product_list' )


from .forms import BrandCreationForm,ProductCreationForm
def add_brand(request):
    brand_form = BrandCreationForm()
    context={
        'form':brand_form,
        'entity':'Brand'
    }
    return render(request,'product/add_entity.html',context)

def add_product_with_django_form(request):
    product_form = ProductCreationForm()
    context={
        'form':product_form,
        'entity':'Product'
    }
    return render(request,'product/add_entity.html',context)

