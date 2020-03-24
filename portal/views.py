from django.shortcuts import render, HttpResponse, redirect, reverse
from .models import Category, Post, Tag

from bs4 import BeautifulSoup
import requests
import time
from fake_useragent import UserAgent
import wget


def home_view(request):
    context = {
        'posts': Post.objects.all()[5:19],
        'four_posts': Post.objects.filter(status='draft')[:4],
    }
    # print(context)
    return render(request, 'portal/index.html', context)


def scrape(request):
    ua = UserAgent()
    response = requests.get('https://www.theverge.com/', headers={'User-Agent': ua.chrome})
    soup = BeautifulSoup(response.content, 'lxml')
    
    block_h2 = soup.find_all('h2', attrs={'class': 'c-entry-box--compact__title'})

    for i in block_h2:
        link = i.a['href']
        time.sleep(1)
        try:
            response = requests.get(link, headers={'User-Agent': ua.chrome})
            soup = BeautifulSoup(response.content, 'lxml')
            
            title = soup.find('h1', attrs={'class': 'c-page-title'}).text
            tags =[i.a.span.text for i in soup.find_all('li', attrs={'class': 'c-entry-group-labels__item'})]

            category = []

            if len(tags) == 1:
                category.append(tags[0])

            elif len(tags) > 1:
                category.append(tags[1])

            category = ''.join(category)
            # print(tags)

            img = []
            
            try:
                image = soup.find('figure', attrs={'class': 'e-image e-image--hero'}).find('span', class_='e-image__image')['data-original']
                img.append(image)
            except:
                import random
                img_uns = []
                list_tag = ['Technology', 'Network', 'Data', 'Future', 'Design', 'Abstract']

                print(f'Пытаюсь взять фото с другого источника по случайному тегу из: {tags}')
                if tags:
                    random_tag = random.choice(tags)
                    ua_n = UserAgent()
                    response_n = requests.get(f'https://unsplash.com/s/photos/{random_tag}', headers={'User-Agent': ua_n.chrome})
                    
                    print(response_n.url)
                    soup_n = BeautifulSoup(response_n.content, 'lxml')
                    list_images = soup_n.find('div', attrs={'class': '_2HheS _2sCnE PrOBO _1CR66'})

                    try:
                        for i in list_images.find_all('div', class_='nDTlD'):
                            a = i.find('div', class_='_232xU').find('div', class_='IEpfq').find('img')['src']
                            img_uns.append(a)
                            print(a)
                    except:
                        pass
                else:
                    random_tag = random.choice(list_tag)
                    ua_n = UserAgent()
                    response_n = requests.get(f'https://unsplash.com/s/photos/{random_tag}', headers={'User-Agent': ua_n.chrome})
                    
                    print(response_n.url)
                    soup_n = BeautifulSoup(response_n.content, 'lxml')
                    list_images = soup_n.find('div', attrs={'class': '_2HheS _2sCnE PrOBO _1CR66'})

                    try:
                        for i in list_images.find_all('div', class_='nDTlD'):
                            a = i.find('div', class_='_232xU').find('div', class_='IEpfq').find('img')['src']
                            img_uns.append(a)
                            print(a)
                    except:
                        pass

                if img_uns == []:
                    random_tag = random.choice(list_tag)
                    print(f'Список пуст. Пробую по другому тегу {random_tag}')
                    response_nn = requests.get(f'https://unsplash.com/s/photos/{random_tag}', headers={'User-Agent': ua.chrome})

                    print(response_nn.url)
                    soup_nn = BeautifulSoup(response_nn.content, 'lxml')
                    list_images_n = soup_nn.find('div', attrs={'class': '_2HheS _2sCnE PrOBO _1CR66'})

                    try:
                        for i in list_images_n.find_all('div', class_='nDTlD'):
                            a = i.find('div', class_='_232xU').find('div', class_='IEpfq').find('img')['src']
                            img_uns.append(a)
                            print(a)
                    except:
                        pass

                # print(f'ПОЛУЧЕННЫЙ СПИСОК {img_uns}')
                img.append(random.choice(img_uns))
                # print(f'СЛУЧАЙНОЕ ФОТО : {img}')
            img = ''.join(img)

            content = soup.find('div', class_='c-entry-content')
            # print(content)
            tmp_content = []
            for i in content.find_all(['p', 'img']):
                tmp_content.append(i.text)
                try:
                    img = i['src']
                    tmp_content.append(img)
                except:
                    pass
        except:
            pass
        
        # print('=====================================================')
        print(title)
        print(category)
        print(link)
        print(img)

        try:
            path_to_media = 'D:/NEW_20/MEDIA_PORTAL/django/media/images'
            temp_post = Post()
            temp_category, _ = Category.objects.get_or_create(name=category)

            temp_post.category = temp_category
            temp_post.author = request.user
            
            temp_post.title = title
            temp_post.raw_title = title
            temp_post.link_new = link
            temp_post.body = '\n'.join(tmp_content)
            temp_post.raw_body = '\n'.join(tmp_content)
            # temp_post.image = wget.download(image, path_to_media)
            for i in tags:
                tmp_tag, _ = Tag.objects.get_or_create(name=i)

            if not Post.objects.filter(raw_title=temp_post.raw_title).exists():
                temp_post.image = wget.download(img, path_to_media)
                temp_post.save()

                for i in tags:
                    temp_tag, _ = Tag.objects.get_or_create(name=i)
                    temp_post.tags.add(temp_tag)
                temp_post.save()

        except Exception as err:
            import traceback
            print('Ошибка:\n', traceback.format_exc())
            # print(f'ОШИБКА: ===== > {err.__class__}')
            print(f'В ссылке {link}')
            pass

        

        print('===================== DONE ==========================')

        

        # break  

    # return HttpResponse('OK')  
    return redirect('home')  

        


