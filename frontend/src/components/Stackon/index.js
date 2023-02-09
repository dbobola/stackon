import React, { Component } from "react";
import "./HeroSection.css";
import { ethers } from "ethers";
import Greeter from "../../artifacts/contracts/Greeter.sol/Greeter.json";

import {
  HeroBg,
  HeroContainer,
  VideoBg,
  HeroContent,
  HeroH1,
  HeroP,
  HeroP2,
} from "./HeroElements";
import Video from "../../videos/bg.mp4";
const greeterAddress = "0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512";

const HeroSection = ({ disabled = true }) => {
  return (
    <HeroContainer>
      <HeroBg>
        <VideoBg autoPlay loop muted src={Video} type="video/mp4" />
      </HeroBg>
      <HeroContent>
        <HeroH1>Predict Your Non-Fungible Digital Assets </HeroH1>
        <HeroP>My Non-Fungible Assets</HeroP>
        <HeroP2>
          If you experience delay from getting predictions; kindly reload page
          or click twice.
        </HeroP2>
        <JsonForm />
      </HeroContent>
    </HeroContainer>
  );
};

export default HeroSection;

class JsonForm extends Component {
  constructor(props) {
    super(props);

    this.state = {
      open: 0.02,
      name: "My Asset",
      volume: 5006,
      tweets: 1257,
      sentiment: "Positive",
      nft500: "Neutral",
      result: "",
      isLoaded: true,
      collections: [
        {
          id: 1,
          name: "Mega NFT",
          volume_24h: 1536,
          open_price: "0.0030",
          tweets: 125,
          sentiment: "Positive",
          nft_index: "Neutral",
          image: null,
        },
        {
          id: 2,
          name: "Bored Ninjas",
          volume_24h: 230,
          open_price: "0.4000",
          tweets: 2345,
          sentiment: "Neutral",
          nft_index: "Neutral",
          image: "",
        },
        {
          id: 3,
          name: "Bag Face",
          volume_24h: 768,
          open_price: "0.0040",
          tweets: 1252,
          sentiment: "Positive",
          nft_index: "Positive",
          image: null,
        },
        {
          id: 4,
          name: "Hand of God",
          volume_24h: 4500,
          open_price: "0.7000",
          tweets: 23242,
          sentiment: "Positive",
          nft_index: "Neutral",
          image: null,
        },
        {
          id: 5,
          name: "Yatch Uni",
          volume_24h: 3400,
          open_price: "1.3000",
          tweets: 213311,
          sentiment: "Positive",
          nft_index: "Neutral",
          image: null,
        },
        {
          id: 6,
          name: "Conda NFT",
          volume_24h: 470,
          open_price: "0.1000",
          tweets: 12512,
          sentiment: "Neutral",
          nft_index: "Neutral",
          image: null,
        },
        {
          id: 7,
          name: "Henry's Hat",
          volume_24h: 1250,
          open_price: "2.3000",
          tweets: 22132,
          sentiment: "Neutral",
          nft_index: "Negative",
          image: null,
        },
        {
          id: 8,
          name: "Blue Mood",
          volume_24h: 202,
          open_price: "0.2500",
          tweets: 1253,
          sentiment: "Negative",
          nft_index: "Positive",
          image: null,
        },
        {
          id: 9,
          name: "Jeggers",
          volume_24h: 78,
          open_price: "0.0002",
          tweets: 87,
          sentiment: "Positive",
          nft_index: "Positive",
          image: null,
        },
        {
          id: 10,
          name: "Frame World",
          volume_24h: 53,
          open_price: "0.0030",
          tweets: 879,
          sentiment: "Positive",
          nft_index: "Negative",
          image: null,
        },
        {
          id: 11,
          name: "Cosmos",
          volume_24h: 14100,
          open_price: "15.0000",
          tweets: 231232,
          sentiment: "Positive",
          nft_index: "Positive",
          image: null,
        },
        {
          id: 13,
          name: "JJK",
          volume_24h: 56,
          open_price: "0.0100",
          tweets: 234,
          sentiment: "Positive",
          nft_index: "Positive",
          image: null,
        },
      ],
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleData = this.handleData.bind(this);
  }
  handleData(event) {
    event.preventDefault();
    this.setState({ isLoaded: true });
    fetch("http://127.0.0.1:8000/collections.json")
      .then((response) => response.json())
      .then((data) => {
        this.setState({ isLoaded: true });
        this.setState({ collections: data.collections });
      });
    console.log(this.collections);
  }

  handleChange(event) {
    console.log(event.target.name + " " + event.target.value);
    this.setState({ [event.target.name]: event.target.value });
  }

  handleSubmit(event) {
    if (this.setGreeting()) {
      event.preventDefault();
      // this.setState({ result: "" });
      const url = "http://localhost:8000/resultJson";

      const bodyData = JSON.stringify({
        open_price: this.state.open,
        "24h_volume": this.state.volume,
        tweets: this.state.tweets,
        public_sentiment: this.state.sentiment,
        nft_500_index: this.state.nft500,
      });
      const reqOpt = {
        method: "POST",
        headers: { "Content-type": "application/json" },
        body: bodyData,
      };
      fetch(url, reqOpt)
        .then((resp) => resp.json())
        .then((respJ) => this.setState({ result: respJ.result }));
    }
  }

  async requestAccount() {
    await window.ethereum.request({ method: "eth_requestAccounts" });
  }

  async fetchGreeting() {
    if (typeof window.ethereum !== "undefined") {
      const provider = new ethers.providers.Web3Provider(window.ethereum);
      const contract = new ethers.Contract(
        greeterAddress,
        Greeter.abi,
        provider
      );

      try {
        const data = await contract.greet();
        console.log("data", data);
      } catch (error) {
        console.log("Error: ", error);
      }
    }
  }

  async setGreeting() {
    if (typeof window.ethereum != "undefined") {
      await this.requestAccount();

      const provider = new ethers.providers.Web3Provider(window.ethereum);
      const signer = provider.getSigner();

      const contract = new ethers.Contract(greeterAddress, Greeter.abi, signer);
      const transaction = await contract.setGreeting(this.state.result);

      await transaction.wait();
    }
  }

  render() {
    return (
      <div>
        <div>
          <table>
            <tbody>
              <tr>
                <th>Collection Name</th>
                <th>Opening Price (tCET)</th>
                <th>Volume (24h)</th>
                <th>No of Tweets</th>
                <th>Public Sentiment</th>
                <th>NFT-500 Index</th>
                <th>Closing Price (tCET)</th>
              </tr>
              <tr>
                <td>
                  <input
                    type="text"
                    value={this.state.name}
                    name="name"
                    onChange={this.handleChange}
                  ></input>
                </td>
                <td>
                  <input
                    type="text"
                    value={this.state.open}
                    name="open"
                    onChange={this.handleChange}
                  ></input>
                </td>
                <td>
                  <input
                    type="text"
                    value={this.state.volume}
                    name="volume"
                    onChange={this.handleChange}
                  ></input>
                </td>

                <td>
                  <input
                    type="text"
                    value={this.state.tweets}
                    name="tweets"
                    onChange={this.handleChange}
                  ></input>
                </td>
                <td>
                  <input
                    type="text"
                    value={this.state.sentiment}
                    name="sentiment"
                    onChange={this.handleChange}
                  ></input>
                </td>
                <td>
                  <input
                    type="text"
                    value={this.state.nft500}
                    name="nft500"
                    onChange={this.handleChange}
                  ></input>
                </td>
                <td>
                  <h3>{this.state.result}</h3>
                </td>
              </tr>
            </tbody>
          </table>
          <form onSubmit={this.handleSubmit}>
            <input class="button" type="submit" value="Predict"></input>{" "}
          </form>
        </div>
        <div>
          <table>
            <tbody>
              <tr>
                <th>Collection Name</th>
                <th>Opening Price (tCET)</th>
                <th>Volume (24h)</th>
                <th>No of Tweets</th>
                <th>Public Sentiment</th>
                <th>NFT-500 Index</th>
              </tr>
              {this.state.collections.map((collection) => {
                return (
                  <tr>
                    <td key={collection.id}>{collection.name}</td>
                    <td key={collection.id}>{collection.open_price}</td>
                    <td key={collection.id}>{collection.volume_24h}</td>
                    <td key={collection.id}>{collection.tweets}</td>
                    <td key={collection.id}>{collection.sentiment}</td>
                    <td key={collection.id}>{collection.nft_index}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    );
  }
}
