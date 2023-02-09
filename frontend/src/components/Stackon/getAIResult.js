import { useState, useEffect } from "react";

function useAIResult(open_price, volume, tweets, sentiment, nft500) {
  const [result, setResult] = useState(0.0);

  useEffect(() => {
    const url = "http://localhost:8000/resultJson";
    const bodyData = JSON.stringify({
      open_price: open_price,
      "24h_volume": volume,
      tweets: tweets,
      public_sentiment: sentiment,
      nft_500_index: nft500,
    });

    const reqOpt = {
      method: "POST",
      headers: { "Content-type": "application/json" },
      body: bodyData,
    };
    const getAI = async () =>
      await fetch(url, reqOpt)
        .then((resp) => resp.json())
        .then((respJ) => {
          setResult(respJ.result);
          console.log(respJ.result);
        });

    getAI();
  }, [open_price, volume, tweets, sentiment, nft500]);
  return result;
}

export default useAIResult;
