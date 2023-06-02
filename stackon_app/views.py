import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import NFTAsset, NFTPosts, Geek, Accounts, Assets, FilteredAssets, Feature, LiveStream, Contract
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from decimal import Decimal
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from datetime import timedelta
from django.utils import timezone
from django.template.defaultfilters import timesince
import json
from django.contrib.auth.hashers import check_password


@csrf_exempt
def check_password_correct(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        user = request.user
        
        is_password_correct = check_password(password, user.password)
        return JsonResponse({'is_password_correct': is_password_correct})


def nft_assets(request):
    assets = NFTAsset.objects.all()
    data = []
    for asset in assets:
        data.append({
            'name': asset.name,
            'image': asset.image,
            'volume': asset.volume,
            'current_price': asset.current_price,
            'sentiment': asset.sentiment,
            'next_1d_percent': asset.next_1d_percent,
            'next_3d_percent': asset.next_3d_percent,
            'next_7d_percent': asset.next_7d_percent,
            'accuracy': asset.accuracy,
            'trend': asset.trend,
        })
    return JsonResponse(data, safe=False)

def nft_posts(request):
    posts = NFTPosts.objects.all()
    data = []
    for post in posts:
        data.append({
            'display_name': post.display_name,
            'user': post.user_name,
            'avatar': post.avatar,
            'timestamp': post.timestamp,
            'post': post.post
        })
    
    return JsonResponse(data, safe=False)

@csrf_exempt
def playground(request):
    try: 
        if request.user.is_authenticated:
            current_user = User.objects.get(username=request.user)
            print(current_user)
            print("WORKED")
            profile = Accounts.objects.get(user=current_user)
            user_short = str(profile.wallet_address)
            user_short = user_short[:20]
            print(user_short)

        context = {
            'profile': profile,
            'user_short': user_short,
        }
        return render(request, 'playground.html', context=context)
    except:
        print("FAILED")
        return render(request, 'playground.html')

@csrf_exempt
def landing(request):
    return render(request, 'landing.html')

def generate_text(filtered_values):
    sentence_parts = []

    for key, value in filtered_values.items():
        if key == 'blockchain__in':
            blockchains = ', '.join(value)
            sentence_parts.append(f"on the {blockchains} blockchain")
            continue

        if key == 'regulations':
            if value == 'True':
                sentence_parts.append(f"had recent regulation")
            continue
    
        if key == 'partnerships':
            if value == 'True':
                sentence_parts.append(f"had recent partnership")
            continue

        if key == 'technology_updates':
            if value == 'True':
                sentence_parts.append(f"had recent technology update or upgrade")
            continue

        if key == 'security_incidents':
            if value == 'True':
                sentence_parts.append(f"had recent security incidents")
            continue 

        if key == 'floor_price_range':
            floor_price_map = {
                'ZEROFIFTY': '$0 - $49',
                'FIFTYHUNDRED': '$50 - $99',
                'THOUSAND': '$100 - $999',
                'HUNDREDTHOUSAND': '$1000 - $99,999',
                'MILLION': '$99,999 and above'
            }
            floor_price = floor_price_map.get(value, 'Unknown')
            sentence_parts.append(f"floor price is {floor_price}")
            continue

        if key == 'volume_traded_range':
            volume_map = {
                'BELOW10THOUSAND': 'below $10,000',
                'FROM10_100THOUSAND': '$10,000 - $99,999',
                'FROM100_1MILLION': '$100,000 - $999,999',
                'FROM1_50MILLION': '$1,000,000 - $49,999,999',
                'FROM50_500MILLION': '$50,000,000 - $499,999,999',
                'FROM500_1BILLION': '$500,000,000 - $999,999,999',
                'ABOVE1BILLION': '$1,000,000,000 and above'
            }
            volume = volume_map.get(value, 'Unknown')
            sentence_parts.append(f"volume traded is {volume}")
            continue

        if key == 'launch_time':
            launch_time_map = {
                'ONEMONTH': 'Last 1 Month',
                'THREEMONTH': 'Last 3 Months',
                'SIXMONTH': 'Last 6 Months',
                'ONEYEAR': 'Last 1 year',
                'TWOYEARS': 'Last 2 years',
                'FIVEYEARS': 'Last 5 years'
            }
            launch_time = launch_time_map.get(value, 'Unknown')
            sentence_parts.append(f"launch time is {launch_time}")
            continue 

        sentence_parts.append(f"{key.replace('_', ' ')} sentiment is {value}")

    sentence = "None"
    if sentence_parts != []:
        print(sentence_parts)
        sentence = "These are all available NFTs that " + ", ".join(sentence_parts) + "."
    
    return sentence 

def generate_description_text(nft):
    features = nft.nft_features.all() if nft else []
    description_parts = []

    if features:
        description_parts.append(f"{nft.nft_name} is part of the 1000 total supply from the {nft.nft_collection} and can allow you to ")

        if features.filter(name="Twitter").exists():
            description_parts.append("access sentiment data from twitter feeds,")
        
        if features.filter(name="Reddit").exists():
            description_parts.append("access sentiment data from reddit discussions,")

        if features.filter(name="Discord").exists():
            description_parts.append("access sentiment data from investors channel(s) on discord,")

        if features.filter(name="Telegram").exists():
            description_parts.append("access sentiment data from investors channel(s) on telegram,")

        if features.filter(name="c-Telegram").exists():
            description_parts.append(" add Stackon Geek Bot to your telegram channel to scrape data and earn from it")

        if features.filter(name="c-Discord").exists():
            description_parts.append(" add Stackon Geek Bot to your Discord channel to scrape data and earn from it")

        if features.filter(name="Stream").exists():
            description_parts.append(" stream your Geek sentiment analysis to investors,")

        if features.filter(name="Watch").exists():
            description_parts.append(" watch exclusive videos from previous Geek streams on Stackon Ecosystem.")

        if features.filter(name="Theta").exists():
            description_parts.append(" use Stackon Modifiers on all verifible NFTs on Theta Blockchain -TDROP Markeplace also to stream your Geek sentiment analysis to investors and watch exclusive videos from previous Geek streams on Stackon Ecosystem.")

        if features.filter(name="Ethereum").exists():
            description_parts.append(" use Stackon Modifiers on all verifible NFTs on Ethereum Blockchain and watch exclusive videos from previous Geek streams on Stackon Ecosystem.")
        
        if features.filter(name="Polygon").exists():
            description_parts.append(" use Stackon Modifiers on all verifible NFTs on Polygon Blockchain and watch exclusive videos from previous Geek streams on Stackon Ecosystem.")

        if features.filter(name="Solana").exists():
            description_parts.append(" use Stackon Modifiers on all verifible NFTs on Solana Blockchain and watch exclusive videos from previous Geek streams on Stackon Ecosystem.")

        if features.filter(name="BNB").exists():
            description_parts.append(" use Stackon Modifiers on all verifible NFTs on BNB Blockchain and watch exclusive videos from previous Geek streams on Stackon Ecosystem.")

        if features.filter(name="Tezos").exists():
            description_parts.append(" use Stackon Modifiers on all verifible NFTs on Tezos Blockchain and watch exclusive videos from previous Geek streams on Stackon Ecosystem.")

        if features.filter(name="Allblockchain").exists():
            description_parts.append(" use Stackon Modifiers on all verifible NFTs on Ethereum, Theta, Polygon, Solana, BNB and Tezos Blockchain and watch exclusive videos from previous Geek streams on Stackon Ecosystem.")

        # Add more conditions for other features 

    if description_parts:
        description_text = "\n".join(description_parts)
    else:
        description_text = "No additional features available."

    return description_text

def generate_pre_description_text(nft):
    # Get the features of the nft
    features = nft.nft_features.all()

    # Sort the features based on their IDs
    sorted_features = sorted(features, key=lambda x: x.id)

    # Select the top 3 features or all features if less than 3
    selected_features = sorted_features[:3]

    # Concatenate the feature names with "|"
    feature_names = " | ".join(feature.name for feature in selected_features)

    # Add a suffix if there are more features
    if len(features) > 3:
        feature_names += f" | ... +{len(features) - 3}"

    return feature_names

def features_dict(request):
    current_user = User.objects.get(username=request.user)
    profile = Accounts.objects.get(user=current_user)
    all_features = Feature.objects.all()
    feature_dict = {}

    for feature in all_features:
        is_selected = feature in profile.stack.all()
        feature_dict[feature.name.lower()] = is_selected
    
    return JsonResponse(feature_dict)

@csrf_exempt
def add_features(request):
    if request.method == 'POST':
        current_user = User.objects.get(username=request.user)
        profile = Accounts.objects.get(user=current_user)
        features = []
        for key, value in request.POST.items():
            if key == 'True':
                try:
                    feature = Feature.objects.get(name=value)
                    features.append(feature.id)
                except Feature.DoesNotExist:
                    pass
                
        print('ADDED FEATURE')
        print(features)

         # Add each feature individually to the stack
        for feature in features:
            profile.stack.add(feature)
            
        return HttpResponse('Features added successfully')

@csrf_exempt
def stacks_view(request):
    try: 
        if request.user.is_authenticated:
            current_user = User.objects.get(username=request.user)
            profile = Accounts.objects.get(user=current_user)

            user_short = str(profile.wallet_address)
            user_short = user_short[:12]
            try:
                filtered_assets_instance =  FilteredAssets.objects.get(profile=request.user) 
            except:
                filtered_assets_instance = FilteredAssets.objects.create(profile=request.user) 
            
            if filtered_assets_instance:
                filtered_assets = filtered_assets_instance.filtered_assets  # Access the filtered_assets field
                
                filtered_assets_texts = filtered_assets_instance.filtered_assets_texts 
            else:
                filtered_assets = []
    
    except Exception as e: 
        print(str(e))
        print("FAILED")
        return render(request, 'stacks.html')
    context = {
                'profile': profile,
                'assets': filtered_assets,
                'user_short': user_short,
                'geek_text': filtered_assets_texts,
               
            }    
    return render(request, 'stacks.html', context)

@csrf_exempt
def stacks(request):
    try: 
        if request.user.is_authenticated:
            current_user = User.objects.get(username=request.user)
            profile = Accounts.objects.get(user=current_user)
            stack = profile.stack.all()
            user_short = str(profile.wallet_address)
            user_short = user_short[:12]
            # assets = Assets.objects.all().order_by('-trend_percent')
            filtered_assets_instance, created = FilteredAssets.objects.get_or_create(profile=request.user) # Retrieve the first instance from the database
            
            if filtered_assets_instance:
                filtered_assets = filtered_assets_instance.filtered_assets  # Access the filtered_assets field
                
            else:
                filtered_assets = []
          
            if request.method == 'POST':
                ethereum = request.POST.get('ethereum')
                theta = request.POST.get('theta')
                solana = request.POST.get('solana')
                polygon = request.POST.get('polygon')
                bnb = request.POST.get('bnb')
                tezos = request.POST.get('tezos')
                floorPrice = request.POST.get('floorPrice')
                rarity = request.POST.get('rarity')
                volume = request.POST.get('volume')
                launchTime = request.POST.get('launchTime')
                regulations = request.POST.get('regulations')
                partnerships = request.POST.get('partnerships')
                technologyUpdates = request.POST.get('technologyUpdates')
                securityIncidents = request.POST.get('securityIncidents')
                allInfluencers = request.POST.get('allInfluencers')
                allInvestors = request.POST.get('allInvestors')
                allFounders = request.POST.get('allFounders')
                allCommunity = request.POST.get('allCommunity')
                allSocialMedia = request.POST.get('allSocialMedia')
                twitterInfluencers = request.POST.get('twitterInfluencers')
                twitterInvestors = request.POST.get('twitterInvestors')
                twitterFounders = request.POST.get('twitterFounders')
                twitterCommunity = request.POST.get('twitterCommunity')
                allTwitter = request.POST.get('allTwitter')
                redditInfluencers = request.POST.get('redditInfluencers')
                redditInvestors = request.POST.get('redditInvestors')
                redditFounders = request.POST.get('redditFounders')
                redditCommunity = request.POST.get('redditCommunity')
                allReddit = request.POST.get('allReddit')
                telegramInfluencers = request.POST.get('telegramInfluencers')
                telegramInvestors = request.POST.get('telegramInvestors')
                telegramFounders = request.POST.get('telegramFounders')
                telegramCommunity = request.POST.get('telegramCommunity')
                allTelegram = request.POST.get('allTelegram')
                discordInfluencers = request.POST.get('discordInfluencers')
                discordInvestors = request.POST.get('discordInvestors')
                discordFounders = request.POST.get('discordFounders')
                discordCommunity = request.POST.get('discordCommunity')
                allDiscord = request.POST.get('allDiscord')


                filter_conditions = {}
                # FILTER BLOCKCHAIN
                blockchains = []
                if ethereum != 'none':
                    blockchains.append(ethereum)
                if theta != 'none':
                    blockchains.append(theta)
                if solana != 'none':
                    blockchains.append(solana)
                if polygon != 'none':
                    blockchains.append(polygon)
                if tezos != 'none':
                    blockchains.append(tezos)
                if bnb != 'none':
                    blockchains.append(bnb)

                if blockchains:
                    filter_conditions['blockchain__in'] = blockchains

                # FILTER FLOOR PRICE
                if floorPrice != 'none':
                    filter_conditions['floor_price_range'] = floorPrice

                # FILTER RARITY
                if rarity != 'none':
                    filter_conditions['rarity'] = rarity

                # FILTER VOLUME TRADED
                if volume != 'none':
                    filter_conditions['volume_traded_range'] = volume
                
                # FILTER LAUNCH TIME
                if launchTime != 'none':
                    filter_conditions['launch_time'] = launchTime
                
                # FILTER REGULATIONS
                if regulations != 'none':
                    filter_conditions['regulations'] = regulations
                
                # FILTER PARTNERSHIPS
                if partnerships != 'none':
                    filter_conditions['partnerships'] = partnerships

                # FILTER TECHNOLOGY UPDATES
                if technologyUpdates != 'none':
                    filter_conditions['technology_updates'] = technologyUpdates
                
                # FILTER SECURITY INCIDENTS 
                if securityIncidents != 'none':
                    filter_conditions['security_incidents'] = securityIncidents

                # FILTER ALL INFLUENCERS
                if allInfluencers != 'none':
                    filter_conditions['overall_influencers'] = allInfluencers
                if allInvestors != 'none':
                    filter_conditions['overall_investors'] = allInvestors 
                if allFounders != 'none':
                    filter_conditions['overall_founders'] = allFounders
                if allCommunity != 'none':
                    filter_conditions['overall_community'] = allCommunity
                if allSocialMedia != 'none':
                    filter_conditions['overall_social_media'] = allSocialMedia
                
                # FILTER TWITTER 
                if twitterInfluencers != 'none':
                    filter_conditions['twitter_influencers'] = twitterInfluencers
                if twitterInvestors != 'none':
                    filter_conditions['twitter_investors'] = twitterInvestors
                if twitterFounders != 'none':
                    filter_conditions['twitter_founders'] = twitterFounders
                if twitterCommunity != 'none':
                    filter_conditions['twitter_community'] = twitterCommunity
                if allTwitter != 'none':
                    filter_conditions['overall_twitter'] = allTwitter
                
                # FILTER REDDIT 
                if redditInfluencers != 'none':
                    filter_conditions['reddit_influencers'] = redditInfluencers
                if redditInvestors != 'none':
                    filter_conditions['reddit_investors'] = redditInvestors
                if redditFounders != 'none':
                    filter_conditions['reddit_founders'] = redditFounders
                if redditCommunity != 'none':
                    filter_conditions['reddit_community'] = redditCommunity
                if allReddit != 'none':
                    filter_conditions['overall_reddit'] = allReddit

                # FILTER TELEGRAM
                if telegramInfluencers != 'none':
                    filter_conditions['telegram_influencers'] = telegramInfluencers
                if telegramInvestors != 'none':
                    filter_conditions['telegram_investors'] = telegramInvestors
                if telegramFounders != 'none':
                    filter_conditions['telegram_founders'] = telegramFounders
                if telegramCommunity != 'none':
                    filter_conditions['telegram_community'] = telegramCommunity
                if allTelegram != 'none':
                    filter_conditions['overall_telegram'] = allTelegram

                # FILTER DISCORD
                if discordInfluencers != 'none':
                    filter_conditions['discord_influencers'] = discordInfluencers
                if discordInvestors != 'none':
                    filter_conditions['discord_investors'] = discordInvestors
                if discordFounders != 'none':
                    filter_conditions['discord_founders'] = discordFounders
                if discordCommunity != 'none':
                    filter_conditions['discord_community'] = discordCommunity 
                if allDiscord != 'none':
                    filter_conditions['overall_discord'] = allDiscord

                print(filter_conditions)
                new_text = generate_text(filter_conditions)

                # Query the Assets model using the filter conditions
                filtered_assets = Assets.objects.filter(**filter_conditions).order_by('-trend_percent')

                # Serialize the filtered assets into JSON
                serialized_assets = [{'name': asset.name, 'image': asset.image, 'description': asset.description, 'trend_percent': float(asset.trend_percent), 'blockchain_logo': asset.blockchain_logo, 'floor_price':float(asset.floor_price), 'volume_traded':asset.volume_traded } for asset in filtered_assets]

                # Create an instance of FilteredAssets model and save the serialized assets
                filtered_instance, created = FilteredAssets.objects.get_or_create(profile=request.user)
                filtered_instance.filtered_assets = serialized_assets
                filtered_instance.filtered_assets_texts = new_text
                filtered_instance.save()
                
                
       
    except Exception as e: 
        print(str(e))
        print("FAILED")
        return render(request, 'stacks.html')
    
    # context = {
    #             'profile': profile,
    #             'assets': filtered_assets,
    #             'user_short': user_short,
    #         }    
    return redirect('stacks_view')
    
@csrf_exempt
def index(request):
    assets = Assets.objects.order_by('pk')[:20]
    posts = NFTPosts.objects.all()
    nft_items = Geek.objects.all()

    context = {
                'assets': assets,
                'posts': posts,   
                'nft_items': nft_items,
                
            }

    if request.user.is_authenticated:
        current_user = User.objects.get(username=request.user)
        profile = Accounts.objects.get(user=current_user)
        user_short = str(profile.wallet_address)
        user_short = user_short[:12]
        contract = Contract.objects.first()
        context = {
                'assets': assets,
                'posts': posts,   
                'nft_items': nft_items,
                'profile': profile,
                'user_short': user_short,
                'contract': contract,
            }

   
    return render(request, 'index.html', context=context)

@csrf_exempt
def livestream(request):

    assets = Assets.objects.order_by('pk')[:20]
    posts = NFTPosts.objects.all()
    nft_items = Geek.objects.all()
    

    context = {
                'assets': assets,
                'posts': posts,   
                'nft_items': nft_items,
            
                
            }

    if request.user.is_authenticated:
        current_user = User.objects.get(username=request.user)
        profile = Accounts.objects.get(user=current_user)
        user_short = str(profile.wallet_address)
        user_short = user_short[:12]
        
        livestreams = LiveStream.objects.all()
        for live in livestreams:
            live.time_stamp = timesince(live.start_time, timezone.now())
            live.save()

        livestream = LiveStream.objects.all()
        context = {
                'assets': assets,
                'posts': posts,   
                'nft_items': nft_items,
                'profile': profile,
                'user_short': user_short,
                'livestream': livestream
            }
    return render(request, 'livestream.html', context=context)

@csrf_exempt
def delete_stream(request):
    if request.method == 'POST':
        current_user = User.objects.get(username=request.user)
        profile = Accounts.objects.get(user=current_user)

        livestream = get_object_or_404(LiveStream, creator=profile)
        livestream.delete()
        return HttpResponse('Livestream deleted successfully')
    
    return HttpResponse('Invalid request')
@csrf_exempt
def start_stream(request):
    if request.method == 'POST':
        stream_url = "https://player.thetavideoapi.com/video/video_5uzztb9hf84m5bvppyisrqiy3v"
        stream_title = request.POST.get('streamTitle')
        stream_description = request.POST.get('streamDescription')
        stream_api_key = request.POST.get('streamAPIKey')
        stream_secret_key = request.POST.get('streamSecretKey')
        print(stream_title)
        print(stream_description)


         # Set the start_time to the current time
        start_time = timezone.now()
        time_difference = timesince(start_time, timezone.now())

        # Set the end_time to be 1 hour later than the start_time
        end_time = start_time + timedelta(hours=1)

        if request.user.is_authenticated:
            current_user = User.objects.get(username=request.user)
            profile = Accounts.objects.get(user=current_user)

            profile.api_key = stream_api_key
            profile.secret_key =  stream_secret_key
            profile.save()
            try: 
                # Retrieve the existing LiveStream object for the user
                livestream = LiveStream.objects.get(creator=profile)

                livestream.url = stream_url
                livestream.title = stream_title
                livestream.description = stream_description
                livestream.start_time = start_time
                livestream.end_time = end_time
                livestream.badges = 0
                livestream.status = 'LIVE'
                livestream.time_stamp = time_difference
                livestream.save()
                
            except LiveStream.DoesNotExist:
                livestream = LiveStream(url=stream_url, creator=profile, title= stream_title, description=stream_description, badges=0, status='LIVE', time_stamp=time_difference, start_time=start_time, end_time=end_time)
                livestream.save()
    return redirect('livestream')

@csrf_exempt
def community(request):

    assets = Assets.objects.order_by('pk')[:20]
    posts = NFTPosts.objects.all()
    nft_items = Geek.objects.all()

    context = {
                'assets': assets,
                'posts': posts,   
                'nft_items': nft_items,
                
            }

    if request.user.is_authenticated:
        current_user = User.objects.get(username=request.user)
        profile = Accounts.objects.get(user=current_user)
        user_short = str(profile.wallet_address)
        user_short = user_short[:12]
        context = {
                'assets': assets,
                'posts': posts,   
                'nft_items': nft_items,
                'profile': profile,
                'user_short': user_short,
            }
    return render(request, 'community.html', context=context)

@csrf_exempt
def storefront(request):
    assets = NFTAsset.objects.order_by('pk')[:20]
    nft_items = Geek.objects.all()
    current_user = User.objects.get(username=request.user)
    profile = Accounts.objects.get(user=current_user)
    profile.update_free_mint()
    profile.save()
    free_mint = 3 - profile.free_mint 
    print(free_mint)
    contract = Contract.objects.first()
    user_short = str(profile.wallet_address)
    user_short = user_short[:12]
    geeks = Geek.objects.all()
    for geek in geeks:
        Geek.convert_tfuel_to_usd(geek)
    abi = json.dumps(contract.stackonModCollectionContractABI)
 
    for geek in geeks:
        description_text = generate_description_text(geek)
        pre_description = generate_pre_description_text(geek)
        geek.nft_pre_description = pre_description
        geek.nft_description = description_text
        geek.save()
   
    context = {   
            'nft_items': nft_items, 
            'assets': assets,
            'profile': profile,
            'user_short': user_short,
            'contract': contract,
            'abi':abi,
            'free_mint': free_mint
        }
    return render(request, 'storefront.html', context=context)

@csrf_exempt
def disconnect(request):
    logout(request)
    request.user = None
    return redirect('index')

@csrf_exempt
def disconnect_playground(request):
    logout(request)
    request.user = None
    return redirect('playground')

@csrf_exempt
def create_wallet(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('wallet_address')
            password = request.POST.get('password')
            mnemonicPhrase = request.POST.get('mnemonicPhrase')
            privateKey = request.POST.get('privateKey')
            
            new_user = User.objects.create_user(username=username, password=password)
            new_user_info = Accounts.objects.create(user=new_user, wallet_address = username, mnemonic_phrase=mnemonicPhrase, private_key=privateKey )
            
            return redirect('index')
        except:
            return redirect('index')
            
    return render(request, 'index.html')

@csrf_exempt
def connect(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('wallet_address')
            password = request.POST.get('password')
            
            privateKey = request.POST.get('privateKey')
            
            
            print(password)
            print(username)

            user_exists = User.objects.filter(username=username).exists()
            if user_exists:
                authenticated_user = authenticate(request, username=username, password=password) 
                if authenticated_user is not None:
                    login(request, authenticated_user)
                    return redirect('index')

            else:
                new_user = User.objects.create_user(username=username, password=password)
                new_user_info = Accounts.objects.create(user=new_user, wallet_address = username, private_key=privateKey)
                authenticated_user = authenticate(request, username=username, password=password) 
                if authenticated_user is not None:
                    login(request, authenticated_user)

                return redirect('index')
        
        except:
            return redirect('index')
            
    return render(request, 'index.html')

@csrf_exempt
def connect_playground(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('wallet_address')
            user_exists = User.objects.filter(username=username).exists()
            print(username)
            print(user_exists)
            if user_exists:
                authenticated_user = authenticate(request, username=username) 
                if authenticated_user is not None:
                    login(request, authenticated_user)
                    return redirect('playground')

            else:
                new_user = User.objects.create_user(username=username)
                new_user_info = Accounts.objects.create(user=new_user)
                authenticated_user = authenticate(request, username=username) 
                if authenticated_user is not None:
                    login(request, authenticated_user)

                return redirect('playground')
        
        except:
            return redirect('playground')
            
    return render(request, 'playground.html')

def search(request):
    query = request.GET.get('query', '')
    results = NFTAsset.objects.filter(name__icontains=query)
    data = [{'id': r.id, 'name': r.name} for r in results]
    return JsonResponse(data, safe=False)

@csrf_exempt
def add_asset_to_stack(request):
    if request.method == 'POST':
        profile = get_object_or_404(Accounts, user =request.user)
        asset_name = request.POST.get('asset_name')
      
        asset = get_object_or_404(NFTAsset, name=asset_name)
        asset.asset_value = 0.0
        asset.save()
       
        profile.stack.add(asset)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

@csrf_exempt
def update_asset_value(request):
  if request.method == 'POST':
    asset_id = request.POST.get('asset_id')
    asset_value = request.POST.get('asset_value')
    if asset_value: 
        asset = get_object_or_404(NFTAsset, id=asset_id)
        asset.asset_value = Decimal(asset_value)
        asset.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})

@csrf_exempt
def delete_asset(request):
    if request.method == 'POST':
        asset_id = request.POST.get('asset_id')
        asset = get_object_or_404(NFTAsset, id=asset_id)
        profile = get_object_or_404(Accounts, user =request.user)
        profile.stack.remove(asset)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})
    

