import { useEffect, useState } from "react";
import useAIResult from "./getAIResult";

function GetData() {
  const [collectiondata, setData] = useState([]);
  useEffect(() => {
    const fetchData = async () =>
      await fetch("http://127.0.0.1:8000/collections.json")
        .then((response) => response.json())
        .then((data) => {
          console.log(data.collections[1].name);
          setData(data.collections);
        });

    fetchData();
  }, []);

  const result = useAIResult(
    collectiondata[0].open_price,
    collectiondata[0].volume_24h,
    collectiondata[0].tweets,
    collectiondata[0].sentiment,
    collectiondata[0].nft_index
  );

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
              <th>Closing Price (In 24h)</th>
              <th>Percentage Increase (In 24h)</th>
            </tr>
            {collectiondata.map((collection) => {
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
      <div>result = {result}</div>
    </div>
  );
}

export default GetData;
