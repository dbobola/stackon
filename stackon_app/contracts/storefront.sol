pragma solidity ^0.8.0;

import "./ThetaToken.sol";
import "./ThetaDrop.sol";
import "./ThetaAuction.sol";
import "@openzeppelin/contracts/token/ERC721/IERC721.sol";

contract NFTStorefront {
    // Declare the necessary Theta library instances
    ThetaToken private thetaToken;
    ThetaDrop private thetaDrop;
    ThetaAuction private thetaAuction;

    struct Listing {
        address seller;
        address nftContract;
        uint256 tokenId;
        uint256 price;
        bool active;
    }

    mapping(uint256 => Listing) private listings;

    event NFTListed(uint256 listingId, address seller, address nftContract, uint256 tokenId, uint256 price);
    event NFTSold(uint256 listingId, address buyer, address seller, address nftContract, uint256 tokenId, uint256 price);

    constructor(
        address _thetaTokenAddress,
        address _thetaDropAddress,
        address _thetaAuctionAddress
    ) {
        // Initialize the Theta library instances
        thetaToken = ThetaToken(_thetaTokenAddress);
        thetaDrop = ThetaDrop(_thetaDropAddress);
        thetaAuction = ThetaAuction(_thetaAuctionAddress);
    }

    function listNFT(address _nftContract, uint256 _tokenId, uint256 _price) external {
        require(!_isNFTListed(_nftContract, _tokenId), "NFT is already listed");
        require(IERC721(_nftContract).ownerOf(_tokenId) == msg.sender, "Only NFT owner can list");

        // Transfer the NFT to the storefront contract
        IERC721(_nftContract).transferFrom(msg.sender, address(this), _tokenId);

        // Create a new listing
        uint256 listingId = _generateListingId();
        listings[listingId] = Listing({
            seller: msg.sender,
            nftContract: _nftContract,
            tokenId: _tokenId,
            price: _price,
            active: true
        });

        emit NFTListed(listingId, msg.sender, _nftContract, _tokenId, _price);
    }

    function buyNFT(uint256 _listingId) external payable {
        require(_isNFTListed(_listingId), "Invalid listing");
        Listing storage listing = listings[_listingId];
        require(listing.active, "Listing is inactive");
        require(msg.value >= listing.price, "Insufficient funds");

        // Transfer the NFT from the storefront contract to the buyer
        IERC721(listing.nftContract).transferFrom(address(this), msg.sender, listing.tokenId);

        // Transfer the payment to the seller
        payable(listing.seller).transfer(msg.value);

        // Deactivate the listing
        listing.active = false;

        emit NFTSold(_listingId, msg.sender, listing.seller, listing.nftContract, listing.tokenId, listing.price);
    }

    function _isNFTListed(address _nftContract, uint256 _tokenId) internal view returns (bool) {
        for (uint256 i = 1; i <= _getLatestListingId(); i++) {
            Listing storage listing = listings[i];
            if (listing.nftContract == _nftContract && listing.tokenId == _tokenId) {
                return true;
            }
        }
        return false;
    }

    function _getLatestListingId() internal view returns (uint256) {
        if (_getTotalListings() == 0) {
            return 0; 
        }
        return _getTotalListings();
    }

    function _getTotalListings() internal view returns (uint256) {
        // Iterate over all the listings and count the active ones
        uint256 totalListings = 0;
        for (uint256 i = 1; i <= _getListingCount(); i++) {
            if (listings[i].active) {
                totalListings++;
            }
        }
        return totalListings;
    }

    function _getListingCount() internal view returns (uint256) {
        // Return the total number of listings
        return listings.length - 1;
    }
}
