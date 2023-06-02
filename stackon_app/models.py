from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
import random


class NFTPosts(models.Model):
    display_name = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    avatar = models.CharField(max_length=100)
    timestamp = models.CharField(max_length=10)
    post = models.TextField()
    social_media = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.display_name}"
    
class NFTAsset(models.Model):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=255, blank=True, null=True,)
    image = models.CharField(max_length=100)
    volume = models.DecimalField(max_digits=20, decimal_places=2)
    current_price = models.DecimalField(max_digits=20, decimal_places=2)
    asset_value = models.DecimalField(max_digits=20, decimal_places=3, default=0.0)
    sentiment = models.CharField(max_length=10)
    next_1d_percent = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    next_2d_percent = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    next_3d_percent = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    next_7d_percent = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    next_14d_percent = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    next_30d_percent = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    active_percent = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    accuracy = models.DecimalField(max_digits=5, decimal_places=2)
    trend = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"

class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wallet_avatar = models.CharField(max_length=100, default="avatar4.png")
    stack = models.ManyToManyField(NFTAsset, blank=True)
    api_key = models.TextField(blank=True)
    secret_key = models.TextField(blank=True)
    equity_eth = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    equity_usd = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    equity_change = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    equity_base = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    next_1d_change = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    next_2d_change = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    next_3d_change = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    next_7d_change = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    next_14d_change = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    next_30d_change = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    active_change = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)


    def __str__(self):
        return f"{self.user.username}"
    
    def get_stacks(self):
        return self.stack.all()

    def calculate_equity(self):
        # Calculate equity_eth
        assets = self.get_stacks()
        asset_values = [asset.asset_value for asset in assets]
        total_asset_value = sum(asset_values)
        self.equity_eth = total_asset_value

        # Calculate equity_usd
        eth_to_usd = Decimal('0.00054')
        self.equity_usd = round(self.equity_eth /  eth_to_usd, 2)

        # Calculate equity_change
        equity_change = Decimal(0)
        next_1d_change = Decimal(0)
        next_2d_change = Decimal(0)
        next_3d_change = Decimal(0)
        next_7d_change = Decimal(0)
        next_14d_change = Decimal(0)
        next_30d_change = Decimal(0)

        for stack in assets:
            equity_change += stack.next_1d_percent
            next_1d_change += stack.next_1d_percent
            next_2d_change += stack.next_2d_percent
            next_3d_change += stack.next_3d_percent
            next_7d_change += stack.next_7d_percent
            next_14d_change += stack.next_14d_percent
            next_30d_change += stack.next_30d_percent
            
        self.equity_change = equity_change
        self.next_1d_change = next_1d_change
        self.next_2d_change = next_2d_change
        self.next_3d_change = next_3d_change
        self.next_7d_change = next_7d_change
        self.next_14d_change = next_14d_change
        self.next_30d_change = next_30d_change
        

        # Calculate equity_base
        self.equity_base = self.equity_change * self.equity_eth 

class Feature(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Geek(models.Model):
    GEEKS = 'geeks'
    MODIFIERS = 'modifiers'
    STACKONBOTS = 'stackon-bots'
    STATUS_CHOICES = (
        (GEEKS, 'Geeks'),
        (MODIFIERS, 'Modifiers'),
        (STACKONBOTS, 'Stackon Bots'),
    )
    nft_status = models.CharField(max_length=100, choices=STATUS_CHOICES, default=GEEKS)
    nft_minting = models.BooleanField(default=False)
    nft_name = models.CharField(max_length=255, blank=True)
    nft_collection = models.CharField(max_length=255, blank=True)
    nft_image = models.CharField(max_length=100, null=True, blank=True)
    nft_seller = models.CharField(max_length=100, default="logo.ico")
    nft_features = models.ManyToManyField(Feature, blank=True)
    nft_pre_description = models.TextField(null=True, blank=True)
    nft_total_supply = models.TextField(null=True, blank=True)
    nft_description = models.TextField(null=True, blank=True)
    nft_price_tfuel = models.DecimalField(max_digits=10, decimal_places=2)
    nft_price_usd = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    
    def __str__(self):
        return self.nft_name
    
    def convert_tfuel_to_usd(self):
        conversion_rate = Decimal('0.04')
        usd_price = self.nft_price_tfuel * conversion_rate
        self.nft_price_usd = usd_price
        self.save()

class Assets(models.Model):
    NONE = 'None'
    POSITIVE = 'Positive'
    NEUTRAL = 'Neutral'
    NEGATIVE = 'Negative'
    TRUE = 'True'
    ETHEREUM = 'Ethereum'
    THETA = 'Theta'
    SOLANA = 'Solana'
    POLYGON = 'Polygon'
    BNB = 'BNB'
    TEZOS = 'Tezos'
    COMMON = 'Common'
    UNCOMMON = 'Uncommon'
    RARE = 'Rare'
    EPIC = 'Epic'
    LEGENDARY = 'Legendary'
    ONEMONTH = 'ONEMONTH'
    THREEMONTH = 'THREEMONTH'
    SIXMONTH = 'SIXMONTH'
    ONEYEAR = 'ONEYEAR'
    TWOYEARS = 'TWOYEARS'
    FIVEYEARS = 'FIVEYEARS'
    ZEROFIFTY = 'ZEROFIFTY'
    FIFTYHUNDRED = 'FIFTYHUNDRED'
    THOUSAND = 'THOUSAND'
    HUNDREDTHOUSAND = 'HUNDREDTHOUSAND'
    MILLION = 'MILLION'
    BELOW10THOUSAND = 'BELOW10THOUSAND'
    FROM10_100THOUSAND = 'FROM10_100THOUSAND'
    FROM100_1MILLION = 'FROM100_1MILLION'
    FROM1_50MILLION = 'FROM1_50MILLION'
    FROM50_500MILLION = 'FROM50_500MILLION'
    FROM500_1BILLION = 'FROM500_1BILLION'
    ABOVE1BILLION = 'ABOVE1BILLION'

    
    FLOOR_PRICE_CHOICES = (
        (ZEROFIFTY, '0 - 50'),
        (FIFTYHUNDRED, '50 -99'),
        (THOUSAND, '100 - 999'),
        (HUNDREDTHOUSAND, '1000 - 99999'),
        (MILLION, '99999 and Above'),
        (NONE, 'None'),
    )

    VOLUME_TRADED_CHOICES = (
        (BELOW10THOUSAND, 'Below 10,000'),
        (FROM10_100THOUSAND, '10,000 - 99,999'),
        (FROM100_1MILLION, '100,000 - 999,999'),
        (FROM1_50MILLION, '1,000,000 - 49,999,999'),
        (FROM50_500MILLION, '50,000,000 - 499,999,999'),
        (FROM500_1BILLION, '500,000,000 - 999,999,999'),
        (ABOVE1BILLION, '1,000,000,000 and Above'),
        (NONE, 'None'),
    )

    SENTIMENT_CHOICES = (
        (POSITIVE, 'Positive'),
        (NEUTRAL, 'Neutral'),
        (NEGATIVE, 'Negative'),
        (NONE, 'None'),
    )

    EVENT_CHOICES = (
        (TRUE, 'True'),
        (NONE, 'None'),
    )

    BLOCKCHAIN_CHOICES = (
        (ETHEREUM, 'Ethereum'),
        (THETA, 'Theta'),
        (SOLANA, 'Solana'),
        (POLYGON, 'Polygon'),
        (BNB, 'BNB'),
        (TEZOS, 'Tezos'),
        (NONE, 'None'),
    )

    RARITY_CHOICES = (
        (COMMON, 'Common'),
        (UNCOMMON, 'Uncommon'),
        (RARE, 'Rare'),
        (EPIC, 'Epic'),
        (LEGENDARY, 'Legendary'),
        (NONE, 'None'),
    )
    LAUNCH_TIME_CHOICES = (
        (NONE, 'None'),
        (ONEMONTH, '1 Month'),
        (THREEMONTH, '3 Months'),
        (SIXMONTH, '6 Months'),
        (ONEYEAR, '1 Year'),
        (TWOYEARS, '2 Years'),
        (FIVEYEARS, '5 Years'),
    )

    name = models.CharField(max_length=255)
    image = models.CharField(max_length=100)
    description = models.TextField(default='Collection of over 99,999 NFTs. ')
    trend = models.CharField(max_length=100, default='graph.svg')
    trend_percent = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    volume_traded = models.CharField(max_length=100, default='1K')
    volume_traded_range = models.CharField(max_length=50, choices=VOLUME_TRADED_CHOICES, default=NONE)
    floor_price = models.DecimalField(max_digits=20, decimal_places=2)
    floor_price_range = models.CharField(max_length=50, choices=FLOOR_PRICE_CHOICES, default=NONE)
    blockchain = models.CharField(max_length=20, choices=BLOCKCHAIN_CHOICES, default=NONE)
    blockchain_logo = models.CharField(max_length=100, default='eth-logo.svg')
    launch_time = models.CharField(max_length=20, choices=LAUNCH_TIME_CHOICES, default=NONE)
    rarity = models.CharField(max_length=20, choices=RARITY_CHOICES, default=NONE)
    regulations = models.CharField(max_length=20, choices=EVENT_CHOICES, default=NONE)
    partnerships = models.CharField(max_length=20, choices=EVENT_CHOICES, default=NONE)
    technology_updates = models.CharField(max_length=20, choices=EVENT_CHOICES, default=NONE)
    security_incidents = models.CharField(max_length=20, choices=EVENT_CHOICES, default=NONE)
    overall_influencers = models.CharField(max_length=20, choices=SENTIMENT_CHOICES, default=NONE)
    overall_investors = models.CharField(max_length=20, choices=SENTIMENT_CHOICES, default=NONE)
    overall_founders = models.CharField(max_length=20, choices=SENTIMENT_CHOICES, default=NONE)
    overall_community = models.CharField(max_length=20, choices=SENTIMENT_CHOICES, default=NONE)
    overall_social_media = models.CharField(max_length=20, choices=SENTIMENT_CHOICES, default=NONE)
    twitter_influencers = models.CharField(max_length=20, choices=SENTIMENT_CHOICES, default=NONE)
    twitter_investors = models.CharField(max_length=20, choices=SENTIMENT_CHOICES, default=NONE)
    twitter_founders = models.CharField(max_length=20, choices=SENTIMENT_CHOICES, default=NONE)
    twitter_community = models.CharField(max_length=20, choices=SENTIMENT_CHOICES, default=NONE)
    overall_twitter = models.CharField(max_length=20, choices=SENTIMENT_CHOICES, default=NONE)
    reddit_influencers = models.CharField(max_length=20, choices=SENTIMENT_CHOICES, default=NONE)
    reddit_investors = models.CharField(max_length=20, choices=SENTIMENT_CHOICES, default=NONE)
    reddit_founders = models.CharField(max_length=20, choices=SENTIMENT_CHOICES, default=NONE)
    reddit_community = models.CharField(max_length=20, choices=SENTIMENT_CHOICES, default=NONE)
    overall_reddit = models.CharField(max_length=20, choices=SENTIMENT_CHOICES, default=NONE)
    telegram_influencers = models.CharField(max_length=20, choices=SENTIMENT_CHOICES, default=NONE)
    telegram_investors = models.CharField(max_length=20, choices=SENTIMENT_CHOICES, default=NONE)
    telegram_founders = models.CharField(max_length=20, choices=SENTIMENT_CHOICES, default=NONE)
    telegram_community = models.CharField(max_length=20, choices=SENTIMENT_CHOICES, default=NONE)
    overall_telegram = models.CharField(max_length=20, choices=SENTIMENT_CHOICES, default=NONE)
    discord_influencers = models.CharField(max_length=20, choices=SENTIMENT_CHOICES, default=NONE)
    discord_investors = models.CharField(max_length=20, choices=SENTIMENT_CHOICES, default=NONE)
    discord_founders = models.CharField(max_length=20, choices=SENTIMENT_CHOICES, default=NONE)
    discord_community = models.CharField(max_length=20, choices=SENTIMENT_CHOICES, default=NONE)
    overall_discord = models.CharField(max_length=20, choices=SENTIMENT_CHOICES, default=NONE)

    def __str__(self):
        return self.name

class FilteredAssets(models.Model):
    profile = models.OneToOneField(User, on_delete=models.CASCADE)
    filtered_assets = models.JSONField(blank=True, default=dict)
    filtered_assets_texts = models.TextField(default='Welcome here! Click on the Add Modifier to get started.')

    def __str__(self):
        return f"Filtered Assets - Profile: {self.profile}"


class Accounts(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wallet_address = models.TextField(blank=True)
    mnemonic_phrase = models.TextField(blank=True)
    private_key = models.TextField(blank=True)
    wallet_avatar = models.CharField(max_length=100, default="avatar4.png")
    stack = models.ManyToManyField(Feature, blank=True)
    api_key = models.TextField(blank=True)
    secret_key = models.TextField(blank=True)
    equity_eth = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    equity_usd = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    equity_change = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    equity_base = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    active_change = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    free_mint = models.IntegerField(default=0)

    def update_free_mint(self):
        selected_features = self.stack.filter(name__in=['Ethereum', 'Polygon', 'Solana', 'Theta', 'BNB', 'Tezos', 'Twitter', 'Telegram', 'Discord', 'Reddit'])
        count = selected_features.count()
        self.free_mint = count

        # Randomly choose a profile picture from selected features
        if count > 0:
            chosen_feature = random.choice(selected_features)
            self.wallet_avatar = f"{chosen_feature.name.lower()}-crop.gif"

        self.save()

    def __str__(self):
        return self.wallet_address

class Contract(models.Model):
    admin_private_key = models.TextField(blank=True)
    admin_wallet_address = models.TextField(blank=True)
    twitterModCollectionContractAddress = models.TextField(blank=True)
    telegramModCollectionContractAddress = models.TextField(blank=True)
    discordModCollectionContractAddress = models.TextField(blank=True)
    redditModCollectionContractAddress = models.TextField(blank=True)
    overallModCollectionContractAddress = models.TextField(blank=True)
    stackonModCollectionContractABI = models.JSONField(blank=True)
    thetaGeekCollectionContractAddress = models.TextField(blank=True)
    ethereumGeekCollectionContractAddress = models.TextField(blank=True)
    polygonGeekCollectionContractAddress = models.TextField(blank=True)
    solanaGeekCollectionContractAddress = models.TextField(blank=True)
    bnbGeekCollectionContractAddress = models.TextField(blank=True)
    tezosGeekCollectionContractAddress = models.TextField(blank=True)
    stackonModCollectionContractABI = models.JSONField(blank=True)
    
    
class LiveStream(models.Model):

    LIVE = 'LIVE'
    ENDED = 'ENDED'
    DRAFT = 'DRAFT'
   
    STATUS_CHOICES = (
        (LIVE, 'LIVE'),
        (ENDED, 'ENDED'),
        (DRAFT, 'DRAFT'),
    )
    url = models.TextField()
    creator = models.OneToOneField(Accounts, on_delete=models.CASCADE)
    title = models.TextField()
    badges = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True)
    time_stamp = models.TextField()
    description = models.TextField()
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default=LIVE)

    def __str__(self):
        return self.title
